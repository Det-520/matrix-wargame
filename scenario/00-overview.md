# [Scenario name] — Scenario Overview

**Audience:** everyone. This file goes into **both** team packets unchanged, so it must never contain hidden assets, secret objectives, or inject plans.
**Owner:** [designer] · **Version:** 0.1 ([date]) · Index of scenario files: `scenario/README.md`

Status tags (**[CANON]**, **[PROPOSED]**, **[OPEN]**) work as defined in `RULES.md` §0.

> **TEMPLATE.** Every section below says what belongs in it and gives a short example in brackets or italics. Replace the guidance with the scenario's own text. Watch for indirect leaks: nothing here may describe a capability that only a hidden asset in a packet reveals.

---

## 1. Bottom line up front

*Five to eight bullets: who each side is, what the conflict is about, the geography in one line, the outside backers, and the balance.*

- **REDFOR = [Red nation]**, [one line: what kind of state it is, where it is relative to the conflict].
- **BLUEFOR = [Blue nation].** [One line: its government and military, and why it is in conflict with REDFOR.]
- **[The key terrain]**, [one line: why both sides care about it].
- **[A third party]** backs [a side]. **[Another]** sides with [a side].
- **Balance.** REDFOR starts with **more assets**. BLUEFOR has **natural advantages**: [e.g. defending its own land, a supportive population, outside support].
- **All assets are American.** Every asset in the game is a real U.S. military system, mostly **Department of the Air Force**, so players learn American capabilities. This applies to every actor. [Give the in-world reason, or call it a game convention.]
- The war begins with the white cell's kickoff inject at the end of Phase I.

---

## 2. Background and timeline

Game dates are relative: **D-Day** is the kickoff inject.

| When | Event |
| --- | --- |
| ~D−[years] | [The old relationship or treaty that sets up the conflict] |
| D−[months] | [The trigger: an election, a coup, a scandal, a seizure] |
| D−[weeks] | [Escalation: positions harden, forces move, backers commit] |
| D−3 days (Phase I) | Crisis peak. Both sides posture. **Phase I play happens here.** |
| **D-Day** | Kickoff inject: war begins. |

---

## 3. Geography and map

### 3.1 Map

The game map is built from `map/source/map.svg` (see `map/README.md`) into `map-full.pdf` (one sheet) and `map-tiles.pdf` (letter tiles) in the release folder. [Describe it in two or three sentences: what is where, which areas are coloured for which side, what is off-map.]

### 3.2 Map zones (counters go in zones; no hex grid)

*Zones are the only positions in the game. Ten to fifteen is enough for one table. Put each side's home or patron in an off-map box. The IDs below are an example layout; renumber freely before anything references them, and never after.*

