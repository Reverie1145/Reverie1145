#!/usr/bin/env python3
"""Collect PUBLIC data for the profile cards.

Only /users/{u}, /users/{u}/repos (filtered to non-private) and
/users/{u}/events/public are used: nothing private ever reaches data.json.

usage: GITHUB_TOKEN=... python3 fetch.py --user Reverie1145 --out data.json
"""
import argparse, datetime as dt, json, os, urllib.request

API = "https://api.github.com"


def get(path, token=None):
    req = urllib.request.Request(API + path, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "profile-cards/1.0",
        **({"Authorization": "Bearer " + token} if token else {}),
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def _initials(name):
    words = [w for w in name.replace("-", " ").replace("_", " ").split() if w]
    if len(words) >= 2:
        return (words[0][0] + words[1][0]).upper()
    return name[:2].upper()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", required=True)
    ap.add_argument("--out", default="data.json")
    ap.add_argument("--tagline", default="𝕭𝖊𝖆𝖚𝖙𝖞 𝖋𝖆𝖉𝖊𝖘, 𝖇𝖞𝖕𝖆𝖘𝖘 𝖗𝖊𝖒𝖆𝖎𝖓𝖘.")
    ap.add_argument("--chips", default="watch apps|tooling|reverse engineering")
    a = ap.parse_args()
    tok = os.environ.get("GITHUB_TOKEN")

    u = get("/users/" + a.user, tok)
    repos = [r for r in get(f"/users/{a.user}/repos?per_page=100&type=owner&sort=pushed", tok) if not r["private"]]
    try:
        events = get(f"/users/{a.user}/events/public?per_page=100", tok)
    except Exception:
        events = []

    today = dt.date.today()
    days = [0] * 90
    commits30 = 0
    last_push = None

    # Events only carry recent, aggregated pushes and miss commits created through
    # the REST API, so count real commits per public repo as well.
    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=90)).isoformat(timespec="seconds")
    counted = 0
    for r in repos:
        if r["name"].lower() == a.user.lower() or r.get("fork"):
            continue
        try:
            hist = get(f"/repos/{r['full_name']}/commits?since={since}&per_page=100", tok)
        except Exception:
            continue
        for c in hist if isinstance(hist, list) else []:
            stamp = c.get("commit", {}).get("committer", {}).get("date") or ""
            if len(stamp) < 10:
                continue
            d = dt.date.fromisoformat(stamp[:10])
            delta = (today - d).days
            if 0 <= delta < 90:
                days[89 - delta] += 1
                if delta < 30:
                    commits30 += 1
            if last_push is None or stamp > last_push:
                last_push = stamp
            counted += 1
    if counted:
        events = []
    for e in events:
        if e.get("type") != "PushEvent":
            continue
        d = dt.date.fromisoformat(e["created_at"][:10])
        delta = (today - d).days
        if 0 <= delta < 90:
            n = len(e.get("payload", {}).get("commits", [])) or 1
            days[89 - delta] += n
            if delta < 30:
                commits30 += n
        if last_push is None or e["created_at"] > last_push:
            last_push = e["created_at"]

    total90 = sum(days)
    if last_push:
        gap = (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(last_push.replace("Z", "+00:00"))).days
        state = "ACTIVE" if gap <= 7 else ("IDLE" if gap <= 30 else "DORMANT")
        detail = f"last public push {gap}d ago" if gap else "last public push today"
    else:
        state, detail = "DORMANT", "no public pushes in 90d"

    # the profile repo itself is not "work" — it is the page
    projs = [r for r in repos if r["name"].lower() != a.user.lower()]
    projs = sorted(projs, key=lambda r: r["pushed_at"] or "", reverse=True)[:3]
    projects = [{
        "name": r["name"],
        "desc": (r["description"] or "no description yet").strip()[:140],
        "initials": _initials(r["name"]),
        "tag": "PUBLIC",
    } for r in projs]

    data = {
        "name": u.get("name") or u["login"],
        "handle": u["login"],
        "tagline": a.tagline,
        "chips": a.chips.split("|"),
        "state": state,
        "state_detail": detail,
        "metrics": [
            {"value": str(u["public_repos"]), "label": "public repos"},
            {"value": str(commits30), "label": "commits · 30d"},
            {"value": str(total90), "label": "commits · 90d"},
        ],
        "activity": {"days": days, "total": total90,
                     "caption": "public commits · rolling 90 days",
                     "left_label": "90d ago", "right_label": "today",
                     "empty": "no public activity in this window"},
        "projects": projects,
        "stack": ["Python", "JavaScript", "Java", "Kotlin", "Linux", "Docker"],
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
    }
    json.dump(data, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"wrote {a.out}: state={state} repos={u['public_repos']} c30={commits30} c90={total90}")


if __name__ == "__main__":
    main()
