# Presets — Teams, Cells, Assets, Tracks, and Scenario Elements

**Audience:** designer. Generic building blocks, with no scenario in them; nothing here is secret until you copy it into a scenario.

This folder holds ready-made pieces to build a scenario from, so you start from a sound example instead of a blank page. `tools/presets.py` lists them and copies them into the scenario files, and every one can be edited after it is copied. `DESIGN-GUIDE.md` §2 says when in the design each one comes in.

| File | What it holds | Copied in by |
| --- | --- | --- |
| `teams.toml` | Four archetypes for a third or fourth player team (§1) | `python3 tools/presets.py add-team KEY` |
| `cells.toml` | Seventeen cells a team can be split into, each with a brief for its players (§2) | `python3 tools/presets.py add-cell SIDE [KEY ...]` |
| `assets.csv` | Eighty-six real U.S. systems, forces, and authorities, each with a role and a limitation (§3) | `python3 tools/presets.py add-asset SIDE KEY ...` |
| `asset-reference.md` | The asset catalog as a readable reference, by category (generated) | `python3 tools/presets.py reference --write` |
| `tracks.toml` | Eleven tracks with triggers (§4) | `python3 tools/presets.py add-track KEY ...` |
| `scenario-elements.md` | Injects, starting conditions, objectives, intelligence products, and run-of-show options to adapt (§5) | By hand |
| `templates/` | The files `add-team` and `add-cell` write: a team's packet and handouts, and a cell brief | — |

```bash
python3 tools/presets.py list teams          # or cells, assets, tracks
python3 tools/presets.py list assets --category tanker
python3 tools/presets.py list assets --search "anti-ship"
python3 tools/presets.py show air            # one preset in full
```

Every command that changes `game.toml` loads the result with `tools/game.py` first and leaves the file alone if it wouldn't load. No command overwrites a file that already exists. After one that changes `game.toml`, run `python3 tools/schedule.py --write` so the timer program follows (the builds do it too).

## 1. Teams

Two teams (BLUEFOR and REDFOR) is the default and the right number for most events. Add a team only for an actor with **real capacity for independent action** and objectives that pull against **every** other team (Mouat, *Practical Advice on Matrix Games*, "Number of Actors"; `DESIGN-GUIDE.md` §2.1; `RULES.md` §2.6). An actor that matters only now and then is cheaper as a white-cell actor with X- counters.

| Key | Label | Prefix | Archetype | Pulls against every team because… | Suggested cells |
| --- | --- | --- | --- | --- | --- |
| `grayfor` | GRAYFOR | G | Contested host nation | It needs the stronger power's protection but fears its presence, and it trades with the other side | diplo, land, info |
| `greenfor` | GREENFOR | C | Coalition partner with its own agenda | It shares its ally's main goal but not the price or the end state, and can make a separate deal | air, diplo |
| `yellowfor` | YELLOWFOR | Y | Non-state armed group | Both main teams want to use it or stamp it out, and its cause pulls against the host and its sponsor | sof, info, civil |
| `purplefor` | PURPLEFOR | P | Outside power or opportunist | It can arm either side, mediate, or wait for both to tire; it wants neither to win outright | diplo, info, intel |

The colour names are a convention, not a rule: label and colour the team whatever suits the scenario.

```bash
python3 tools/presets.py add-team grayfor
python3 tools/presets.py add-team greenfor --nation "[Green nation]" --cells air,diplo
python3 tools/presets.py add-team yellowfor --id militia --label MILITIA --prefix M
```

`add-team` does the mechanical part of `DESIGN-GUIDE.md` §2.1:

1. Adds the `[[side]]` to `game.toml`, its COA step after the other COA steps and its Cons step after the other Cons steps, and a minute to the white cell's resolve step.
2. Writes the team's files from `templates/team/`: `scenario/<id>-packet.md`, and in `handouts/<id>/` the team packet, order of battle, commander's letter, and an intelligence folder with a read-me-first and one sample product (`<prefix>I-01`).
3. Copies the archetype's starter assets into `scenario/data/assets.csv` and the packet (`--no-assets` to skip), and adds cells if you name them (`--cells`).

The team packet it writes has a section for the players on **playing one of three or more teams**: no ally by default, talk to everyone, spend Cons where they matter, expect deals aimed at you. The Player Rules Handbook (§2.1, §2.6) and the Basic Rules carry the same guidance to every player whenever `game.toml` has more than two teams, and the White Cell Handbook §4.2 tells the white cell what changes.

It then lists what only you can write: the team's actor entry, starting conditions, and directives in the scenario overview and the Scenario Brief; its rows in the white cell's documents; its objectives; and its placement form. Rewrite every file it wrote, too: they are templates with the archetype's typical wants and levers as a starting point.

