# Scenario Elements — Patterns to Adapt

**Audience:** designer. Generic patterns, with no scenario in them. Copy one into a scenario file and rewrite it there; once it is in `scenario/` or `handouts/`, the secrecy rules of that file apply (`AGENTS.md` rule 2).

The base's own templates already hold a starting set: thirteen generic injects in `scenario/whitecell-injects.md` §2, and an example of every other element. This file adds more to choose from, with a few written for games with three or more teams or with cells. [TEAM], [NATION], [ZONE], and the like are placeholders; replace them all before a release (`DESIGN-GUIDE.md` §5).

## 1. Injects

Give a copied inject the next free I-xx number in `scenario/whitecell-injects.md` §2 and in the White Cell Intelligence and Injects. Each one should read aloud in 30 seconds, have a purpose, and name the turns it fits (`DESIGN-GUIDE.md` §2.10).

| Inject | Purpose | Fits |
| --- | --- | --- |
| **Ammunition shortfall**: [TEAM]'s precision munitions run low. −1 to its next strike COA unless a resupply RFF is approved this turn. | Rewards logistics planning; gives a logistics cell a voice | Turn 4–5, after heavy strike use |
| **Runway cratered**: [BASE] can't launch for one turn while engineers repair it. A successful repair COA ends it at once. | Tests basing and Agile Combat Employment | After any strike on a base |
| **Press finds the hidden unit**: a journalist photographs [a hidden asset] and publishes it. The counter goes on the map. | Fog of war cuts both ways | When a team has leaned on one hidden asset |
| **Allied election**: [a partner]'s government faces a vote and asks for a pause in offensive operations for one turn. | Coalition friction; the cost of partners | Turn 3–5 |
| **Third-party ultimatum**: [a neutral state] demands that all forces leave [ZONE] within one turn, or it closes its airspace. | Brings a white-cell actor into play | When fighting spreads near a neutral |
| **Refugee flow** from [ZONE] toward [a neighbor]. The Humanitarian Situation worsens by one unless a team's next COA addresses it. | Consequence management (`RULES.md` §7) | After strikes near cities |
| **Insurance markets close [the chokepoint]**: commercial shipping stops whatever the navies do. | Shows economic effects outrun military ones | When the sea lane is contested |
| **Communications outage** inside [TEAM]: for one turn its cells can't reach the commander; each cell lead decides alone for its own counters, and the team still makes one COA. | Tests mission command and cells (`RULES.md` §9.4) | Teams with cells, Turn 3–5 |
| **Leak from a cell**: one of [TEAM]'s cell plans appears in the press. The white cell reads a sentence of it aloud. | Operational security; tension inside a team | Teams with cells, when a cell has a pet plan |
| **Sponsor cuts off support**: [the armed group]'s sponsor halts arms shipments unless the group stops attacks on [TARGET]. | Pulls a non-state team between its cause and its patron | A YELLOWFOR team, mid-game |
| **Host nation demands a say**: [the host] insists on approving each strike from its territory. Until a team wins its consent, strikes from its bases need an RFF. | Makes host-nation consent a live issue | A GRAYFOR team or a host-nation actor, Turn 2–4 |
| **Backdoor offer**: [an outside power] privately offers each team the same deal. Every team learns of its own offer only. | Tests trust among three or more teams | Three or more teams, Turn 3–5 |
| **Separate peace rumor**: reports say two of the teams are close to a deal without the third. | Pressure to talk; tests alliances | Three or more teams, Phase III |

## 2. Starting conditions

Starting conditions are standing ±1 modifiers with a stated way to remove them (`DESIGN-GUIDE.md` §2.5). Give each team two or three, each one an obvious target for another team's COA. Number them S-*prefix*1, S-*prefix*2 … in `scenario/00-overview.md` §5.2 and `handouts/common/starting-conditions.md`.

| Pattern | Effect | Removed by |
| --- | --- | --- |
| **Long supply line** | −1 to sustained operations far from home | A successful COA that opens a closer base or port |
| **Single main base** | −1 to every air COA in the turn after the base is struck | Dispersal (a big project of up to three COAs) |
| **Home ground** | +1 to defensive COAs in home zones | Losing control of the zone |
| **Popular support** | +1 to COAs that rely on the population (information, hiding forces, recruitment) | A strike that causes civilian harm, or a successful information COA against it |
| **Restrictive rules of engagement** | Strikes on [a target set] are ruled impossible | An approved RFF for the authority |
| **Divided government** | −1 to big RFFs; Domestic Will drops faster | A visible success, or a successful information COA at home |
| **Untested coalition** | −1 to COAs that use a partner's forces | A successful COA that builds the coalition (consultation, a combined exercise) |
| **Air superiority over home** | +1 to air defense of home zones | A successful offensive counter-air COA |
| **Surprise held** | The first COA using a hidden asset gets +1 | Revealing the asset |
| **Sanctions bite** | −1 to RFFs for new equipment | A trade deal, or a third party breaking the sanctions |
| **Host nation reluctant** | Combat operations from [the host]'s bases need an RFF each time | A diplomatic COA that wins consent (Host Nation Consent track) |
| **Weapons stockpile low** | −1 to a second strike COA in a row | A resupply RFF |

## 3. Objectives

Three secret objectives a team, each scorable as achieved, partial, or not achieved (`DESIGN-GUIDE.md` §2.7). Write the objective so it reads well with an exclamation mark and put the scoring detail in the criteria.

