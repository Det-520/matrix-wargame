---
title: "Operation Example — Table Setup Guide"
subtitle: "Devices, table layout, and where every counter starts · [Event] · [Date]"
short: "Table Setup Guide"
---

**WHITE CELL ONLY.** This guide places the hidden counters, so keep it with the white cell. Set the room up before the event: the white cell may have no time between arriving and the Phase I opening script. Everything here comes from the White Cell Handbook §2.3 and the Master Asset List; if they ever disagree, the Master Asset List wins.

## 1. Devices

{{ Both }} teams need to see the map, the ongoing-effects sheet, the cue cards, and the screen, which shows the tracks. No player should be able to see a logger's laptop or forms.

| Device | Who runs it | What is on it | Where |
| --- | --- | --- | --- |
| **Room computer and TV or projector** | Lead adjudicator | The timer and dice program (`whitecell-clock.html`), on the Phase I block. Its tracker is the only track board: there is no paper one. Many rooms have a computer already connected to the TV or projector: use it. Copy the file onto it (USB drive or download) before the event. The program needs no network. | Where every player can see it. Test it before the event. |
| **Lead adjudicator's laptop** | Lead adjudicator | Only if the room has no computer connected to the screen: connect it to the TV or projector and run the program on it. Keep nothing else open on the shared screen. | With the lead adjudicator |
| {{ team_rows("**{label} logger's laptop** | {label} logger | The white cell reference site and Slack: the group channel and {label}'s team channel | Screen turned away from the teams. The site shows every team's secrets.") }} |
| **Players' laptops** | Any player | Slack (the group channel and the player's own team channel), plus anything players want to search online. Every player may bring one. | With the team |

## 2. Where everything goes on the table

| Item | Where | Face | Kept by |
| --- | --- | --- | --- |
| Map (letter tiles taped together, or the plotter sheet) | Middle of the table | Up | Table |
| Ongoing effects and big projects sheet (White Cell Forms §2) | Beside the map, where {{ both }} teams can see it | Up | Lead adjudicator |
| Starting-condition cue cards (one per {% for s in sides %}S-{{ s.prefix }}x{% if not loop.last %}, {% endif %}{% endfor %}) | Beside the map, standing or flat | Up | Table |
| Visible counters | On the map by zone (§4) | Up | Each team's logger |
| Hidden counters (§5) | In the envelope | Hidden | Lead adjudicator |
| Blank counters ({% for s in sides %}{{ s.prefix }}-, {% endfor %}grey X-) | Beside the lead adjudicator | — | Lead adjudicator |
| Objective status card (White Cell Forms §3) | With the {{ sides[-1].label }} logger | **Down** | {{ sides[-1].label }} logger |
| {{ team_rows("{label} placement form (White Cell Forms §4) | With the {label} logger | **Down** | {label} logger") }} |
| Score sheet (White Cell Forms §1) | With the lead adjudicator, until the end of the game | **Down** | Lead adjudicator |
| White Cell Checklist | With the lead adjudicator | — | Lead adjudicator |
| Each team's player forms (OPORD format, COA and Cons worksheets, request {% if rules == "full" %}and secret COA {% endif %}slips) | With that team | — | The team |
| Spare forms and slips | With the white cell | — | Any logger |

Never put the objective status card or a placement form beside the ongoing-effects sheet: they show what the secret objectives look for.

> **TEMPLATE.** Sections 3 to 7 list the scenario's own tracks and counters. Fill them in from `scenario/00-overview.md` §5 and the Master Asset List once the forces are settled; the rows below are the example assets in `scenario/data/assets.csv`. Count the counters per zone from the CSV, and count each part of a split counter (B-07a, b, c) separately.

## 3. Track starting positions

Set these in the tracker on the timer and dice program (**Reset to start** sets them all).

| Track | Start | Changes at |
| --- | --- | --- |
| [Track] | **[start]** | [e.g. moves to Restricted when you read the kickoff inject] |
| [Track] | **[start]** | |

The ongoing-effects and big-projects sheet starts empty.

<!-- pagebreak -->

## 4. Visible counters on the map

Z1 [Red nation] is an off-map box. [Say where each off-map box sits on the map, and list the zones that start empty.]

