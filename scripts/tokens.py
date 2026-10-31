"""Material 3 design tokens (baseline violet seed #6750A4).

Two schemes, same semantic names. Everything rendered from these — no hard
coded colours anywhere else, so swapping the seed re-skins all six cards.
"""

LIGHT = dict(
    primary="#6750A4", on_primary="#FFFFFF",
    primary_container="#EADDFF", on_primary_container="#21005D",
    secondary="#625B71", secondary_container="#E8DEF8", on_secondary_container="#1D192B",
    tertiary="#7D5260", tertiary_container="#FFD8E4", on_tertiary_container="#31111D",
    surface="#FEF7FF", surface_dim="#DED8E1",
    surface_container_lowest="#FFFFFF", surface_container_low="#F7F2FA",
    surface_container="#F3EDF7", surface_container_high="#ECE6F0", surface_container_highest="#E6E0E9",
    on_surface="#1D1B20", on_surface_variant="#49454F",
    outline="#79747E", outline_variant="#CAC4D0",
    inverse_surface="#322F35", inverse_on_surface="#F5EFF7",
    shadow="#000000", scrim="#000000",
)

DARK = dict(
    primary="#D0BCFF", on_primary="#381E72",
    primary_container="#4F378B", on_primary_container="#EADDFF",
    secondary="#CCC2DC", secondary_container="#4A4458", on_secondary_container="#E8DEF8",
    tertiary="#EFB8C8", tertiary_container="#633B48", on_tertiary_container="#FFD8E4",
    surface="#141218", surface_dim="#141218",
    surface_container_lowest="#0F0D13", surface_container_low="#1D1B20",
    surface_container="#211F26", surface_container_high="#2B2930", surface_container_highest="#36343B",
    on_surface="#E6E0E9", on_surface_variant="#CAC4D0",
    outline="#938F99", outline_variant="#49454F",
    inverse_surface="#E6E0E9", inverse_on_surface="#322F35",
    shadow="#000000", scrim="#000000",
)

SANS = "Roboto, 'Google Sans', 'Helvetica Neue', Arial, sans-serif"
MONO = "'Roboto Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

# Material 3 type scale (size, line-height, weight, letter-spacing)
TYPE = {
    "display_small": (36, 44, 400, 0.0),
    "headline_small": (24, 32, 400, 0.0),
    "title_large": (22, 28, 400, 0.0),
    "title_medium": (16, 24, 500, 0.15),
    "title_small": (14, 20, 500, 0.1),
    "body_large": (16, 24, 400, 0.5),
    "body_medium": (14, 20, 400, 0.25),
    "body_small": (12, 16, 400, 0.4),
    "label_large": (14, 20, 500, 0.1),
    "label_medium": (12, 16, 500, 0.5),
    "label_small": (11, 16, 500, 0.5),
}

# corner scale (dp)
RADIUS = dict(xs=4, sm=8, md=12, lg=16, xl=20, full=28, pill=999)
GUTTER = 16          # 8dp grid
PAD = 24