| Zone ID | Zone | On central map? | Notes |
| --- | --- | --- | --- |
| Z1 | [Red nation] | Off-map box | REDFOR home: bombers, airlift, space, cyber, reserves |
| Z2 | [Blue's backer] | Off-map box | The source of outside support for BLUEFOR |
| Z3 | [Third-party state] | Yes | [Alignment; what it can grant] |
| Z4 | [Neutral interior] | Yes | [Terrain] |
| Z5 | [Neutral coast] | Yes | [Terrain] |
| Z6 | [Red forward base] | Yes | REDFOR's main base in theater |
| Z7 | [Sea zone] | Yes | |
| Z8 | [The chokepoint] | Yes | [Why it matters] |
| Z9 | [Sea zone] | Yes | |
| Z10 | [Blue coast] | Yes | |
| Z11 | [Blue capital] | Yes | BLUEFOR's main base |
| Z12 | [Blue interior] | Yes | Reserve bases, dispersal areas |
| Z13 | [Open ocean] | Yes (edge) | |

### 3.3 Key distances

*Measure them from the finished map. Each row should say why the distance matters in an argument (tanker support, missile range, reinforcement time).*

| From → To | Distance | Why it matters |
| --- | --- | --- |
| [Red forward base] → [the chokepoint] | [~ mi] | [e.g. fighters need tanker support for persistence] |
| [Blue coast] → [Red forward base] | [~ mi] | [e.g. inside or outside a missile's range] |
| [Red home] → theater | [~ mi] | Long reinforcement timelines (§6) |

---

## 4. Actors

### 4.1 [Red nation] — REDFOR (player team)

*One row per PMESII dimension, a sentence or two each. The Cons the other side will use come from here.*

| Dimension | Situation |
| --- | --- |
| **Political** | |
| **Military** | |
| **Economic** | |
| **Social** | |
| **Information** | |
| **Infrastructure** | |

### 4.2 [Blue nation] — BLUEFOR (player team)

| Dimension | Situation |
| --- | --- |
| **Political** | |
| **Military** | |
| **Economic** | |
| **Social** | |
| **Information** | |
| **Infrastructure** | |

*Optional: if one team plays several factions (a government and a militia, say), add a faction table here with what each wants. Internal friction makes good starting conditions.*

### 4.3 Other actors (white-cell controlled)

*Every actor a team might try to persuade with a COA. Give each one interests and levers, so the white cell can rule consistently.*

| Actor | Alignment | Capability | Interests and levers |
| --- | --- | --- | --- |
| **[Backer]** | Backs [side] | | |
| **[Neutral state]** | Neutral | | [What it can grant or deny] |
| **International shipping and markets** | — | — | React to the tracks. The white cell narrates prices, rerouting, insurance. |
| **The press** | — | — | The white cell's voice for consequence management |

---

## 5. Tracks and starting conditions

### 5.1 Tracks (shown on the white cell's screen, moved by COA results and consequence management)

*Three to five tracks. Each one should tie to at least one objective and have a trigger at its ends. Copy the final set into `game.toml` `[[track]]`, which the timer program shows.*

| Track | Range | Start | Moves when… | Trigger effects |
| --- | --- | --- | --- | --- |
| **[Access track]** | Open / Restricted / Closed | | | |
| **International Opinion** | −3 (pro-Blue) … +3 (pro-Red) | | Civilian harm, legitimacy actions, diplomacy, propaganda, broken deals | |
| **[Red] Domestic Will** | 0 … 5 | | Casualties, victories, information ops aimed at REDFOR's public | **0:** [REDFOR's government orders a ceasefire] |
| **[Blue] Regime Stability** | 0 … 5 | | Strikes on infrastructure, unrest, rallying around the flag | **0:** [BLUEFOR's government collapses] |

### 5.2 Starting conditions (shown openly to both teams on cue cards)

*Each is worth ±1 to the COAs it applies to, until removed. Give REDFOR constraints that cost its advantages something, and give BLUEFOR advantages that make up for fewer assets. Say how each one is removed. Copy the final set into `handouts/common/scenario-brief.md` §6 and `handouts/common/starting-conditions.md`.*

**REDFOR: more assets, longer reach, more constraints**

| ID | Name | Effect | How to remove |
| --- | --- | --- | --- |
| S-R1 | **[Name]** | [e.g. reinforcements arrive slowly; −1 on strike COAs from the forward base after Turn 3 until resupplied] | [e.g. a successful resupply COA] |
| S-R2 | **[Name]** | | |

**BLUEFOR: fewer assets, natural advantages**

| ID | Name | Effect | How to remove |
| --- | --- | --- | --- |
| S-B1 | **[Name]** | [e.g. −1 on COAs that need two rival forces to work together] | |
| S-B2 | **[Name]** *(advantage)* | [e.g. +1 to defensive COAs in home zones] | — (permanent) |

---

## 6. Timing and movement

"N" is the turn an RFF is submitted (Phase I RFFs count as Turn 1). A force can be used in the COA of the turn it arrives: an N+1 RFF submitted on Turn 3 arrives on Turn 4 and can be part of the Turn 4 COA.

**Main base zones.** Forces that arrive by RFF are placed on **[Z6]** for REDFOR and **[Z11]** for BLUEFOR unless the RFF names another destination (`RULES.md` §5).

| Movement | Takes |
| --- | --- |
| Any aircraft within theater | Same turn (part of the COA) |
| Fighters, tankers, and ISR self-deploying from home | Arrive N+1 |
| Bombers striking from home | Same turn, but the bomber counter is used up for that turn |
| Airlifted light ground forces | N+2 |
| Naval forces from regional waters | N+2 |
| Amphibious forces | N+3 |
| Heavy ground forces by sea from far away | **Beyond the game** (≥ 5 turns) |
| BLUEFOR ground forces within its own country (zone to adjacent zone) | Same turn |
| BLUEFOR mobilization | N+1 |
| Outside support to BLUEFOR | N+1 to N+3, depending on what is sent |
| Diplomatic results (basing agreements, recognition) | Same turn if the COA succeeds. Effects begin next turn. |

---

## 7. Rules of engagement and national directives (start of game)

These are public in the game world. The white cell may add, change, or lift directives with injects (`RULES.md` §7). That is the CANON tool for bounding behavior. *Each directive that needs national authority is something a team can ask for with an RFF.*

### 7.1 [Red nation] (REDFOR)

1. No nuclear, chemical, or biological weapons (applies game-wide to all actors).
2. **No strikes on leadership or government targets in [the Blue capital]** without national authority (an RFF for authorities).
3. **No ground forces on [Blue] soil** without national approval.
4. [Respect a neutral's sovereignty: no operations in its territory without its consent.]
5. Minimize civilian harm. A COA result causing significant civilian casualties moves International Opinion **and** Domestic Will against REDFOR.

### 7.2 [Blue nation] (BLUEFOR)

1. [A standing order that limits BLUEFOR, e.g. its regular military won't take part in political repression.]
2. Striking *civilian* targets in a third-party state moves International Opinion toward REDFOR.
