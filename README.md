# Matrix Wargame Base

A starting point for building a two-sided matrix wargame (REDFOR vs. BLUEFOR with a white cell) to run as an AFROTC leadership exercise. It holds a scenario-free rule set, templates for every scenario file and handout, and the tools that turn the markdown into printable release packets, counters, a map, a white cell clock, and a white cell reference site.

It was generalized from *Operation Zugzwang* (AFROTC LLAB 12, November 2026). The rules, forms, schedule, and build are the ones that ran there. The scenario files are templates with a small Redland vs. Blueland example, so the build works before you write anything.

> **Secrecy.** Once you fill in a scenario, this repository holds both teams' secret packets, the white cell's ground truth, and the injects. Keep your scenario's repository private, and don't share it with players.

## Starting a new scenario

1. Copy this repository (GitHub **Use this template**, or clone it and change the remote).
2. Fetch the third-party files and build the example once to check your setup (see [Building](#building)).
3. Edit `game.toml`: the game's name, designer, event, date, number of tables, turns, side names, and the Tongue and Quill letterheads.
4. Follow `DESIGN-GUIDE.md`. It walks through the scenario files in the order that works best, from the public world to the injects.
5. Draw the map (`map/README.md`) and fill in the handouts (`handouts/`).
6. Rebuild, playtest, and repeat.

## Where things are

| Path | What it is |
| --- | --- |
| `game.toml` | The facts about this game that the tools read: name, dates, tables, turn counts, map, Tongue and Quill documents |
| `RULES.md` | How to play: turns, COAs, adjudication, requests, injects. Scenario-free. |
| `EVENT-SETUP.md` | Event logistics: schedule, rooms, groups, staffing, evaluation, risks |
| `DESIGN-GUIDE.md` | How to build a scenario from these templates, with balance heuristics and lessons learned |
| `scenario/` | The world, each side's forces and objectives, injects, and ground truth (templates; `scenario/README.md`) |
| `handouts/` | The documents players and the white cell get, by audience. The markdown is the source for every PDF and the site. |
| `map/` | The map's master SVG and the scripts that print it (`map/README.md`) |
| `tools/` | Build scripts, the counters generator, the Tongue and Quill builder, and the white cell clock |
| `site/` | The white cell site's settings and style (mdbook; `site/README.md`) |
| `references/` | Training objective, writing and doctrine references |

`AGENTS.md` is the full file map and the rules for editing (also read by AI agents through `CLAUDE.md`).

## Building

The release PDFs, the map, and the site are built from the sources and aren't in git. Files that belong to others (the reference PDFs, the Air Force Word templates, and the fonts) aren't in git either: a script downloads them.

```bash
python3 tools/fetch_third_party.py   # once after cloning
tools/build_all.sh                   # map, counters, Tongue and Quill documents, build/, site
npx markdownlint-cli2                # after editing markdown: keep it at 0 issues
```

| Step | Script | Output |
| --- | --- | --- |
| Map | `tools/build_map.sh` | `map/maps/`, `handouts/assets/game-map.png` |
| Release PDFs | `tools/build_handouts.sh` (`--only NAME` for one, `SKIP_TQ=1` to skip WordCraft) | `build/`, by release folder |
| White cell site | `tools/build_site.sh` (`serve` to preview) | `site/book/` |
| Publish (manual) | `.github/workflows/pages.yml` | GitHub Pages |

Needs Python 3.11 or later, Chromium 131 or later, poppler-utils (`pdftotext`, `pdftoppm`), [mdbook](https://rust-lang.github.io/mdBook/) 0.5 or later, and `wordcraft-cli` for the Tongue and Quill documents. On NixOS the scripts pull the Python packages with `nix-shell`. Elsewhere, install `markdown-it-py`, `mdit-py-plugins`, `pypdf`, and `playwright`.

Without WordCraft (or with `SKIP_TQ=1`), the build uses the files committed in `handouts/word/`. If a document has none yet, it prints the markdown version instead and says so. After changing a Tongue and Quill document, run `python3 tools/tq/build_tq.py` and commit the results.

Air Force sites often refuse scripted downloads. When one does, `fetch_third_party.py` prints the URL: open it in a browser, save the file to the path shown, and run the script again to check it and make its text copy.

### Publishing the white cell site

The workflow runs only when you start it by hand (**Actions → Publish site → Run workflow**). A GitHub Pages site is public even when the repository is private, and this site shows both sides' secrets, so publish it only if you accept that, or host it somewhere access-controlled. Set **Settings → Pages → Source** to **GitHub Actions**. The site uses relative links, so it works under any path, and also straight from `site/book/index.html` on a laptop.
