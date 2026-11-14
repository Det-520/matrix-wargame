---
title: "Operation Example — White Cell Handbook"
subtitle: "Procedures and adjudication for lead adjudicators and loggers · [Event] · [Date]"
short: "White Cell Handbook"
---

**WHITE CELL ONLY.** This handbook and the other white cell documents hold both sides' secrets, the injects, and the ground truth. **Never leave them where players can see them.**

*Fictional training scenario. All military systems are real U.S. systems, described with unclassified, approximate capabilities.*

> **TEMPLATE.** The procedure in this handbook (§1, §2.1–2.2, §4, §5.1–5.3, §5.5, §7.1) is the same for every scenario, and follows the teams in `game.toml` `[[side]]`. The tables that list the scenario's own tracks, counters, starting conditions, RFF pools, and objectives (§2.3, §2.4, §3, §5.4, §6, §7.2, §8) hold placeholders or example rows: fill them in from `scenario/` once it is settled, with a column or a section for each team, in the order of `[[side]]`.

<!-- pagebreak -->

## 0. What's Going On?

We are running a matrix wargame where GMC will play opposing teams ({{ teams }}) in a conflict and POC will be adjudicating (the white cell). Each turn, teams present their COAs, give pro arguments for why it would be successful and then give cons against {{ "the opposing team's COA" if n_teams == 2 else "the other teams' COAs" }}. The white cell will then evaluate the arguments which become modifiers to a roll which determines if the COA was successful. White cell then delivers the outcomes accordingly.

<!-- pagebreak -->

## 1. POC Roles

The white cell is the neutral referee. It runs the clock, judges the arguments, rolls the dice, narrates the results, introduces fog and friction, and keeps the game on the rails. Each of the groups plays its own game at its own table, so each table has its own white cell consisting of at least {{ word(n_teams + 1) }} POC: a lead adjudicator and a logger for each team.

| Role | Job |
| --- | --- |
| **Lead adjudicator** | Runs the **timer program** and the **dice program**, shown on the room's TV or projector. Calls each step. Gives injects. Rules on every COA and RFF. **Final authority.** |
| {{ team_rows("**{label} logger** | Hears {label}'s Phase I brief and Phase III FRAGO. Keeps the {label} placement form (White Cell Forms §4): planned COAs, hidden-counter locations, arrivals, and counters that changed. Moves {label} counters. Watches {label}'s team channel, counts its requests, and posts the lead adjudicator's answers (§2.4). Doesn't log every move. Keeps the white cell site and Slack open on a laptop the teams can't see.") }} |

The white cell should work to be efficient and generally help teams stay within the bounds of the rules. As white cell, you are given lots of freedom:

- You make up the outcomes of a COA
- You can add injects as you please
- You determine which RFIs and RFFs are allowed (there is some guidance on how to respond)

Generally, you should be helpful in ensuring that teams understand the rules and ask clarifying questions. While the complexity of the rules may seem daunting, also know that it is the responsibility of teams to advocate for themselves: to point out the assets they have, argue the success and effects of a COA, remind white cell of triggers that are to their advantage, etc.

<!-- pagebreak -->

## 2. Before the game

### 2.1 Distribution

| Who | Gets |
| --- | --- |
| **Every player** | {% if rules == "full" %}Player Rules Handbook{% else %}Basic Rules{% endif %} · Scenario Brief · Scenario Schedule · Starting Conditions · Player Forms |
| {{ team_rows("**{label} players** | + {label} Commander's Read-Ahead · {label} Team Packet · {label} Order of Battle · {label} Intelligence Products") }} |
| **White cell** | Everything |

**Nobody on a team gets another team's documents.** Teams and flight commanders should be assigned before distribution.

**Distribution schedule**

- **ASAP:** general rules information ({% if rules == "full" %}Player Rules Handbook{% else %}Basic Rules{% endif %}, Player Forms)
- **One week prior (e.g. over Canvas):** scenario information (Scenario Brief, Scenario Schedule, Starting Conditions, map)
- **24 hours prior (over email):** team assignments, team information, and the Slack invitations (the designer sends them; §2.4)

### 2.2 Prep checklist (before the event)

The White Cell Checklist has the full list, from a week out to cleanup, in order.

