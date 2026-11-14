---
title: "Operation Example — Scenario Schedule"
subtitle: "Phases, timings, and planning for the event · [Event]"
short: "Scenario Schedule"
---

**Audience:** every player, REDFOR and BLUEFOR. Nothing in this document is secret. Released one week before the event, with the Scenario Brief.

**You are expected to arrive at the event having read, and knowing, everything in your read-ahead:** the {% if rules == "full" %}Player Rules Handbook{% else %}Basic Rules{% endif %}, the Scenario Brief, this Scenario Schedule, the Player Forms, and your team's documents. Your team's documents are secret, so don't show them to the other team.

*All countries, people, and events in this scenario are fictional. All military systems are real U.S. systems, described with unclassified, approximate capabilities.*

It is helpful to think of this document as an extension of the *Matrix Wargame — {% if rules == "full" %}Player Rules Handbook{% else %}Basic Rules{% endif %}* document with scenario-specific information.

## 1. Phases

### 1.1 Full Schedule

> **FORMAT NOTE (delete before printing):** The table is generated from the run of show in `game.toml` (`[[block]]`, `[[turn_step]]`, and `[schedule]` `start`). Change it there; the build fills it in. Section 1.2 and the text below it are written by hand (the numbers in them come from `game.toml` too), so keep the wording in step.

{{ schedule_table() }}

### 1.2 Summary of Phases

| Phase | Turns | What happens |
| --- | --- | --- |
| **Phase I – Planning** | none | Synthesize pre-read intel, plan, and file up to {{ planning_requests }} requests (due at minute {{ request_deadline }}). End by briefing your plan to your logger. **No COAs.** |
| **Kickoff inject** | — | The lead adjudicator announces the war has begun and returns Phase I request answers. |
| **Phase II** | Turns {{ blocks.P2.turns }} | Full turns |
| **Phase III** | — | Debrief 1, command handover to Phase III–IV flight commander, and a 1-minute oral FRAGO brief to your logger (§1.4). |
| **Phase IV** | Turns {{ blocks.P4.turns }} | Full turns |

Each turn is about {{ days(game_days) }}, so {{ turns }} turns cover about {{ days(game_days * turns) }} of conflict. The white cell keeps timelines realistic: moving forces across an ocean takes turns, not minutes (Scenario Brief §7).

### 1.3 Phase I – Planning

- You receive your intelligence products and team documents at least 24 hours before the event so you can read them in advance. During Phase I ({{ mins(blocks.P1.min) }}), decide how your team is organized, synthesize your intelligence, build a plan, and file requests to posture your forces before the war starts.
- **Requests:** up to **{{ planning_requests }} in total** (RFIs and RFFs combined), **posted in your team's secret Slack channel by minute {{ request_deadline }} ({{ request_deadline_at }})** so the white cell can answer them while loggers hear the Phase I briefs. The white cell posts answers and rulings in threads under your requests after the kickoff inject, before Turn 1. Phase I RFFs follow normal arrival timing (Scenario Brief §7), counted from Turn 1.
- **The brief.** In the last 3 minutes (minutes 15–18), give an **oral brief** of your plan to your own logger. It doesn't have to follow the five-paragraph OPORD format, but the template in the Player Forms (Situation, Mission, Execution, Sustainment, Command & Signal) is there if you want a structure. Nothing written is required.
- **Planned COAs.** The brief may name **up to 3 planned COAs** in order for Phase II, e.g. "Turn 1: X; Turn 2: Y; Turn 3: Z." The logger writes them down. When you later execute a planned COA *substantially as briefed, and the situation still supports it*, you get **+1 (Planned)**. If events make it invalid (the target is gone, you lost the assets, or the enemy forced a reaction), the bonus is lost. Recognizing that and adapting is the point.
- **Organize your team.** Only your flight commander is assigned. The team decides everything else, for example who runs operations, intel, logistics, and requests, and who briefs COAs and Cons. Rotate briefers so everyone talks.

### 1.4 Phase III – Planning and FRAGO

- **Command handover and FRAGO.** After Debrief 1, the **Phase III–IV flight commander** takes command. The new flight commander gives a **1-minute oral Fragmentary Order (FRAGO)** to the team's logger: a brief situation update, updated Commander's Intent, and **up to 2 new planned COAs for Phase IV (Turns 5–7)**, which earn the same **+1 (Planned)** bonus when executed as briefed.
