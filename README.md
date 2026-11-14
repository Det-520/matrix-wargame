# Matrix Wargame Base

A starting point for building a two-sided matrix wargame (REDFOR vs. BLUEFOR with a white cell) to run as an AFROTC leadership exercise. It holds a scenario-free rule set, templates for every scenario file and handout, and the tools that turn the markdown into printable release packets, counters, a map, a white cell clock, and a white cell reference site.

It was generalized from *Operation Zugzwang* (AFROTC LLAB 12, November 2026). The rules, forms, schedule, and build are the ones that ran there. The scenario files are templates with a small Redland vs. Blueland example, so the build works before you write anything.

> **Demo.** The base's own example builds into a live site on GitHub Pages on every push to `main`: the white cell site, every release PDF, and the timer and dice program. See [Publishing the white cell site](#publishing-the-white-cell-site).
>
> **Secrecy.** Once you fill in a scenario, this repository holds both teams' secret packets, the white cell's ground truth, and the injects. Keep your scenario's repository private, and don't share it with players.

## Starting a new scenario

1. Copy this repository (GitHub **Use this template**, or clone it and change the remote).
2. Fetch the third-party files and build the example once to check your setup (see [Building](#building)).
3. Edit `game.toml`: the game's name, designer, event, date, number of tables, side names, the rule set (full, or basic for new players), the run of show (the phases, their order and timing, and the turns in each), the tracks, and the Tongue and Quill letterheads. The default run of show is the first game's: four phases and 7 turns in a 3-hour block (`RULES.md` §2.1).
4. Follow `DESIGN-GUIDE.md`. It walks through the scenario files in the order that works best, from the public world to the injects.
5. Draw the map (`map/README.md`) and fill in the handouts (`handouts/`).
6. Rebuild, playtest, and repeat.

## Where things are

| Path | What it is |
| --- | --- |
| `game.toml` | The facts about this game that the tools read: name, dates, tables, rule set, run of show (phases, timing, turns), tracks, map, Tongue and Quill documents |
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
| Timer settings, template check | `python3 tools/schedule.py --write` (the next two steps run it), `--check` | `tools/whitecell-clock.html` |
| Map | `tools/build_map.sh` | `map/maps/`, `handouts/assets/game-map.png` |
| Release PDFs | `tools/build_handouts.sh` (`--only NAME` for one, `SKIP_TQ=1` to skip WordCraft) | `build/`, by release folder |
| White cell site | `tools/build_site.sh` (`serve` to preview) | `site/book/` |
| Publish | `.github/workflows/pages.yml` | GitHub Pages |

Needs Python 3.11 or later, Chromium 131 or later, poppler-utils (`pdftotext`, `pdftoppm`), [mdbook](https://rust-lang.github.io/mdBook/) 0.5 or later, and `wordcraft-cli` for the Tongue and Quill documents. On NixOS the scripts pull the Python packages with `nix-shell` (`tools/pyenv.sh`). Elsewhere, install `jinja2`, `markdown-it-py`, `mdit-py-plugins`, `pypdf`, and `playwright`.

Without WordCraft (or with `SKIP_TQ=1`), the build uses the files committed in `handouts/word/`. If a document has none yet, it prints the markdown version instead and says so. After changing a Tongue and Quill document, run `python3 tools/tq/build_tq.py` and commit the results.

Air Force sites often refuse scripted downloads. When one does, `fetch_third_party.py` prints the URL: open it in a browser, save the file to the path shown, and run the script again to check it and make its text copy.

### Changing the schedule and timing

The phase structure and timing live in `game.toml`: `[schedule]` (start time, parley length, which turn step can be shortened), `[[block]]` (each phase or break in order, with its steps or its number of turns), and `[[turn_step]]` (the steps of one turn). The timer program, the schedule and turn clock tables, every time and limit the rules and handouts quote, the turn count, and the number of forms printed all follow it.

```bash
python3 tools/schedule.py            # print the schedule with clock times (whitecell for the white cell's)
python3 tools/schedule.py --write    # refresh the timer's settings (the builds do this too)
```

To try a different schedule without editing files, open `tools/whitecell-clock.html` in a browser and choose **Setup**. **Apply** keeps the change in that browser, **Download page** saves a copy of the program with it built in, and **Copy as game.toml** gives the text to paste back into `game.toml`.

### Choosing the rule set

`game.toml` `[rules]` `set` picks the rules the game is played with (`RULES.md` §0). `"full"` is every rule: players get the Player Rules Handbook, with the Basic Rules as a short first read. `"basic"`, for groups new to matrix games, drops secret COAs and the estimative vote: players get the Basic Rules in place of the handbook, and the player forms, the Print Packet, the timer, and the white cell documents follow on the next build. Text that holds for one rule set only sits inside `{% if rules == "full" %}` … `{% endif %}` (below).

### Documents are templates

Every markdown document (handouts, `RULES.md`, `scenario/`) is a [Jinja2](https://jinja.palletsprojects.com/templates/) template, filled in from `game.toml` when the PDFs and the site are built. Never type a number `game.toml` sets: quote it.

```text
Each turn is **{{ mins(turn_min) }}** of real time and about **{{ days(game_days) }}** of game time,
so {{ turns }} turns cover about {{ days(game_days * turns) }}.
Post up to {{ requests }} requests (Phase I: {{ planning_requests }}, due at minute {{ request_deadline }}).
Prepare runs {{ steps.prep.span }}; Phase IV is Turns {{ blocks.P4.turns }} ({{ blocks.P4.span }}).
{% if rules == "full" %}Secret COAs ...{% else %}...{% endif %}
{{ turn_clock_table() }}    {{ schedule_table("whitecell") }}    | {{ ticks() }} |
```

- `python3 tools/schedule.py values` lists every name: the numbers, `steps.ID` (each `[[turn_step]]` by `id`) and `blocks.TAG` (each `[[block]]` by `tag`), and the functions `mins()`, `clock()` (`5:00`), `word()` and `Word()` (`four`), `days()` (`3 days`, `3 weeks`; `days(n, adj=True)` gives `3-day`), `ticks()`, `turn_columns()`, `turn_rule()`, `schedule_table()`, and `turn_clock_table()`.
- Use the function form, not Jinja filters (`{{ mins(turn_min) }}`, not `{{ turn_min | mins }}`): a `|` breaks a markdown table.
- A `{% if %}` or `{% endif %}` alone on its line disappears with the line. Don't put one on its own line inside a table or a list; put it inside the cell or the item instead.
- Anything in backticks is printed as written, so a document can show an example.
- The game.toml texts (`say`, `brief`) are templates too; there, write the test as `{% if rules == 'full' %}` (single quotes).
- A misspelled name stops the build with the file and line. `python3 tools/schedule.py --check` (run in CI) renders every document under both rule sets.

### Publishing the white cell site

`.github/workflows/pages.yml` builds everything and publishes the site to GitHub Pages. In this base repository it runs on every push to `main`, so the example is always online as a demo. In any other copy it runs only when you start it by hand (**Actions → Publish site → Run workflow**), because a GitHub Pages site is public even when the repository is private, and a scenario's site shows both sides' secrets. Publish a scenario only if you accept that, or host it somewhere access-controlled. To publish a copy on every push anyway, set the repository variable `PUBLISH_ON_PUSH` to `true`.

Once per repository, set **Settings → Pages → Build and deployment → Source** to **GitHub Actions**. The site uses relative links, so it works under any path (`https://<owner>.github.io/<repository>/`), and also straight from `site/book/index.html` on a laptop. The timer is at `tools/whitecell-clock.html` on the site.
