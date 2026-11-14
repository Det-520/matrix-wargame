# Map

The game map is one SVG, `map/source/map.svg` (the path is set in `game.toml` `[map]`). Draw it in any tool that saves SVG (Inkscape, Illustrator, Figma, or by hand), or generate it with a script. The base ships a placeholder: thirteen zones, Z1–Z13, that match the example rows in `scenario/00-overview.md` §3.2.

## Building

```bash
tools/build_map.sh
```

| Output | What it is |
| --- | --- |
| `map/maps/<name>.png` | 2× raster, for checking |
| `map/maps/<name>_full.pdf` | One page, at the size of the assembled tiles, for a plotter |
| `map/maps/<name>_tiles_letter.pdf` | `tiles` × `tiles` US Letter pages to trim and tape |
| `handouts/assets/game-map.png` | The image the Scenario Brief embeds |

`<name>` and `tiles` come from `game.toml` `[map]`. `tools/build_handouts.sh` copies the two PDFs into `build/Common Scenario - 1WK RELEASE/` as `map-full.pdf` and `map-tiles.pdf`. The scripts read the SVG's size from its `width` and `height` attributes, or else its `viewBox`, so any aspect ratio works. A 3:2 map on 3 × 3 tiles fits letter pages with little waste.

## Drawing a map that plays well

- **Zones, not hexes.** Counters go in zones (`RULES.md` §4.5). Label each zone with its ID in large type (`Z7`) and a short name under it. Keep the IDs stable once anything else references them.
- **Big enough for counters.** A counter is about 1 in square, and a busy zone may hold eight. On the printed map, a land zone that matters should be at least 4 in across. Check the tiles at print size before you finish.
- **Off-map boxes** (dashed outline) hold each side's home and any distant backer: Z1 and Z2 in the placeholder.
- **Colour by alignment**, lightly, so counters stay readable: one tint for each side's territory, one for neutrals, one for the other side's partners. Water is the background.
- **A scale grid** (100 mi squares in the placeholder) lets players argue distance without a ruler. If a distance on the map matters to the game, record it in `scenario/00-overview.md` §3.3 so the white cell rules on the same number every time.
- **No secrets.** The map goes to both teams. Don't mark hidden bases, routes, or objectives on it.
- **Fonts.** The placeholder uses Inter, which `tools/fetch_third_party.py` downloads into `map/fonts/` and `build_map.sh` makes visible to Chromium. Any other font has to be installed on the build machine, or converted to outlines in the SVG.

## When the map changes

1. Rebuild with `tools/build_map.sh`.
2. Update the zone table and distances in `scenario/00-overview.md` §3.2–3.3, and any zone IDs in `scenario/data/assets.csv` (then run `python3 tools/check_assets.py`).
3. Rebuild the handouts so the Scenario Brief picks up the new image.
