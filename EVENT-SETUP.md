# Event Setup — [Event name]

**Owner:** [designer]
**Date of event:** [date]
**Version:** 0.1 (draft, [date])

This document covers **the event that hosts the game**: schedule, rooms, groups and teams, flight commanders, POC staffing, evaluation, materials, and risks. The game mechanics are in `RULES.md`. The scenario is in `scenario/` (index: `scenario/README.md`). Status tags (**[CANON]**, **[PROPOSED]**, **[OPEN]**) work as defined in `RULES.md` §0.

**In the base.** The schedule, staffing, and materials below are what the first game built on this base used for a 3-hour AFROTC LLAB with four tables of 9–10 cadets. Keep what fits your event and change the rest. If you change the turn count or block lengths, change `game.toml` `[turns]` and the timer program's `BLOCKS` (`tools/whitecell-clock.html`) to match.

---

## 1. Purpose

### 1.1 Outcomes

- Improve leadership skills:
  - planning a COA
  - decision making
  - communication within teams
  - briefing, giving reasoning for decisions, and defending them
  - creativity
- Learn Air Force doctrine.
- Learn DAF assets.

### 1.2 Training objective

**[Objective number and title]** (`references/training-objective.txt`). Its performance measures:

- [measure]
- [measure]

The LLAB objective this base was built for, 1.3 *Apply wargaming principles to analyze and solve a tactical problem*, is in `references/training-objective.txt` with its performance measures. §7 maps them to what evaluators can observe.

### 1.3 Why a matrix wargame

- It is a different style from previous leadership projects, so it demands different thinking.
- It puts less weight on puzzles, math, and trivia, and more on sound decision making, argumentation, and a broad understanding of America's defense capabilities.

---

## 2. Before the event (homework)

**Due at least 24 hours prior.**