Prefixes X, S, I, O, and Z are taken (third parties, starting conditions, injects, open items, zones), and each team needs its own. A third team costs about 4 minutes a turn, so plan a shorter Prepare or one turn fewer (`presets/scenario-elements.md` §5.4 has a run of show for three teams).

## 2. Cells (sub-teams)

A team can be split into **cells** under its flight commander: an intelligence cell, an air component, a diplomatic cell (`RULES.md` §9.4). The team still makes one COA a turn. Each cell pitches the COA it thinks matters most, and the commander chooses. Cells suit a team of more than about 8 players, or an exercise about coordination inside a staff.

### 2.1 The catalog

| Key | Short | Cell | Fits |
| --- | --- | --- | --- |
| `ops` | OPS | Operations Cell | Any large team; the natural home of the briefer |
| `plans` | PLN | Plans Cell | Objectives that take several COAs; exercises about planning |
| `intel` | INT | Intelligence Cell | Almost any team, and any scenario with hidden assets |
| `air` | AIR | Air Component | Any team with more than a handful of aircraft |
| `maritime` | SEA | Maritime Component | A strait, sea lane, island, or blockade |
| `land` | LAND | Land Component | Ground forces in contact, an island to hold, a host nation's army |
| `amd` | AMD | Air and Missile Defense Cell | A defending team that will be struck |
| `mobility` | LOG | Logistics and Mobility Cell | A team far from home; reinforcement and sustainment |
| `base` | ACE | Basing and ACE Cell | Air forces at bases the enemy can reach; teaches Agile Combat Employment |
| `space` | SPC | Space Cell | Contested satellite communications, navigation, or warning |
| `cyber` | CYB | Cyber Cell | Infrastructure, elections, or networks worth attacking |
| `info` | INFO | Information and Public Affairs Cell | Any scenario with opinion, will, or legitimacy tracks |
| `diplo` | POL | Diplomatic Cell | A negotiated objective, or a third party both sides court |
| `legal` | JAG | Legal Cell | Tight rules of engagement or national directives |
| `sof` | SOF | Special Operations Cell | A partner force, a population, targets that need people on the ground |
| `civil` | CA | Civil Affairs Cell | A population, refugees, a host nation, or a humanitarian track |
| `comms` | COM | Communications and Records Cell | Large teams, and exercises about staff work |

`python3 tools/presets.py show KEY` prints a cell in full: its lead, its job, its concern, the asset categories it usually owns, the cells it works with, and example RFIs, COAs, and Pros.

### 2.2 Choosing cells

- **Two to four cells a team**, about two players each, plus the flight commander. More cells than that means more pitching than deciding.
- **Pick cells whose concerns pull against each other**, so the team has to agree before it acts ("a house divided", Mouat). Good pairs: operations and logistics (tempo against sustainment), air and legal (a bold strike against the rules of engagement), information and operations (legitimacy against effect), intelligence and plans (certainty against time).
- **Give every cell counters or a track to own.** A cell with nothing on the map and nothing on the screen has nothing to pitch. The diplomatic, information, and legal cells own talks, tracks, and authorities instead of counters: make sure the scenario has those.
- Cells can differ between teams. A team far from home might want logistics; a host nation, diplomacy and civil affairs.

Some sets that work together:

| Scenario | Cells |
| --- | --- |
| Air campaign | `intel`, `air`, `mobility` |
| Maritime crisis | `intel`, `maritime`, `air`, `info` |
| Defending team under missile attack | `amd`, `base`, `air` |
| Gray-zone crisis below the threshold of war | `diplo`, `info`, `legal`, `cyber` |
| Staff exercise (coordination is the point) | `ops`, `plans`, `intel`, `mobility` |
| Host nation or partner team | `diplo`, `land`, `civil` |

### 2.3 Adding cells

Three ways, all equivalent:

```bash
python3 tools/presets.py add-cell redfor              # a checklist: tick the cells you want
python3 tools/presets.py add-cell redfor intel air    # no questions
```

or by hand in `game.toml`, under the team's `[[side]]`, either as a list of keys or as entries that change a preset's fields:

```toml
[[side]]
id = "redfor"
# ...
cells = ["intel", "air"]

  [[side.cell]]
  preset = "mobility"
  name = "Logistics Readiness Cell"   # any of name, short, lead, job overrides the preset
```

The tool also writes each cell's **brief** to `handouts/<side>/cells/<cell>.md` (`--no-brief` to skip); by hand, copy `templates/cell-brief.md.tmpl` and fill in its `$` fields. A cell brief is the cell's players' instructions: how a team with cells works, the counters the cell owns (a table filled in from the `cell` column of `scenario/data/assets.csv` on every build), its part in each step of the turn, its concern, and example RFIs, COAs, and Pros. Rewrite the examples for the scenario. The brief goes into the team's release folder and on the site.