| Pattern | Example | Opposed by |
| --- | --- | --- |
| **Hold or take a zone** | "Keep [ZONE] in our hands!" | A team that wants the zone |
| **Keep a track in a range** | "Keep the sea lane open!" (Access never Closed for two turns running) | A team that gains from closing it |
| **Protect a force** | "Bring the fleet home!" (no more than one ship counter destroyed) | Any team that can strike it |
| **Win a third party** | "Win [the neutral]'s support!" (basing granted, or Opinion +2 or better) | The team courting the same neutral |
| **Negotiated outcome** | "Get a ceasefire on our terms!" (an agreement that includes [term]) | Reachable by a deal both sides can accept |
| **Long-term position** | "Come out stronger than we went in!" (a new base, treaty, or partner by game end) | Makes a team that plays only for the next turn pay (Mouat) |
| **Limit the war** | "Keep the war off our soil!" (no strikes on [home zones]) | A team that needs to strike there |
| **Survive** (non-state or weak team) | "Still standing at the end!" (leaders not captured, at least one zone held) | Both main teams |
| **Separate gain** (coalition partner) | "Get our own guarantee!" (an agreement that names us, not only our ally) | Pulls against its own ally's end state |

With three or more teams, give each team one objective opposed to each of the others, and at least one that needs a deal with one of them.

## 4. Intelligence products

Ten to fifteen a team, mixing true, misleading, and irrelevant reports in different formats (`DESIGN-GUIDE.md` §2.9, `references/tongue-and-quill-summary.md` §6). Formats that work:

| Format | Voice | Good for |
| --- | --- | --- |
| Imagery report | Terse, measured, with an analyst's assessment | Hinting at a hidden asset by its size or shape |
| Intelligence information report (HUMINT) | Source description, then what the source said, then comments | Intentions; a source who may be lying |
| Signals intercept summary | Fragments, times, call signs | Confirming or denying a capability |
| Diplomatic cable | An ambassador's judgment, polite and hedged | A third party's real price |
| Press clipping or social media post | Unverified, emotional | Public opinion; deliberate disinformation |
| Open-source analyst blog | Confident and sometimes wrong | An overestimate the white cell's ground truth corrects |
| Logistics status report | Tables and shortfalls | The team's own limits, so players plan around them |
| Liaison officer's note | Informal, from a partner's headquarters | What a partner or host nation will and won't do |

## 5. Run of show

The run of show lives in `game.toml` (`[[block]]` and `[[turn_step]]`; `DESIGN-GUIDE.md` §2.1). The timer program's **Setup** dialog is the quickest way to try one of these: change the turns and minutes, watch the totals, and **Copy as game.toml**. Mouat recommends at least six turns. Renaming or removing a phase means updating the handouts that name it (`DESIGN-GUIDE.md` §2.1 lists them); changing only turns and minutes needs nothing else.

### 5.1 The default (about 2½ hours of play)

Four phases and 7 turns of 15 minutes, with a handover of flight commanders between Debrief 1 and Phase III. This is the game as first played, and what the documents are written for.

### 5.2 Two hours

Keep the four phases. Play 3 turns in Phase II and 3 in Phase IV, cut Phase I to 12 minutes (9 planning, 1 rehearsal, 2 briefs), shorten the debriefs to 5 minutes, and shorten Prepare to 4 minutes (14-minute turns). About 1 hour 56 minutes. Then reread the `say` scripts of the Phase I steps, which name their minutes in words.

```toml
# Phase I [[block.step]]s: min = 9, then min = 1, then min = 2
# [[block]] tag = "P2": turns = 3        [[block]] tag = "P4": turns = 3
# [[block]] tag = "D1" and "D2": min = 5
# [[turn_step]] id = "prep": min = 4
```

### 5.3 About 100 minutes, one commander

No handover: Phase I, the kickoff, one block of 6 turns, and one debrief. Shorten Prepare to 3 minutes (13-minute turns). About 98 minutes. This removes Phases III and IV and the first debrief, which the documents name and quote (`blocks.P3`, `blocks.P4`, `blocks.D1`): `python3 tools/schedule.py --check` names each place to change, and the Scenario Schedule, the White Cell Checklist, the forms' planned-COA rows, the Rules Handbook, and the Basic Rules need their phase descriptions rewritten.

```toml
[[block]]
tag = "P1"
short = "Phase I"
name = "Phase I – Planning"
  [[block.step]]
  name = "Team planning & requests"
  min = 8
  who = "All teams"
  requests_due = true
  [[block.step]]
  name = "OPORD briefs"
  min = 2
  who = "Teams → loggers"

[[block]]
tag = "KO"
short = "Kickoff"
name = "Kickoff inject"
  [[block.step]]
  name = "Kickoff inject"
  min = 2
  who = "White cell"

[[block]]
tag = "P2"
short = "Turns"
name = "Phase II"
turns = 6

[[block]]
tag = "D2"
short = "Debrief"
name = "End of game & debrief"
  [[block.step]]
  name = "End of game & debrief"
  min = 8
  who = "Flight commanders"
```

### 5.4 Three teams

A third team adds its COA step (2 minutes), its Cons step (1 minute), and a minute of resolve time, so a turn grows from 15 to 19 minutes (`RULES.md` §2.6). To stay inside the default 3-hour block, play 3 turns in Phase II and 3 in Phase IV (6 turns, about 2 hours 40 minutes), or shorten Prepare to 4 minutes and keep 4 and 3 (7 turns, about 2 hours 50 minutes). `python3 tools/presets.py add-team` adds the steps; change the turns yourself.

```toml
# [[block]] tag = "P2": turns = 3
# [[block]] tag = "P4": turns = 3
```