> **FORMAT NOTE (delete before printing):** one subsection per team, in the order of `game.toml` `[[side]]`, numbered to match the setup checklist (§7). A team added in `game.toml` needs its own subsection here and its rows in §5.

### 4.1 BLUEFOR: [n] counters

| Zone | Counter | Asset |
| --- | --- | --- |
| **Z10 [Blue coast]** | B-04 | Patriot battalion (PAC-2) |
| | B-07a | Early-warning radar site |
| **Z11 [Blue capital]** | B-01 | F-16C/D Fighting Falcon squadron |
| | B-07b | Early-warning radar site |
| **Z12 [Blue interior]** | B-07c | Early-warning radar site |

### 4.2 REDFOR: [n] counters

| Zone | Counter | Asset |
| --- | --- | --- |
| **Z1 [Red nation]** (off-map box) | R-16 | B-52H Stratofortress (JASSM-ER/LRASM) |
| **Z6 [Red forward base]** | R-01 | F-35A Lightning II squadron |
| | R-05 | KC-46A Pegasus tanker detachment |

<!-- pagebreak -->

## 5. Hidden counters: [n], in the envelope

Hidden counters stay in the envelope with the lead adjudicator. They are not on the map, and the teams do not see them. Each goes on the map only when it is **found** by a successful ISR COA, **used** by its owner (naming it in a COA or argument reveals it, whatever the roll), or **disclosed** by an inject (Handbook §2.3).

| Side | Counter | Asset | Where it really is |
| --- | --- | --- | --- |
| REDFOR | R-18 | B-2A Spirit | Z1 [Red nation] |
| BLUEFOR | B-09 | Harpoon coastal-defense battery | Z10 [Blue coast] |

If a team chooses where a hidden counter starts, its logger writes the zone on the placement form during the team's Phase I brief. A split hidden counter is revealed one part at a time.

## 6. Counters that come later

- **RFF arrivals** go on each team's main base zone (**Z6** for REDFOR, **Z11** for BLUEFOR, outside support included) unless the RFF names another destination (Handbook §7). Keep the RFF counters (R-30 and up, B-30 and up) off the map, beside the lead adjudicator, until one arrives.
- **Blank counters** are for a force with no printed counter: {% for s in sides %}{{ s.prefix }}-{% if not loop.last %}, {% endif %}{% endfor %} for free-text RFFs (number them from {% for s in sides %}{{ s.prefix }}-50{% if not loop.last %}, {% endif %}{% endfor %}) and grey X- for forces an inject creates (from X-01). Write the ID and zone on it (Rules §5).

<!-- pagebreak -->

## 7. Setup checklist

### Room and devices

- [ ] TV or projector on and showing the timer and dice program, on the **Phase I** block, visible to every player. Use the room computer if one is connected to the screen; otherwise the lead adjudicator's laptop.
- [ ] Each logger's laptop open to the white cell site and Slack (the group channel and its team's channel), screen turned away from the teams.
- [ ] Each team has at least one laptop that can post in its group and team channels. Players may use their laptops to search online too.

### Map, tracks, and cue cards

- [ ] Map in the middle of the table.
- [ ] Tracker on the timer and dice program at the starting values (§3).
- [ ] Ongoing effects and big projects sheet beside the map, blank.
- [ ] Cue cards face up beside the map: [S-R1 … S-B*n*].

### Counters

- [ ] Each logger placed its team's visible counters (§4): {% for s in sides %}**[n]** {{ s.label }} (§4.{{ loop.index }}){% if not loop.last %}, {% endif %}{% endfor %}.
- [ ] **[n]** hidden counters in the envelope with the lead adjudicator (§5). None on the map.
- [ ] RFF counters and blank counters set aside with the lead adjudicator (§6).

### Paper

- [ ] Each logger: its team's placement form, face down. The {{ sides[-1].label }} logger also has the objective status card, face down.
- [ ] Lead adjudicator: the White Cell Checklist and the score sheet, face down.
- [ ] Each team's stack of player forms with the team. Spares with the white cell.

### Last look (before Phase I)

- [ ] Nothing white-cell-only is where a player can see it: no counter sheet, no hidden counter, no placement form, no open laptop screen.
- [ ] Phase I opening script ready (Handbook §3.1). Start the timer when you finish reading it.
