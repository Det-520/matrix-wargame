---
title: "Operation Example — BLUEFOR Team Packet"
subtitle: "[Blue nation]: objectives, intelligence estimate, constraints, planning guide"
short: "BLUEFOR Team Packet"
---

**BLUEFOR EYES ONLY.** This packet is for the BLUEFOR team and the white cell. **Never show it to REDFOR.**

*Fictional training scenario. All military systems are real U.S. systems, described with unclassified, approximate capabilities.*

**Your BLUEFOR read-ahead** is four documents: the **Commander's Read-Ahead** (your orders), this **Team Packet**, the **BLUEFOR Order of Battle** (your forces, your RFF pool, and the enemy forces you can see), and the **BLUEFOR Intelligence Products**.{% if team.cells %} Each of your cells also has a **Cell Brief** (§5).{% endif %} You also have the common documents: the {% if rules == "full" %}Player Rules Handbook{% else %}Basic Rules{% endif %}, the Scenario Brief, the Scenario Schedule, and the Player Forms.

> **FORMAT NOTE (delete before printing):** TEMPLATE. Fill each section from `scenario/bluefor-packet.md` and `scenario/00-overview.md`. This is the player-facing version of the packet: same objectives and estimate, plus the constraints and planning questions that point the team at good COAs, including non-kinetic ones.

## 1. Secret objectives

Keep these from REDFOR. The white cell scores them after the final turn.

| # | Objective | Achieved | Partial | Not achieved |
| --- | --- | --- | --- | --- |
| **B1** | **"[Objective]"** | | | |
| **B2** | **"[Objective]"** | | | |
| **B3** | **"[Objective]"** | | | |

### Things to think about

- No single COA will settle an objective. Plan a sequence.
- [Which tracks each objective runs through.]
- A negotiated outcome can count. Talks are a weapon too.

## 2. Intelligence estimate

*This is [the headquarters]' assessment of what [Blue nation] believes. It may be incomplete or wrong. The Intelligence Products are the raw reporting behind it, and they don't all agree. Use RFIs and ISR COAs to confirm. All visible REDFOR counters are on the central map.*

- **[Topic]:** [what the side believes, from `scenario/bluefor-packet.md` §2]

**Good first RFIs** might target the gaps above: [two or three examples].

<!-- pagebreak -->

## 3. Your constraints at a glance

**Your starting conditions** (full text in Scenario Brief §6)

| ID | Name | What it means for you |
| --- | --- | --- |
| S-B1 | [Name] | |

### REDFOR starting conditions you are up against

| ID | Name | What it means for you |
| --- | --- | --- |
| S-R1 | [Name] | |

**Your rules of engagement** (Scenario Brief §8): [the limits in one line each, separated by ·].

### Tracks that matter most to you

| Track | Starts | Watch for |
| --- | --- | --- |
| [Track] | | |

## 4. Phase I & Phase III Planning

### Planning questions

1. Which objective do we push first, and which tracks does that move?
2. [A question about the side's biggest constraint, and when it bites.]
3. Which intelligence products do we believe, which do we doubt, and which do we need to confirm before we act on them?
4. What are our **non-kinetic** COAs? Some ideas to test: [diplomatic, information, economic, cyber options from the scenario].
5. What would we need national authority for, and when do we ask?
6. Which hidden asset do we reveal first, and why?
{% if team.cells %}

## 5. Your cells

{{ team.label }} works in cells under the flight commander ({% if rules == "full" %}Rules Handbook §2.10{% else %}Basic Rules §5.4{% endif %}). Each cell has its own brief, with its counters and its part in each step. In Prepare, each cell lead pitches a COA; the commander picks the team's one.

| Cell | Lead | Job |
| --- | --- | --- |
| {{ cell_rows("**{name}** ({short}) | {lead} | {job}", team.id) }} |

{% endif %}