- Teams and flight commanders (both Phase I–II and Phase III–IV) are assigned (§4).
- Each player receives the **common player documents**: `handouts/common/rules-handbook.md` (especially `rules-handbook.md` §1, How to play), `handouts/common/scenario-brief.md`, `handouts/common/scenario-schedule.md`, `handouts/common/player-forms.md`, and the doctrine one-pagers. Players are expected to arrive knowing how to play.
- Each player receives the **team-specific documents and intelligence products** for their side (`handouts/redfor/` or `handouts/bluefor/`: Commander's Read-Ahead, Team Packet, Order of Battle, and every intelligence product in `intel/`), so they can read and weigh the intelligence before Phase I begins.
- **[PROPOSED] Release schedule.** The build sorts the PDFs into release folders by when they go out: `Common Matrix - ASAP RELEASE` (rules and forms, as soon as teams are set), `Common Scenario - 1WK RELEASE` (the public scenario, a week out), and each side's `24H RELEASE` (secret documents, 24 hours out).
- **[PROPOSED] Slack.** The designer creates the channels and sends the invitations with the team assignments. Every player joins their **group channel** (public, both teams) and their **team channel** (secret) before the event (`RULES.md` §2.5). Slack is the written record: COAs and Cons go in the group channel, requests and secret COAs in the team channel. Briefs are still given aloud. Every player may bring a laptop; each team needs at least one signed in at the table.

---

## 3. Schedule

Times below are the first game's, kept as an example of a 3-hour block that fits 7 turns. Replace them with your event's.

The game blocks (Phase I through Debrief 2) come from the run of show in `game.toml` (`[schedule]` `start`, `[[block]]`, `[[turn_step]]`; `RULES.md` §2.1). Set the structure and the minutes there, then print the game's rows with clock times to copy into this table:

```bash
python3 tools/schedule.py            # the players' table; add `whitecell` for the white cell's
```

The timer program and the schedule tables in the Scenario Schedule and the White Cell Handbook follow `game.toml` on the next build. The rows around the game (door checks, formation, transit, closing) are the event's and stay here.

| Start | End | Event (min) | Location | Intensity |
| --- | --- | --- | --- | --- |
| 1325 | 1335 | Door checks (10) | [place] | 3 |
| 1335 | 1340 | Formation (5) | [place] | 3 |
| 1340 | 1345 | Transit to game rooms (5) | — | 3 |
| 1345 | 1403 | **Phase I – Planning** (18) | Group rooms (§5) | 3 |
| 1403 | 1405 | **Kickoff inject** (2) | Group rooms (§5) | 3 |
| 1405 | 1505 | **Phase II: Turns 1–4** (60) | Group rooms (§5) | 3 |
| 1505 | 1512 | Debrief 1 (7) | Group rooms (§5) | 2 |
| 1512 | 1520 | **Phase III – Planning and FRAGO** (8) | Group rooms (§5) | 3 |
| 1520 | 1605 | **Phase IV: Turns 5–7** (45) | Group rooms (§5) | 3 |
| 1605 | 1612 | Debrief 2 (7) | Group rooms (§5) | 2 |
| 1612 | 1617 | Transit (5) | — | 3 |
| 1617 | 1625 | Closing remarks (8) | [place] | 2 |

### Event notes

- **Phase I (18 min):** teams organize their staff, synthesize pre-read intel, and build a plan. Up to **4 requests (RFIs/RFFs combined)** are due in Slack at **minute 12** so the lead adjudicator can answer them while teams rehearse and brief. In the last 3 minutes, each team briefs its plan and up to 3 planned COAs to its logger (the five-paragraph OPORD format is a reference, not a requirement) (`RULES.md` §2.3).
- **Kickoff inject (2 min):** the lead adjudicator reads the kickoff inject (`scenario/whitecell-injects.md` §1), and the loggers post Phase I RFI answers and RFF rulings in each team channel.
- **Phase II (60 min):** 4 full turns of 15 minutes each (`RULES.md` §2.2).
- **Debrief 1 (7 min):** led by the Phase I–II flight commander. Afterward, the **Phase III–IV flight commander** takes over (§4.2).
- **Phase III – Planning and FRAGO (8 min):** teams plan under the new flight commander. In the last minute, the new flight commander gives a **1-minute oral FRAGO** to the logger with updated Commander's Intent and up to 2 new planned COAs for Phase IV (`RULES.md` §2.4).
- **Phase IV (45 min):** 3 full turns.
- **Debrief 2 (7 min):** led by the Phase III–IV flight commander after the white cell announces the end state and scores objectives.
- The debrief and unstructured planning blocks are deliberately flexible, so they can absorb overruns.

---

## 4. Groups, teams, and flight commanders

### 4.1 Groups and teams

- **[N] groups** of 9–10 players each. Each group plays its **own separate game** at its own table. Set `game.toml` `tables` to the number of groups.
- **2 teams per group**, one REDFOR and one BLUEFOR, of 4–5 players each, named Alpha, Bravo, and so on.
- Small teams are deliberate: they keep every member engaged for the whole event and give evaluators more to observe.

### 4.2 Flight commanders

- Each team gets **one assigned flight commander for Phases I and II** and **a different assigned flight commander for Phases III and IV**. The handover happens after Debrief 1, and the Phase III–IV flight commander briefs a 1-minute FRAGO before Turn 5.
- **Only the flight commander is assigned.** During Phase I, each team decides its own structure (who handles operations, intel, logistics, briefing, and so on).

---

## 5. Room setup

- **One group per room.** Each group plays in its own room, at one table arranged so its two teams and white cell sit in a circle. The group's public Slack channel is named for its room (`RULES.md` §2.5).

| Group | Room | Teams | Group channel |
| --- | --- | --- | --- |
| 1 | [room] | Alpha (REDFOR), Bravo (BLUEFOR) | `[prefix]-group1-[room]` |
| 2 | [room] | Charlie (REDFOR), Delta (BLUEFOR) | `[prefix]-group2-[room]` |

- **[PROPOSED] Devices.** The lead adjudicator shows the timer and dice program on the room's TV or projector, where every player can see it, running it on the room computer where one is connected to the screen and on a laptop otherwise. Each logger keeps the white cell site and Slack open on a laptop turned away from the players. `handouts/whitecell/table-setup.md` has the devices, table layout, and counter placement.
- **[PROPOSED] No room leads.** Each group's white cell sets up its own room before the event and puts it back afterward.

---

## 6. POC staffing

| Role | Count | Job |
| --- | --- | --- |
| White cell lead adjudicator | 1 per group | Timekeeper (timer program), inject-giver, dice program, final adjudication (`RULES.md` §9.2) |
| BLUEFOR action logger | 1 per group | Receives the BLUEFOR Phase I brief and Phase III FRAGO. Keeps the BLUEFOR placement form (`RULES.md` App. B). Watches BLUEFOR's team channel and posts the white cell's answers. Doesn't log every move. |
| REDFOR action logger | 1 per group | The same for REDFOR |
| Evaluator | 1 per team | Observes one team (§7) |
| Extras | as available | |

**[OPEN]** Confirm POC availability: at least 5 per group before extras.

---

## 7. Evaluation [PROPOSED]

Evaluators can tie their observations to the training objective's performance measures. These rows fit LLAB objective 1.3; adjust them to your objective.

| Performance measure | Where to observe it |
| --- | --- |
| Develop a viable COA | The Phase I plan, Phase III FRAGO, and each turn's COA. Is it feasible, acceptable, suitable, distinguishable, and complete (AFDP 5-0)? |
| Construct a clear, concise OPORD | The oral Phase I brief and the Phase III FRAGO brief to the logger (`RULES.md` App. A) |
| Execute the COA while justifying decisions | Quality of Pros, Cons, and briefing delivery |
| Modify the plan in response to the adversary or injects | When a planned COA was invalidated, did the team notice and adapt (especially in the Phase III FRAGO)? |
| Articulate lessons learned | Debrief contributions |
| Leadership | Team communication, how the team organized itself in Phase I, inclusion of all members, flight commander decisions, time management |

---

## 8. Tools and materials

- **Dice:** a computer program rolls 2d6 for adjudication (`tools/whitecell-clock.html`). No physical dice.
- **Timekeeping:** the same program runs the turn clock (`RULES.md` §2.2).
- **Print Packet:** `build/White Cell/Print Packet - One Table.pdf` holds everything one table prints (checklist, White Cell Forms, starting-condition cue cards, counters, map tiles, both teams' player forms and slips, and spares at the back), with a cover listing it. Print one per group. `Print Packet - One Table, Reference Forms.pdf` holds one copy of each player form per side and no spares, to photocopy from. Print the game pieces in colour and the forms in greyscale.
- **Map:** `build/Common Scenario - 1WK RELEASE/map-full.pdf` (one sheet, for a plotter) or `map-tiles.pdf` (letter tiles to trim and tape). See `map/README.md`.
- **Counters:** `python3 tools/make_counters.py` builds them from `scenario/data/assets.csv` (the build runs it). Print at 100% scale, in colour, on card stock if available, and cut along the gray lines. The white cell sheet shows hidden assets and has blank R-, B-, and X- counters for forces created during play (`RULES.md` §5). Never give a team the other side's sheet or the white cell sheet.
- **Tracks:** kept in the timer and dice program's tracker on the room's screen, not on paper.
- **Slack:** one public channel per group and one secret channel per team (`RULES.md` §2.5).

---

## 9. Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| The POC have never run a game of this type | Prepare well in advance: good pre-event information, POC (especially the white cell) who know the capabilities, and **POC run-throughs** of the game. |
| **Going over time** | Turns are cut to 15 minutes (or the turn length set in `game.toml`), with padding between phases. Shorten Prepare, never the Cons (`RULES.md` §8.4). |
| Players struggle with the rules at first | Rules go out early with a one-page quick-start. The worked example is in `RULES.md` §10. |
| Slack or the network fails during play | Teams write the same posts on the backup paper slips in the Print Packet and hand them to the white cell (`RULES.md` §2.5). |
| Tables drift apart in how generously they rule | The lead adjudicators agree on auto-success and COA size beforehand (`RULES.md` §8.5) and can check with each other by Slack during play. |
| Players act outside reasonable bounds | The white cell bounds behavior at its discretion. It can kill actions or issue injects that restrict behavior, e.g. a new national directive (`RULES.md` §8.4, the bounding inject in `scenario/whitecell-injects.md`). |