- [ ] Everyone in the white cell has at least skimmed the Likely Plans guide, so you know the COAs to expect and where to look up how to rule on them.
- [ ] You're in your group's Slack channel and {{ "both" if n_teams == 2 else "all " ~ word(n_teams) }} of its team channels (§2.4).
- [ ] Everyone in the white cell has at least skimmed **every** team's intelligence products and the key (Intelligence and Injects §3), and knows how to look one up, so you can check a Pro that may be built on a false report.
- [ ] The timer and dice program works on the room computer connected to the TV or projector (or the lead adjudicator's laptop, if the room has none) and shows on the screen, where every player can see it. Each logger's laptop opens the white cell site and Slack.
- [ ] Printed: one **Print Packet** per table (`White Cell/Print Packet - One Table.pdf`). `Print Packet - One Table, Reference Forms.pdf` is the same packet with one copy of each player form and slip for each team and no spares, for tables that will photocopy their own. Its cover lists what is in it: the White Cell Checklist, White Cell Forms (score sheet, ongoing-effects sheet, objective status card, a placement form for each team), starting-condition cue cards, counters, the map in letter tiles, each team's player forms and request slips, and spare forms and slips at the back. Print the game pieces (counters, map, cue cards) in colour and the rest in greyscale. For one large map, print `map-full.pdf` on a plotter.
- [ ] Counters printed and cut out: one set per table. It shows **every** team's hidden assets, so keep it with the white cell. The HIDDEN counters stay in an envelope until they go on the map (§2.3).

### 2.3 Table setup

The **Table Setup Guide** is the at-the-table version of this section: the devices, the table layout, every counter by name and zone, and a setup checklist. In short: the lead adjudicator puts the timer and dice program up on the room's TV or projector, using the room computer where one is connected, and each logger keeps the white cell site and Slack open on a laptop the teams can't see.

**Tracks** (in the tracker on the timer and dice program, shown on the TV or projector; there is no paper track board)

| Track | Start position |
| --- | --- |
| [Track] | **[start]**. [Any change at the kickoff inject.] |
| [Track] | **[start]** |

**Objective status card** (White Cell Forms §3): blank, **face down with the logger**. Each logger also keeps its team's **placement form** (White Cell Forms §4) face down. Never put it beside the ongoing-effects sheet, because it shows what the secret objectives look for.

**Starting-condition cue cards** (face up, visible to {{ both }} teams): [S-R1 to S-R*n*, S-B1 to S-B*n*].

**Counters on the central map (visible only)**

| Zone | REDFOR | BLUEFOR |
| --- | --- | --- |
| Z1 [Red nation] (off-map box) | R-16 | |
| Z6 [Red forward base] | R-01, R-05 | |
| Z10 [Blue coast] | | B-04, B-07a |
| Z11 [Blue capital] | | B-01, B-07b |
| Z12 [Blue interior] | | B-07c |

B-07 (radar network) has one counter in each of Z10, Z11, and Z12. Each part moves and takes damage on its own (Rules §4.5).

**Hidden counters stay off the map**, on the owning team's sheet and on the Master Asset List:

| Side | Hidden counter | Where |
| --- | --- | --- |
| REDFOR | R-18 B-2A Spirit | Z1 [Red nation] |
| BLUEFOR | B-09 Harpoon coastal-defense battery | Z10 [Blue coast] |

A hidden counter goes on the map under three conditions:

- **Found** by a successful ISR COA
- **Used** by its owner
  - If a team mentions a hidden asset in a COA or argument, it is revealed, whether or not the COA had its intended effect.
- **Disclosed** by an inject (e.g. a defector inject)

### 2.4 Slack channels

Nothing is handed over on paper (Rules §2.5). Slack is the **record**: teams still brief and argue **aloud**, and only what is said in the slot counts. The designer creates the channels and sends the invitations. Each group has a **public group channel** ({{ both }} teams and the white cell) and a **secret team channel** for each team (that team and the white cell). Each logger watches its team's channel.

| Group | Group channel (public) | {{ team_cols("{label} team channel") }} |
| --- | --- | {{ team_cols("---") }} |
| 1 | `[prefix]-group1-[room]` | {{ team_cols("[prefix]-{lname}-{id}", 1, code=True) }} |
| 2 | `[prefix]-group2-[room]` | {{ team_cols("[prefix]-{lname}-{id}", 2, code=True) }} |

| Teams post | Where | When | White cell does |
| --- | --- | --- | --- |
| COA and Pros | Group channel | By the end of its COA slot | Read the asset IDs while adjudicating. **Only what was said aloud counts.** |
| Cons | Group channel | By the end of its Cons slot | Same |
| Each RFI or RFF, one per message | Team channel | During Prepare (Phase I: by minute {{ request_deadline }}) | Logger counts the first {{ requests }} (Phase I: {{ planning_requests }}) and posts the lead adjudicator's answer in a **thread** under each, by the start of the next Prepare |

{% if rules == "full" %}

**Secret COAs** also go in the team channel: in the COA slot, announced aloud, or during Phase I or III, unannounced and not using a turn's COA. The logger pins each one and checks its trigger every resolve step.

{% endif %}

- Post nothing in a team channel except answers and procedure ("Requests closed"). Never put anything from a team channel into the group channel or another team's channel.
- **Slack down?** Hand out the backup paper slips from the Print Packet and carry on.

<!-- pagebreak -->

## 3. Master schedule of phases

> **FORMAT NOTE (delete before printing):** The table is generated from the run of show in `game.toml` (`[[block]]` and `[[turn_step]]`), the same settings the timer program runs. Change it there; the build fills it in.

{{ schedule_table("whitecell") }}

### 3.1 Scripts

Read these aloud, word for word or close to it.

**Phase I opening ({{ blocks.P1.start }})**

> "Your intelligence suggests that an attack is imminent. You have {{ blocks.P1.min }} minutes to organize your team, synthesize your intelligence, and build a plan. You may submit up to {{ word(planning_requests) }} requests, RFIs or RFFs, due at minute {{ request_deadline }}—six minutes before the end of the phase. In the last three minutes you will brief your plan to your logger, including up to three planned COAs. There are no COAs in Phase I. Your time starts now."

**Phase I minute {{ request_deadline }} call ({{ request_deadline_at }})**

> "Six minutes left in Phase I. Requests close now—we'll answer the first {{ word(planning_requests) }} posted in your team channel. You have three minutes to rehearse before you brief your logger."

**Turn start**

> "Turn [N]. Prepare, {{ word(steps.prep.min) }} minutes. Your RFI answers are in your team channel. Requests are due there when the timer ends."

**Phase III Planning and FRAGO call (1519)**

> "One minute left in Phase III. Phase III–IV flight commanders, brief your one-minute FRAGO and up to two Phase IV planned COAs to your logger now."

**End of game (1605)**

> "That was the final turn. Here is where things stand." Then read the tracks and key map facts, and score (§8).

## 4. Running a turn

### 4.1 Turn steps and timing checklist ({{ clock(turn_min) }} per turn)

{{ turn_clock_table("whitecell") }}

**End-of-turn track checks** (do these every turn, in the resolve step)

- [ ] Per-turn track effects (§6.2), e.g. [a track at its worst value moves another track every turn].
- [ ] Any track at a trigger value? Apply it (§6.2).
- [ ] [Any starting condition that switches on at a set turn (§6.1).]
- [ ] Any RFF arriving **next** turn (including N+1 RFFs approved just now) → announce it and place its counter (each side's main base zone unless the RFF named another destination). It can be used in next turn's COA.
- [ ] {% if rules == "full" %}Any secret COA trigger met → resolve it now.{% else %}Anything else the turn changed is on the map and the tracks.{% endif %}

### 4.2 Keeping order

- **It's a courtroom.** Players speak only in their slot. Accept only points of fact or procedure. "You had your slot" ends most disputes.
- **Late objections** (after the slot, or after the roll) **are not considered**. Results are never re-run.
- **Laundry lists.** Count only the first three reasons and only one action. If a COA tries to do two unrelated things, tell the briefer to pick one, or pick the first.
- **Behind schedule?** Shorten **Prepare** (to {{ flex }}). **Never cut the Cons.**
- **Players out of bounds?** Kill the COA outright, or deliver I-13, a bounding directive.
- **Simultaneous execution and reacting.** {{ Both }} COAs take place simultaneously across the {{ days(game_days, adj=True) }} turn window. A team that briefs later in the order ({{ team_order }}) may react to an earlier team's COA, which is realistic. However, it **may not simply negate** that COA ("their strike doesn't happen") or prevent its roll. Negating is what Cons are for; a counter-move is resolved as an **Interacting** or **Directly Opposed** COA (§5.3).

<!-- pagebreak -->

## 5. Adjudication

### 5.1 Procedure for each COA

1. **Check feasibility:** time ({{ days(game_days) }}), space, and assets the team actually has. If it fails, rule it **impossible** (no roll) or **scope it down**. Say so in one sentence.
2. **Auto-success?** No credible Cons, or an overwhelming case → **Success** without a roll.
3. **Count modifiers:** Cap the net at **±4**.
4. **Roll 2d6** in the dice program, add the modifiers, and read the band.
5. **Narrate** in one or two sentences. It may also be helpful to name the deciding Pro or Con.
6. Successful results become **established facts**.

**Argument to Modifier Reference**

| Modifier | Value |
| --- | --- |
| Each **strong** accepted Pro | +1 (one exceptionally compelling Pro may be +2) |
| Each **strong** accepted Con | −1 (one exceptionally compelling Con may be −2) |
| Weak, vague, or duplicate reason | 0 |
| **Planned** COA, executed as briefed in Phase I or Phase III FRAGO and still valid (check the placement form) | +1 |
| Each starting condition or ongoing effect that applies (§6) | ±1 |
| Each asset in the COA that is **Degraded** (each counter in a package counts) | −1 each |

**Outcome Reference**

| Total | Result | Typical outcome |
| --- | --- | --- |
| **≤ 3** | **Critical failure** | Fails, and something goes wrong: losses, exposure (a hidden counter revealed), backlash, a track moves against the actor |
| **4–6** | **Failure** | No meaningful effect. A risky combat action may leave its assets **Degraded**. |
| **7–8** | **Partial success** | Happens, but limited or at a cost: the target is **Degraded** instead of Destroyed, or there are own losses or a political cost |
| **9–11** | **Success** | Happens as argued |
| **≥ 12** | **Exceptional success** | As argued, plus a bonus: an extra effect, a new established fact, or a track moves in the actor's favor |

**Probability Card**

| Net modifier | −4 | −3 | −2 | −1 | 0 | +1 | +2 | +3 | +4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Natural roll needed | 11+ | 10+ | 9+ | 8+ | 7+ | 6+ | 5+ | 4+ | 3+ |
| Chance of at least Partial | 8% | 17% | 28% | 42% | 58% | 72% | 83% | 92% | 97% |

### 5.2 Judging a reason in seconds

Ask four questions. **Four yeses = strong (±1).** Decisive on its own = ±2. Anything else = 0.

1. **Is it true?** An established fact, a listed capability or limitation, or a reasonable assumption.
2. **Is it relevant** to *this* action and *this* effect?
3. **Is it new,** not a restatement of a reason already counted?
4. **Does it matter?** Would a real commander care?

**Common calls**

| Situation | Call |
| --- | --- |
| A Pro about the *effect* ("closing the strait hurts their economy") | 0 toward success. It explains why the COA matters, not why it works. |
| A Con about *consequences* ("civilian casualties will cause outrage") | 0 toward success, but **shape the outcome** with it: side effects and track moves |
| A Con that a Pro already answered, or vice versa | They cancel. Count neither. |
| A reason that names doctrine but doesn't explain how it applies | 0 |
| A reason built on something that happened earlier in the game | Usually strong. Reward building on the story. |
| A reason built on an **intelligence product** | Check the key (Intelligence and Injects §3). A **true** report can be strong, and stronger if the team confirmed it. A **false or misleading** report counts 0, and acting on it can make the COA fail in an instructive way. |
| A Pro relying on a hidden asset's capability the briefer hasn't revealed | The COA uses the asset, so it is revealed. Place the counter. |
| A Con relying on information the team shouldn't have | 0. Teams argue from their own intel. |
| An interaction nobody mentioned (BLUEFOR dispersed the SAMs REDFOR struck) | Fold it into the modifiers anyway. A well-timed counter-move is a strong Pro or Con even if unspoken. |

### 5.3 Interacting COAs (simultaneous execution)

{{ Both }} COAs happen simultaneously across the {{ days(game_days, adj=True) }} turn window. A team that briefs later can't stop an earlier team's COA from being rolled; instead, resolve interactions using one of these three cases:

- **Independent** (different places or effects): resolve each normally, in briefing order ({{ first_team }}'s first).
- **Interacting** (one affects the other's odds): fold the interaction into the modifiers.
- **Directly opposed** (both can't succeed): **opposed roll**. Roll 2d6 for each team in the contest (the dice program's opposed roll takes every team), each adds its own modifiers, and the highest total wins. A tie for highest means those teams are **Partial**, the situation stays contested, and you describe a stalemate.

### 5.4 Special COA types

| Type | Handling |
| --- | --- |
| **Big project** (coalition, ACE network) | State up front how many successful COAs it needs, **at most 3**. [Name any big projects the scenario defines, with their counts.] Track progress on the ongoing-effects sheet (White Cell Forms §2). |
| **Protected or hidden target** | At most 3 layers, e.g. *find* (ISR COA), then *strike*. A strike on a hidden counter nobody has found is impossible, or becomes an ISR COA. An intel product that points at a hidden asset is a good Pro for the *find* COA, not a substitute for it. |
| **Long-term COA** | Success means the effect **has started and continues** until someone stops it. Record it as an ongoing effect. |
| **Announcement** | Free, unless it claims a measurable effect. Then it is the team's COA. |
| **Arguing a player-controlled actor agrees** | Not allowed. Tell the team to ask in person (a parley, §7.1). |
| **Persuading a white-cell actor** (third-party states, the press, populations) | A normal COA. Use the ground truth (Intelligence and Injects §1) for how those actors really feel. **No RFF needed** (§7.1). Don't deny or scope it down for lack of one. |

{% if rules == "full" %}

**Secret COAs.** One per team per phase (II and IV). It may be posted in the planning phase before (I or III); then it costs no turn's COA. The logger pins the Slack post (or keeps the backup slip). Resolve it when the trigger occurs, using your own judgment in place of Cons. **A loose trigger doesn't fire.**

{% else %}

**Basic rules.** This game uses the Basic Rules (`game.toml` `[rules]`), so there are no secret COAs and no estimative vote. Everything else in this handbook applies. The Basic Rules cover big projects, layers, long-term COAs, and colliding COAs in a sentence or two each, so say what you are doing when one comes up ("Building the coalition takes two successful COAs; this is the first").

{% endif %}

### 5.5 Contentious calls

{% if rules == "full" %}

If both teams keep arguing, or the call is too close to count in time, don't debate. Either **make the call**, or announce an **estimative vote** (Rules §4.3; players know this rule from Player Rules Handbook §2.7): each white cell member shows 1–5 fingers for how likely the COA is to work, you take the **median**, and roll against it with the dice program's **Estimative vote** button. **Happens = Success. Doesn't happen = Failure.** Narrate it like any other result.

**Estimative Vote Card**

| Fingers | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- |
| Meaning | Remote | Unlikely | Even chance | Likely | Almost certain |
| Roll needed on 2d6 | 11+ (8%) | 9+ (28%) | 50% (the program's percentage roll) | 6+ (72%) | 4+ (92%) |

{% else %}

If both teams keep arguing, or the call is too close to count in time, don't debate. **Make the call**, say the deciding reason in a sentence, and roll. The basic rules have no estimative vote, so its button is hidden on the dice program.

{% endif %}

<!-- pagebreak -->

## 6. Starting conditions, tracks, and ongoing effects

### 6.1 Starting conditions: when to apply them

*One row per starting condition in `scenario/00-overview.md` §5.2, rewritten for quick rulings: when exactly it applies, and what removes it.*

| ID | Name | Apply when | Effect | Removed by |
| --- | --- | --- | --- | --- |
| S-R1 | [Name] | [The kind of COA it touches, and from which turn] | −1 | [What removes it] |
| S-B1 | [Name] | | | |

### 6.2 Track triggers

| Track | Trigger | What happens |
| --- | --- | --- |
| [Track] | **[value]** | [Effect; name any starting condition or RFF it unlocks] |

**Fixed track moves** from the rules of engagement (`scenario/00-overview.md` §7):

| Event | Move |
| --- | --- |
| A COA result causes significant civilian casualties | [Opinion and Domestic Will against the side that caused them] |

### 6.3 Ongoing effects

At the end of each resolve step, state any **ongoing effects** in one line ("refugees on the coast road," "the port burning," "mines in the strait"). Each gives ±1 to related COAs **until a successful COA removes it**. Write them on the ongoing-effects sheet (White Cell Forms §2) so all players can see them.

<!-- pagebreak -->

## 7. Ruling on RFFs

### 7.1 Parleys and diplomacy (no RFF)

**A parley** (Rules §6.1) is a talk of up to {{ clock(parley) }} between {{ "the two teams" if n_teams == 2 else "two or more teams" }} during Prepare. It stands for talks between the governments during the turn, and it is the only way one team gets a decision from another. It is not a COA or a request: no roll, no Pros or Cons, and it doesn't count against the {{ requests }} requests.

1. A flight commander (or delegate) asks you. Authorize it unless Prepare is nearly over. A team asked to parley may decline.
2. One person from each team comes to the white cell end of the table. Start the **Parley** timer in the timer program (≤ {{ clock(parley) }}). Listen; don't mediate or advise.
3. At the end, each side says aloud what it agreed to. Repeat the deal back. The logger notes it on the objective status card (White Cell Forms), including what each side says it agreed, if they differ.
4. The deal **happens**. Apply its effects in this turn's resolve step. If the teams later dispute it, you decide from the logger's note. A broken deal is an established fact; you may move tracks.

Parleys are only between the teams. A team that wants to talk to a white-cell actor (a third-party state, the press) makes a COA.

**Diplomacy needs no RFF** (Rules §6.2). Each team speaks for its whole government, President included. Parleys, the deals made in them, and diplomatic COAs (basing, overflight, recognition, mediation, pressure on a third party, an offer of talks) need no RFF and no one's permission. RFFs for authorities cover only the military limits in the ROE (Scenario Brief §8), such as leadership strikes in the enemy capital or ground forces on enemy soil. A deal that commits forces to one of those still needs the authority before they act. A neutral state's consent comes from a diplomatic COA, not an RFF.

If a team posts an RFF asking permission to negotiate, the logger answers in the thread: "No RFF needed: diplomacy is within your authority (Rules §6.2)." It doesn't count against the team's {{ requests }} requests.

### 7.2 Rulings and arrival turns

Rule on RFFs during the resolve step and tell the team the **arrival turn**. **Approvals stand** (Rules §5): once approved, a force arrives and a grant stays even if the track that allowed it moves later. "N" is the turn the RFF is submitted, which is also the turn you rule on it. Phase I RFFs count as Turn 1. Arriving forces **can be used in the COA of the turn they arrive**: an N+1 RFF submitted and approved on Turn 3 arrives on Turn 4 and can be part of the Turn 4 COA, so place its counter now. An N+0 grant (new authorities) takes effect when approved and applies from the next COA. Forces arrive on each side's main base zone (**Z6** for REDFOR, **Z11** for BLUEFOR, outside support included) unless the RFF names another destination; rule on whether that destination is realistic.

*One row per RFF in each packet's pool, with the condition for approving it. Copy the conditions from the packets and add the white cell's judgment calls (a partial approval, what an approval unlocks).*

**REDFOR**

| ID | Asset | Arrives | Approve when |
| --- | --- | --- | --- |
| R-30 | Additional F-35A squadron | N+1 | There is basing room at the forward base. Consider a partial approval if it is crowded. |

**BLUEFOR**

| ID | Asset | Arrives | Approve when |
| --- | --- | --- | --- |
| B-30 | Reserve mobilization: 2 infantry brigades | N+1 | Routine. If repeated, you may move a track for the economic cost. |
| B-40 | Arms shipment from [Backer] | N+2 | **Routine.** REDFOR may try to interdict it in transit. |

**No counter for it?** A free-text RFF or a force an inject creates (a third party's escort, a pirate band, an ally's squadron) goes on a **blank counter** from the white cell counter sheet: {% for s in sides %}{{ s.prefix }}- for {{ s.label }}, {% endfor %}or grey X- for third parties. Write the ID (free-text RFFs from {% for s in sides %}**{{ s.prefix }}-50**{% if not loop.last %}, {% endif %}{% endfor %}; inject forces from **X-01**), a short name, and the zone. Note it on that team's placement form.

**Free-text RFFs** (not in a pool): judge them by realism, the timing table, and politics. A big request may need a successful COA first to build the case. **All assets must be U.S. systems.**

**Watch for RFFs that settle an objective.** If approving an RFF would decide an objective by itself (an outside backer's troops arriving, say), make sure its conditions are really met when you approve. Once approved, it arrives even if the condition later lapses.

## 8. End of game and scoring

After Turn {{ turns }}'s resolution:

1. **State the end state:** every track, [the map facts the objectives check], and any agreements reached.
2. **Score each objective** as Achieved, Partial, or Not achieved, using the tables below. Loggers record the results.

### REDFOR Objectives

| # | Objective | Achieved | Partial | Not achieved |
| --- | --- | --- | --- | --- |
| R1 | [Objective] | | | |
| R2 | [Objective] | | | |
| R3 | [Objective] | | | |

### BLUEFOR Objectives

| # | Objective | Achieved | Partial | Not achieved |
| --- | --- | --- | --- | --- |
| B1 | [Objective] | | | |
| B2 | [Objective] | | | |
| B3 | [Objective] | | | |

### Scoring notes

*Copy the scoring notes from `scenario/whitecell-ground-truth.md` §2: what each ambiguous phrase means, which objectives can both be achieved, and which are opposed through a track. If the teams are talking, let them. That is the game working.*
