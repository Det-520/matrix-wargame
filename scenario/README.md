# [Scenario name] — Scenario Index

**Owner:** [designer] · **Version:** 0.1 ([date])

The scenario is split by **audience**, so a team packet is just a set of files and nothing has to be cut out by hand. The rules are in `RULES.md`, and the event logistics are in `EVENT-SETUP.md`. `DESIGN-GUIDE.md` walks through building a scenario from these templates, in order.

## Files

| File | Contents | Every team | That team only | White cell |
| --- | --- | :---: | :---: | :---: |
| `00-overview.md` | BLUF, background, map and zones, actors, tracks, starting conditions, timing, ROE | ✅ | | ✅ |
| `<team id>-packet.md`, one per `game.toml` `[[side]]` (here: {% for s in sides %}{{ s.id }}{% if not loop.last %}, {% endif %}{% endfor %}) | That team's forces (incl. hidden), RFF pool, intel estimate, secret objectives | ❌ | ✅ | ✅ |
| `whitecell-injects.md` | Kickoff inject, inject pool, notes on white-cell actors | ❌ | ❌ | ✅ |
| `whitecell-ground-truth.md` | The truth behind each team's intel estimate, scoring notes, objective status card | ❌ | ❌ | ✅ |
| `data/assets.csv` | Every counter as one row, for printing counters and checking consistency | ❌ | ❌ | ✅ |

The packets ship as `redfor-packet.md` and `bluefor-packet.md`. A team added in `game.toml` gets its own, copied from one of them (`DESIGN-GUIDE.md` §2.1).

`data/assets.csv` mirrors the force tables in the team packets. **The packets are the source of truth.** After editing a force table, update the CSV and run `python3 tools/check_assets.py` to confirm the two still match. Then run `python3 tools/make_counters.py` to rebuild the printable counters (`handouts/whitecell/counters.pdf` for every team, plus one sheet per team in `handouts/<team id>/`).

**The templates hold example rows** (a few real U.S. systems for each default team) so the tools run on a fresh copy. Replace them with the scenario's forces.

## Building team packets (≥ 24 h before the event)

The printable documents are in `handouts/`, and the distribution list is in `handouts/whitecell/handbook.md` §2.1. The table below lists the design files they come from.

| Packet | Contents |
| --- | --- |
| **Common (every team)** | `RULES.md` (the Quick-Start, `RULES.md` §1, first), `scenario/00-overview.md`, `references/doctrine/AFDP_3-0_One_Pager.pdf`, `references/doctrine/AFDP_5-0_One_Pager.pdf`, `references/doctrine/AFDP_1-1_Placemat.pdf` |
| {{ team_rows("**{label}** | Common + scenario/{id}-packet.md + handouts/{id}/intel/ (and handouts/{id}/cells/ if the team has cells)") }} |
| **White cell** | Everything |

## Open decisions (scenario)

| ID | Decision | Draft assumes |
| --- | --- | --- |
| S1 | Final wording of the {{ word(3 * n_teams) }} secret objectives (the objectives section of each team packet) | [as drafted] |
| S2 | Map distances and zone layout (`00-overview.md` §3) | [as drafted] |
| S3 | Kickoff inject wording, and who "fires first" | `whitecell-injects.md` §1 |
| S4 | Balance check: each team's counters against the others', plus the weaker team's advantages | Needs a POC run-through |
| S5 | The intelligence products ({% for s in sides %}{{ s.prefix }}I-xx{% if not loop.last %}, {% endif %}{% endfor %}) and their key: whether the hints at hidden assets and objectives are too strong or too weak | [as drafted] |
