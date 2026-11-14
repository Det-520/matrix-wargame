---
title: "Operation Example — White Cell Checklist"
subtitle: "Everything the white cell does, in order, from a week out to cleanup · [Event] · [Date]"
short: "White Cell Checklist"
---

**WHITE CELL ONLY.** The lead adjudicator keeps this checklist at the table and ticks it off. The *how* is in the White Cell Handbook; each line names the section. Clock times assume the {{ blocks.P1.start }} start (Handbook §3). If the start moves, the timer program keeps the durations.

## 1. Before the event

### One week out

- [ ] The ASAP release has gone to every player: {% if rules == "full" %}Player Rules Handbook{% else %}Basic Rules{% endif %} and Player Forms (Handbook §2.1).
- [ ] Release the scenario to every player: Scenario Brief, Scenario Schedule, Starting Conditions, and the map.
- [ ] Each table has a lead adjudicator and a logger for each team ({{ teams }}) (Handbook §1). Each team has an evaluator.
- [ ] A white cell run-through is on the calendar.

### 24 hours out

- [ ] Teams and both flight commanders for each team (Phases I–II and III–IV) are assigned.
- [ ] Email each team **only its own** release: {% for s in sides %}{{ s.label }} gets the “{{ s.folder }}” folder{% if not loop.last %}, {% endif %}{% endfor %}. **Nobody gets another team's documents.**
- [ ] Each white cell member is in their group's channel and {{ "both" if n_teams == 2 else "all " ~ word(n_teams) }} of its team channels (Handbook §2.4). The designer sends the invitations with the team assignments.
- [ ] Every white cell member has at least skimmed the Likely Plans guide, **every** team's intelligence products and the key (Intelligence and Injects §3), and the ground truth (Intelligence and Injects §1), and knows where to look things up in them during play. Nobody needs to know them by heart.
- [ ] Every white cell member has read the RFF pools (Handbook §7) and the scoring tables (Handbook §8).
- [ ] The timer and dice program (`whitecell-clock.html`) opens on the room computer connected to the TV or projector (or, if the room has none, the lead adjudicator's laptop), works offline, and shows on the screen.
- [ ] Each logger's laptop opens the white cell site and Slack.
- [ ] One Print Packet printed for each table (the full packet, or the Reference Forms version plus photocopies), game pieces in colour, forms in greyscale. Spares kept with the white cell. Counters and cue cards cut. Hidden counters in an envelope.
- [ ] Each table agrees with the others on what counts as an auto-success, so every table's game is scored alike (Handbook §5.1).

## 2. Table setup (before Phase I)

The Table Setup Guide has the devices, the table layout, every counter by name and zone, and a longer version of this list.

- [ ] Table arranged so {{ both }} teams and the white cell sit in a circle (EVENT-SETUP §5).
- [ ] Map down, with the ongoing-effects sheet (White Cell Forms §2) beside it where {{ both }} teams can see it.
- [ ] Tracker on the timer and dice program at the starting values (Table Setup Guide §3).
- [ ] Starting-condition cue cards face up beside the map: [S-R1 to S-R*n*, S-B1 to S-B*n*].
- [ ] **Visible** counters placed by zone: {% for s in sides %}[*n*] {{ s.label }}{% if not loop.last %}, {% endif %}{% endfor %} (Table Setup Guide §4). The **[*n*] hidden** counters stay in the envelope.
- [ ] Each logger has its team's placement form face down (White Cell Forms §4). The objective status card is face down with a logger (White Cell Forms §3).
- [ ] Each team has Slack open on at least one laptop and can post in its group and team channels. Every player may have a laptop, for Slack or to search online. Each logger has the white cell site and Slack (the group channel and its team's channel) open on a laptop turned away from the teams.
- [ ] Each team has its stack of player forms: OPORD format, COA and Cons worksheets, and the request {% if rules == "full" %}and secret COA {% endif %}slips (backup if Slack fails).
- [ ] Timer and dice program up on the TV or projector, on the Phase I block. Phase I opening script ready (Handbook §3.1).

## 3. Phase I: Planning ({{ blocks.P1.span }})

- [ ] **Minute 0** Read the Phase I opening script. Start the 18-minute timer.
- [ ] **Minute 12** Read the minute-12 call. Close requests: count up to **4** request posts in each team channel. Don't answer extras.
- [ ] **Minutes 12–18** Lead adjudicator writes the RFI answers and RFF rulings. Phase I RFFs count as Turn 1 (Handbook §7): an N+1 approval arrives, and can be used, on Turn 2.
- [ ] **Minutes 15–18** Each logger hears its team's oral OPORD brief and writes its **planned COAs** (up to 3, Turns 1–3) on the placement form.
- [ ] [If a team chooses the starting zones of any hidden counters in Phase I, its logger writes them on the placement form.]

## 4. Kickoff inject ({{ blocks.KO.span }})

- [ ] Read the kickoff inject aloud (Intelligence and Injects §4.1):

> "[The kickoff inject, word for word, from `scenario/whitecell-injects.md` §1.]"

- [ ] Set any tracks the kickoff inject moves.
- [ ] Loggers post the Phase I RFI answers and RFF rulings, with arrival turns, in threads in each team channel.

## 5. Every turn (Turns 1–{{ turns }})

Tick each box as you go. Turns {{ blocks.P2.turns }} are Phase II; Turns {{ blocks.P4.turns }} are Phase IV. Running behind? Shorten **Prepare**, never the Cons (Handbook §4.2).

<!-- mw:checkgrid -->

| Turn clock | Step | {{ turn_columns() }} |
| --- | --- | {{ turn_rule() }} |
| {{ clock(steps.prep.start) }} | Read the turn-start script. Start the timer. Last turn's RFI answers posted in the team channels? | {{ ticks() }} |
| {{ steps.prep.span }} | **Prepare.** Authorize parleys (≤ {{ parley }} min) on request; listen, repeat the deal back, logger notes it. | {{ ticks() }} |
| {{ clock(steps.prep.end) }} | Close requests: count up to **{{ requests }}** request posts per team. Don't answer extras. | {{ ticks() }} |
| {{ team_rows("{coa} | **{label} COA.** No interruptions. A later team may react to an earlier COA but not negate it. | " ~ ticks(), "coa") }} |
| {{ steps.pcons.span }} | **Prepare Cons.** Note the Pros you'll accept. | {{ ticks() }} |
| {{ team_rows("{cons} | **{label} Cons** (up to 3) | " ~ ticks(), "cons") }} |
| {{ clock(steps.res.start) }} | Check each COA: feasible? auto-success? Planned COA still valid (placement form)? (§5.1) | {{ ticks() }} |
| {{ clock(steps.res.start) }} | Count modifiers (cap ±4), roll 2d6, read the band, narrate. Interacting or opposed? (§5.3) Too contentious? {% if rules == "full" %}Estimative vote{% else %}Make the call{% endif %} (§5.5). | {{ ticks() }} |
| {{ clock(steps.res.start) }} | Hidden asset used or found? Reveal it and place the counter.{% if rules == "full" %} Secret COA trigger met? Resolve it now.{% endif %} | {{ ticks() }} |
| {{ clock(steps.res.start) }} | Rule on RFFs; give each one its arrival turn (§7). | {{ ticks() }} |
| {{ clock(steps.res.start) }} | State ongoing effects; write them on the ongoing-effects sheet (§6.3). | {{ ticks() }} |
| {{ clock(steps.res.start) }} | Inject? At most one (Intelligence and Injects §4.2). | {{ ticks() }} |
| {{ clock(steps.res.end) }} | Per-turn track effects applied? Any track at a trigger value? (§6.2) | {{ ticks() }} |
| {{ clock(steps.res.end) }} | [A starting condition that switches on at a set turn, e.g. "forward base not resupplied → S-R1's −1 applies from Turn 4."] | {{ ticks(first=4) }} |
| {{ clock(steps.res.end) }} | RFF arriving next turn (including N+1 approvals just made)? Announce it and place its counter (a blank counter if it has none); it can be used in next turn's COA. | {{ ticks() }} |
| {{ clock(steps.res.end) }} | Loggers: counters, tracks, placement forms, objective status card updated. | {{ ticks() }} |

<!-- pagebreak -->

## 6. Debrief 1 and handover ({{ blocks.D1.span }})

- [ ] Phase I–II flight commanders lead Debrief 1.
- [ ] Command passes to the **Phase III–IV flight commanders**.

## 7. Phase III: Planning and FRAGO ({{ blocks.P3.span }})

- [ ] **Minute 0** Start the Phase III timer. Teams plan Phase IV under the new flight commander.
- [ ] **Minute 7** Read the Phase III call (Handbook §3.1).
- [ ] **Minutes 7–8** Each logger hears the 1-minute oral FRAGO and writes **up to 2** new planned COAs for Turns 5–7 on the placement form.

## 8. Phase IV: Turns {{ blocks.P4.turns }} ({{ blocks.P4.span }})

- [ ] Run Turns {{ blocks.P4.turns }} with the grid in §5.

## 9. End of game and Debrief 2 ({{ blocks.D2.span }})

- [ ] Read the end-of-game script (Handbook §3.1).
- [ ] State the end state: every track, [the map facts the objectives check], any agreements (Handbook §8).
- [ ] Score {% for s in sides %}{{ s.prefix }}1–{{ s.prefix }}3{% if not loop.last %}, {% endif %}{% endfor %} as Achieved, Partial, or Not achieved. Check them against the scoring notes (Handbook §8).
- [ ] Fill in the score sheet (White Cell Forms §1).
- [ ] Phase III–IV flight commanders lead Debrief 2.

## 10. Cleanup

- [ ] Collect the hidden counters, the placement forms, the objective status card, and any backup paper slips that were used.
- [ ] Collect the intelligence products and team documents left on the table if you like. Once the game is over, it doesn't matter if another team sees them.
- [ ] Put the room back the way you found it.