Then give each cell its counters: set the `cell` column in `scenario/data/assets.csv` (or `add-asset ... --cell KEY`). The counters print the cell's short name after the owner.

Once a team has cells, the players' documents follow on the next build: the Player Rules Handbook §2.10 lists every team's cells and how to work in one, the Basic Rules say the same in brief, the team packet lists the team's own cells, and the White Cell Handbook §4.2 tells the white cell how to hear a team with cells.

## 3. Assets

`assets.csv` is a catalog of real U.S. systems, with an Air Force emphasis (`AGENTS.md` rule 7). Capabilities are unclassified, approximate, and simplified for play, and every row has a limitation another team can use as a Con. `asset-reference.md` shows it as a reference by category; read it when you build forces, and give it to the white cell to answer "what does that do?" quickly.

| Column | Meaning |
| --- | --- |
| `key` | The preset's name in commands |
| `category` | fighter, bomber, ew, tanker, airlift, logistics, c2, isr, space, cyber, air-defense, fires, naval, ground, base, sof, info, authority |
| `asset`, `service`, `role`, `limitation` | As in `scenario/data/assets.csv` |
| `core_function` | AFDP 3-0 core function for Air Force assets (AS, GPA, RGM, GISR, C2) |
| `parts`, `part_asset` | For an asset spread over several zones: one counter per part (`RULES.md` §4.5) |
| `visibility` | `hidden` marks an asset that makes a good hidden counter |
| `cell` | The cell preset that usually owns it; used when the team has that cell |
| `arrives`, `approval` | A typical arrival and approval when the asset is in an RFF pool |
| `notes` | A hint for the designer |

```bash
python3 tools/presets.py add-asset redfor f22 kc46 --zone Z6
python3 tools/presets.py add-asset redfor b2 --availability home --zone Z1 --visibility hidden
python3 tools/presets.py add-asset bluefor patriot@rff arms-transfer@rff
python3 tools/presets.py add-asset bluefor ace --zone "Z10;Z11;Z12"
```

`add-asset` gives each asset the team's next free ID (01–29 for forces at start or at home, 30–49 for the RFF pool; free-text RFFs on the day start at 50, `RULES.md` §5), adds its row to `scenario/data/assets.csv` and to the matching table in `scenario/<side>-packet.md`, and prints the order of battle row to paste. `key@rff` (or `@home`, `@start`) sets the availability for one asset. Then set the zones, rewrite the role and limitation in the scenario's words, and run `python3 tools/check_assets.py && python3 tools/make_counters.py`.

The `authority` category holds RFF items that aren't units: authority to strike the enemy's homeland, sanctions, an arms package, aid. They go in an RFF pool and on the placement form, not on the map.

## 4. Tracks

| Key | Track | Scale | Fits |
| --- | --- | --- | --- |
| `opinion` | International Opinion | −3 to +3 | Almost every scenario |
| `will` | [NATION] Domestic Will | 0 to 5 | A team far from home; copy it for each team that needs one |
| `stability` | [NATION] Regime Stability | 0 to 5 | A government under pressure |
| `access` | Sea Lane Access | Open / Restricted / Closed | A strait or shipping lane |
| `escalation` | Escalation | Crisis to Regional war | Any scenario where going too far should be feared |
| `consent` | Host Nation Consent | Full / Limited / Revoked | A team fighting from another country's bases |
| `cohesion` | Coalition Cohesion | 0 to 5 | A coalition, or a GREENFOR partner |
| `humanitarian` | Humanitarian Situation | Stable to Catastrophe | A population in the fighting |
| `economy` | [NATION] Economic Pressure | 0 to 5 | Sanctions, trade, or energy as weapons |
| `talks` | Negotiations | No contact to Agreement | A negotiated objective |
| `info` | Information Advantage | −3 to +3 | Narrative and deception |

`python3 tools/presets.py add-track escalation talks` copies them into `game.toml` `[[track]]`. Rewrite each name and trigger for the scenario ([TEAM] and [NATION] are placeholders), describe the tracks in `scenario/00-overview.md` §5.1 and the Scenario Brief §5, and keep to three to five (`DESIGN-GUIDE.md` §2.5). Two tracks can't share an `id`, so give a copied `will` track a new one (`will-red`).

## 5. Scenario elements

`scenario-elements.md` holds patterns to adapt by hand: inject archetypes, starting-condition archetypes, objective patterns, intelligence product formats, and run-of-show options for shorter events and three teams.

## 6. Adding your own presets

The presets are plain files: add a row to `assets.csv`, or an entry to a `.toml` file, with a new `key`, and the tool picks it up. Keep them generic (no scenario names), keep every asset a real U.S. system with a limitation, and run `python3 tools/presets.py reference --write` after changing `assets.csv`. A preset you build for one scenario and want to keep belongs back in the base repository.
