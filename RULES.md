# Matrix Wargame Rules — Source of Truth

**Owner:** [designer]
**Scenario this game runs:** [scenario name] (see `scenario/README.md`)
**Event logistics** (schedule, rooms, groups, POC staffing): `EVENT-SETUP.md`
**Rules version:** base 1.0, as first played at an AFROTC LLAB in November 2026

This is the single authoritative rule set for the wargame: how a turn works, how moves are argued, and how they are adjudicated. If another document (team packet, slide, handout) disagrees with this one, this one wins, and the other document should be fixed.

Three parts, three jobs (full file map in `AGENTS.md`):

| Document | Holds |
| --- | --- |
| `RULES.md` (this one) | The matrix wargame mechanics: turn structure and timing, COAs, adjudication, requests, injects |
| `scenario/` | The world being played: actors, forces, map, starting conditions, objectives, injects, split by audience |
| `EVENT-SETUP.md` | The event that hosts the game: schedule, rooms, groups and teams, flight commanders, POC staffing, evaluation, materials |

---

## 0. How to read this document

### Status tags

| Tag | Meaning |
| --- | --- |
| **[CANON]** | Decided by the designer. Do not change without the designer's approval. |
| **[PROPOSED]** | A drafted rule that fills a gap. It is usable as written but has not been explicitly approved. |
| **[OPEN]** | A decision the designer still has to make (§11). |

A rule with no tag inherits the tag of its section heading.

**In the base.** Every tag in this file was set for the first game played with these rules. A new scenario inherits them as its starting point: the designer of the new game re-confirms them (they become that game's CANON) or changes them, and records the change in §11. Text in [square brackets] is a placeholder for the scenario to fill in.

### Document map

| Part | Who needs it |
| --- | --- |
| §1 Player Quick-Start | **Everyone.** This is all a player must know to play. |
| §2–§7 Full rules | Players who want detail, plus the white cell |
| §8 White Cell Adjudication Guide | White cell |
| §9 Game roles | Everyone |
| §10 Worked example turn | Everyone (read it before the game) |
| §11 Open decisions | Designer |
| Appendices | Phase I brief format, placement form, probability table, doctrine crosswalk, glossary |

**Rule sets [PROPOSED].** A game is played with one of two rule sets, chosen in `game.toml` `[rules]` `set`:

- **Full** (the default): everything in this document. Players get the Player Rules Handbook, and the Basic Rules (`handouts/common/basic-rules.md`) as a short first read for new players.
- **Basic**, for groups new to matrix games: no secret COAs (§3.4) and no estimative vote (§4.3). Everything else stands. The Basic Rules replace the Player Rules Handbook in the players' release; they explain the special cases (big projects, layers, long-term COAs) and interacting and opposed COAs (§4.2) in a sentence or two each, and leave out announcements and the finer points of parleys and RFFs. The build drops the secret COA slips and templates, the timer hides its estimative vote button, and the white cell documents print without those rules.

Text that applies to only one rule set sits inside `{% if rules == "full" %}` … `{% endif %}` in the handouts (`README.md`, Documents are templates). Time cost of the basic set: none; it saves the time secret COAs and votes take.

---

## 1. Player Quick-Start (read this if you read nothing else)

1. **What this is.** A *matrix wargame*: there is no rulebook of unit stats. You win arguments, not dice-math puzzles. Each turn your team proposes **one course of action (COA)** and gives **up to three reasons it will work**. The other team gives **up to three reasons it won't**. The **white cell** weighs the reasons, sets the odds, rolls the dice (with a computer program), and narrates what happens.
2. **Your side.** You are on one team: {{ teams_or }} (§2.6 covers games with more than two). Your team packet gives you your forces, your intel, and **three secret objectives**. Don't show another team your objectives.
3. **One COA per turn.** A COA is *one* main action with a *measurable effect*, e.g. "F-35As and an EC-37B strike the enemy's Patriot battery at the port **so that** the battery is destroyed and our ISR aircraft can operate over the coast." You can use several assets in one COA (a strike package counts as one action), but you can't do two unrelated things. Everything else your forces do is background activity.
4. **Format of your COA ({{ mins(sides[0].coa.min) }}):**
   > "Our COA: **[action]** in order to **[measurable effect]**. It will work because: **(1)** … **(2)** … **(3)** …"
5. **Format of your Cons ({{ mins(sides[0].cons.min) }}):**
   > "Their COA will fail or fall short because: **(1)** … **(2)** … **(3)** …"
6. **Good reasons** are specific and grounded in facts. They point to your assets' capabilities, the map, things that happened earlier in the game ("established facts"), and doctrine (tenets of airpower, principles of joint operations). Repeating a reason in new words earns nothing.
7. **Odds.** With no strong reasons either way, a COA succeeds on 7+ on two dice (58%). Each strong reason for it adds +1, and each strong reason against it subtracts 1. If a COA is obviously sound and unopposed, it succeeds without a roll. If a call is too contentious to count, the white cell may take a quick **estimative vote** on how likely it is instead (§4.3).
8. **RFIs and RFFs.** Each turn you may post **up to {{ requests }} requests in total** in your team's private Slack channel (§2.5), any mix of:
   - **RFI (Request for Information):** a question about the situation.
   - **RFF (Request for Forces):** a request for more assets or authorities from your national command. Reinforcements take time to arrive.
   Requests don't count as your COA, and there is no debate on them. **Diplomacy needs no RFF:** your team speaks for its government, so you can negotiate or make a diplomatic COA without anyone's permission (§6.2).
9. **Turn clock ({{ mins(turn_min) }}, run by a timer program; minutes in brackets):** {{ turn_line }}. {{ first_team }} always goes first (the first team listed in `game.toml` `[[side]]`){% if n_teams > 2 %}, and the order ({{ team_order }}) never changes{% endif %}.
10. **No interrupting.** It's a courtroom, not a debate. You speak in your slot and are silent in theirs. Raise only points of fact or procedure. **If you miss your slot, the point is lost.** There are no do-overs.
11. **Arguing about the other side is allowed.** You can argue *their* troops are tired or *their* radar has a gap. You cannot argue that a player-controlled actor *agrees* to something. Ask them in person instead.
12. **The point** is good decisions and good reasoning under pressure: plan, communicate, brief, defend your choices, and adapt.

---

## 2. Game structure

### 2.1 Phases [CANON: the default structure; the designer sets the structure and timing]

A game is a **run of show**: blocks in a fixed order, each one of two kinds.

- **Planning blocks** have steps but **no COAs**: planning, briefs, an inject, a debrief, a command handover.
- **Turn blocks** are a number of full turns (§2.2).

The designer sets the blocks, their order, their steps, every duration, and the number of turns in `game.toml` (`[[block]]` and `[[turn_step]]`). The timer program, the schedule tables in the Scenario Schedule and the White Cell Handbook, the turn count, and the number of forms printed all follow it (`python3 tools/schedule.py`), so the structure changes in one place. Fit it to the time the event has (`EVENT-SETUP.md` §3) and record the change in §11.

**Default structure.** The first game used the four phases below, and the rest of these rules use their names. A scenario with a different structure keeps the same pattern: a planning block before the first turn with a brief to the logger (§2.3), and, where command changes hands, a planning block with a FRAGO (§2.4).

| Phase | Turns | What happens |
| --- | --- | --- |
| **Phase I – Planning** | none | Teams study intel, plan, and file up to {{ planning_requests }} RFIs and RFFs (due at minute {{ request_deadline }}). They end by briefing their plan to their logger (§2.3). **No COAs.** |
| **Kickoff inject** | — | The lead adjudicator announces the conflict has begun (`scenario/whitecell-injects.md` §1). |
| **Phase II** | Turns 1–4 | Full turns (§2.2) |
| **Phase III – Planning & FRAGO** | none | After Debrief 1, the Phase III–IV flight commander takes command. Teams plan and end with a 1-minute FRAGO brief to the logger (§2.4). **No COAs.** |
| **Phase IV** | Turns 5–7 | Full turns (§2.2) |

Other structures that fit the same rules: a single planning block and one block of turns, for a short event; three playing phases with two handovers, for a longer one (one secret COA per playing phase, `game.toml` `[turns]` `secret_coas`); or a longer Phase I in place of the pre-read.

- **[CANON] Game time:** each turn represents **about {{ days(game_days) }}** of in-game time (`game.toml` `[turns]` `game_days`), so {{ turns }} turns cover about {{ days(game_days * turns) }} of conflict. Phase I covers the final days of crisis before the shooting starts. The white cell keeps timelines realistic: moving forces across an ocean takes turns, not minutes (`scenario/00-overview.md` §6). The scenario sets the length of a turn; pick one that lets a single COA finish or visibly start.
- Real-world clock times and the debriefs between phases are in `EVENT-SETUP.md` §3. The default turn counts (4 in Phase II, 3 in Phase IV) fit a 3-hour block.

### 2.2 The turn [CANON]

One turn is "a turn in the chess sense": each team acts once, and **{{ "both COAs" if n_teams == 2 else "all the COAs" }} take place simultaneously across the {{ days(game_days, adj=True) }} turn window**. **Target: {{ mins(turn_min) }}**, kept by a **timer program** the lead adjudicator runs.

The step lengths below are the default, set in `game.toml` `[[turn_step]]`. A designer may lengthen or shorten them to fit the event, but keeps the order, keeps the Cons, and keeps the white cell's resolve step: those are the rules, the minutes are the timing. The turn clock tables in the handouts, the times quoted in them, and the timer program follow `game.toml` on the next build (`tools/schedule.py`).

Every turn has these steps, in this order:

1. **Prepare** ({{ both }} teams): choose this turn's COA, post RFIs and RFFs in the team channel (§2.5) by the end of the step, negotiate (§6). The white cell posts answers to last turn's RFIs in each team channel by the start of this step. Requests have no debate.
2. **One COA slot per team**, in briefing order: the team's briefer states its COA and Pros (format in §3.2).
3. **Prepare Cons** ({{ both }} teams).
4. **One Cons slot per team**, each against {{ "the other team's COA" if n_teams == 2 else "any of the other teams' COAs (§2.6)" }}.
5. **White cell resolves**: adjudicate every COA (§4), rule on RFFs, update the map and tracks, possibly deliver an inject.

The steps as `game.toml` sets them for this game:

{{ turn_clock_table() }}

- **[CANON] Fixed order.** The teams brief in the same order every turn: {{ team_order }}. The order never switches. (It is the order of the teams in `game.toml` `[[side]]`, and each team's COA and Cons steps in `[[turn_step]]` follow it.)
- **[CANON] Simultaneous execution.** Although {{ first_team }} briefs first, {{ "both" if n_teams == 2 else "all the" }} teams' COAs happen at the same time in game terms. A team that briefs later **may** react to an earlier team's COA, which is realistic. It **may not** simply negate it ("their strike doesn't happen") or preempt that COA's roll. Negating is what Cons are for; a counter-move is resolved as an interacting or opposed COA (§4.2).

### 2.3 Phase I – Planning [CANON]

- Teams arrive having read the rules, scenario brief, and their team's intelligence products (distributed ≥ 24 hours prior). During Phase I (18 minutes), they organize their team, build a plan, and file RFIs and RFFs to posture forces before the war starts.
- **[CANON] Phase I request limit:** up to **{{ planning_requests }} requests in total** (RFIs and RFFs combined), **posted in the team channel by minute {{ request_deadline }}** (6 minutes before Phase I ends) so the white cell can adjudicate them while loggers hear the OPORD briefs. The white cell posts answers and rulings in each team's channel after the kickoff inject, before Turn 1 begins. Phase I RFFs follow normal arrival timing (`scenario/00-overview.md` §6), with N = Turn 1 (§5).
- In the last 3 minutes (minutes 15–18) each team gives an **oral brief** of its plan to its own logger, **organized like a five-paragraph OPORD**: Situation, Mission, Execution, Sustainment, Command & Signal (AFDP 5-0 App. E; see App. A). No written OPORD is expected.
- **Planned COAs.** The brief may name **up to 3 planned COAs** in intended sequence for Phase II, e.g. "Turn 1: X; Turn 2: Y; Turn 3: Z". The logger writes them down. When a team later executes a planned COA *substantially as briefed, and the situation still supports it*, the white cell adds **+1 (Planned)**. If events make a planned COA invalid (the target is gone, the resources were lost, or the enemy forced a reaction), the bonus is lost. Recognizing that and adapting is the point.
- Phase I has **no COAs**. The first COAs come in Turn 1, after the kickoff inject. A team may post its Phase II secret COA during Phase I (§3.4).

### 2.4 Phase III – Planning and FRAGO [CANON]

- **Command handover and FRAGO.** After Turn 4 and Debrief 1, the **Phase III–IV flight commander** takes command for the 8 minutes of Phase III (`EVENT-SETUP.md` §3). In the last minute of Phase III, the new flight commander gives a **1-minute oral Fragmentary Order (FRAGO)** to the team's logger: updated Commander's Intent and **up to 2 new planned COAs for Phase IV (Turns 5–7)**, which earn the same **+1 (Planned)** bonus when executed as briefed. A team may also post its Phase IV secret COA during Phase III (§3.4).

### 2.5 Slack channels [CANON unless tagged]

- Nothing is handed over on paper. Slack is the **record**: briefs and arguments are still given **aloud** in their slots (§2.2), and only what is said in the slot counts. A post that adds reasons not said aloud adds nothing.
- The designer creates the channels and sends the invitations. Players join before the event (`EVENT-SETUP.md` §2). Each group has two kinds of channel:
  - **Group channel** (public): {{ both }} teams of the group and its white cell. Each team posts its **COA and Pros** (by the end of its COA slot) and its **Cons** (by the end of its Cons slot), using asset IDs, so the white cell can read them while it adjudicates.
  - **Team channel** (secret): one team and its group's white cell. No other team is ever in it, so it is as secret as the team packet. The team posts its **RFIs, RFFs, and secret COAs** there, and the white cell answers there. The team's logger watches it.

| Group | Group channel (public) | {{ team_cols("{label} team channel") }} |
| --- | --- | {{ team_cols("---") }} |
| 1 | `[prefix]-group1-[room]` | {{ team_cols("[prefix]-{lname}-{id}", 1, code=True) }} |
| 2 | `[prefix]-group2-[room]` | {{ team_cols("[prefix]-{lname}-{id}", 2, code=True) }} |

Use a short prefix for the scenario (for example, `opx-` for Operation Example) and one row per group in `EVENT-SETUP.md` §5. The table has a column for each team in `game.toml` `[[side]]`.

- **One request per message.** The white cell counts the first {{ requests }} request messages after the previous turn's resolve step ({{ planning_requests }} in Phase I). The deadline is the **end of Prepare** (Phase I: minute {{ request_deadline }}). A request posted after the deadline, or beyond the limit, isn't answered; post it again next turn.
- **[PROPOSED]** The logger answers in a **thread under each request** (RFI answers and RFF rulings) and posts nothing else in a team channel except procedure. Templates for each post are in the Player Forms.
- **[PROPOSED]** **Backup:** if Slack or the network fails, teams write the same thing on paper (backup slips in the Print Packet) and hand it to the white cell.
- Time cost: none. Posting happens inside steps that already exist, and the white cell no longer collects or returns slips.

### 2.6 More than two teams [PROPOSED]

The default game has two player teams. A scenario may add more (`game.toml` `[[side]]`): a GRAYFOR, a coalition partner with its own agenda, an insurgency. Use one only when the actor has real capacity for independent action and objectives that pull against **every** other team; otherwise the white cell plays it as a white-cell actor (§3.5), which costs no time. `presets/teams.toml` has four archetypes (`presets/README.md` §1). Mouat's advice is that an even number of actors plays best, and that a "laundry list" of actors on one side makes a one-sided game (`DESIGN-GUIDE.md` §2.1).

- **Turn.** Each team has its own COA slot and its own Cons slot, in the order of `[[side]]` (`game.toml` `[[turn_step]]`, one COA step and one Cons step per team). All COAs happen simultaneously (§2.2).
- **Cons.** In its Cons slot a team gives **up to 3 Cons in total**, against any of the other teams' COAs, naming the COA each one is against. It may spend all three on one COA. A COA may therefore draw Cons from several teams; the white cell counts each strong one as usual, within the ±4 cap.
- **Resolving.** The white cell resolves every COA in briefing order. Directly opposed COAs use one opposed roll among the teams involved (§4.2).
- **Parleys and agreements** may involve any two or more teams (§6.1). An agreement binds only the teams that made it.
- **White cell.** One logger per team (§9.2).
- **Time cost:** each extra team adds its COA slot and its Cons slot (3 minutes at the default lengths) and about 1 minute of resolve time: about 4 minutes a turn. Fit the run of show to it (§2.1), or keep the turn length and cut the number of turns no lower than 6.

---

## 3. Courses of action (arguments)

### 3.1 What a COA is [CANON frame; detail PROPOSED]

- **[CANON]** Each turn each team presents one COA with **up to 3 reasons** it will work or be especially effective (Pros).
- A COA has two parts:
  1. **Action:** who does what, where, and with which assets.
  2. **Measurable effect:** what will be true on the map or tracks if it succeeds. Examples: "the Patriot battery destroyed," "[a track] moves to Open," "[a third party] grants combat basing," "[a track] −1."
- **One action per turn.** The action can be big ("mobilize the militia brigades") or a multi-asset package ("F-35A + KC-46 + EC-37B strike package"), but it must serve **one** effect. Two unrelated things are two COAs. Pick one. Choosing priorities is the point.
- Not every COA has to be kinetic. Diplomatic, information, cyber, space, economic, logistics, and deception COAs are all valid and are often stronger. Think **DIME** (Diplomatic, Informational, Military, Economic) and **PMESII** (Political, Military, Economic, Social, Information, Infrastructure).
- **Big projects** take **at most 3 successful COAs**, e.g. building a coalition or standing up a dispersed ACE network. The white cell states the number up front.
- **Protected and hidden things** need successful COAs to find or get through them, with **no more than 3 layers**. Example: a hidden mobile SAM must first be **found** (ISR COA), then **struck**.
- **Long-term COAs** are allowed. If an argued effect can't finish within one turn's {{ days(game_days) }}, success means it **has started and continues** until someone stops it.
- **Announcements** (press statements, declarations) are free. A briefer can add a one-sentence public statement to the COA slot. A statement with a measurable effect ("…in order to raise International Opinion by 1") *is* a COA.

### 3.2 Pros (reasons it will work) [PROPOSED]

- Up to **3**, stated during the COA slot.
- Strong Pros are **specific**, **relevant**, and **grounded**. They draw on:
  - **Established facts:** anything in the briefings, or anything created by an earlier successful COA. These are the strongest Pros. Building on the story is rewarded.
  - **Asset capabilities** listed in the scenario order of battle.
  - **Reasonable assumptions**, e.g. "trained aircrews outperform untrained militia." Unreasonable assumptions ("the militia shoots down the stealth bomber with rifles") count for nothing until someone has argued them into existence.
  - **Doctrine**, e.g. "This applies *mass* and *surprise* (principles of joint operations) and *concentration* (tenet of airpower)." Citing doctrine correctly and specifically counts. Name-dropping it doesn't.
- Weak, vague, or duplicate reasons are worth 0. Three weak Pros are worse than one strong one, because the briefer used up the time.
- **[PROPOSED] Intelligence products are not established facts.** Each side's intel products (`handouts/redfor/intel/`, `handouts/bluefor/intel/`, one file per product) are deliberately a mix of true, misleading, and irrelevant reports. A reason built on one counts only as far as the report is believable. The white cell judges it against ground truth, and confirming a report with an RFI or ISR COA makes it stronger.

### 3.3 Cons (reasons it won't work)

- **[CANON]** The opposing team gives **up to 3** reasons the COA will fail, be ineffective, or have minimal impact. (With more than two teams, each team gives up to 3 in total across the COAs it opposes, §2.6.)
- **[PROPOSED]** The same quality rules apply.
- **[PROPOSED] Cons about consequences** ("that strike will cause civilian casualties and outrage") don't argue the action fails. They argue it has **costs**. The white cell treats them as shaping the *outcome* (side effects, track changes) rather than as −1s against success.

### 3.4 Secret COAs [CANON]

- Use these for **misdirection or conditional traps** only, e.g. decoy SAM sites, a honeypot network, booby-trapped port facilities. Do not use them for ordinary actions you'd simply rather hide.
- Each team may make **one secret COA per phase** (Phase II and Phase IV).
- To make one, post it in your team channel (§2.5) with a **precise trigger**. The other team can't give Cons against something it can't see.
- **During a turn**, announce aloud "We are making a secret COA." That is your COA for the turn.
- **During a planning phase**, post it before the phase ends: Phase I for Phase II's secret COA, Phase III for Phase IV's. Tell your logger in the brief or FRAGO. It doesn't use up a turn's COA, and no announcement is made. Time cost: none.
- The white cell resolves it **when the trigger occurs** and applies its own judgment in place of Cons. A trigger written too loosely doesn't fire. Precision is the player's job.

### 3.5 Arguing about actors [CANON]

| Actor type | Can you argue about it? |
| --- | --- |
| Your own forces | Yes. That's normal. |
| The opposing team's forces | **Yes.** Argue about their morale, readiness, maintenance, gaps. You can't give them orders. |
| A **player-controlled** actor's *decisions* (the other team) | **No.** You can't argue "[the other side] agrees to a ceasefire." Ask them in person in a parley during Prepare (§6.1). If they agree, it happens. |
| **White-cell-controlled** actors (non-player nations, populations, pirates, the press, weather) | Yes, through COAs ("A diplomatic delegation persuades [a neutral state] to grant basing because…"). The white cell adjudicates. Diplomatic COAs need no RFF (§6.2). |

---

## 4. Adjudication [CANON: white cell decides, dice by computer program; method PROPOSED]

**[CANON]** The white cell makes the final decision on probability of success and outcomes. **[CANON]** Dice are rolled with a **computer program**, not physical dice. The procedure below is **[PROPOSED]**. It uses Mouat's *weighted probability* method (2d6, 7+), the fastest method and the one he recommends for instructor-led games with junior students. The white cell needs it to resolve {{ word(n_teams) }} COAs in {{ mins(steps.res.min) }}.

### 4.1 Procedure (per COA)

1. **Screen.** Is the COA feasible within the turn's time, space, and the assets the team actually has (AFDP 5-0's "Feasible" test)? If not, the white cell rules it **impossible** (no roll) or **scopes it down** to what is feasible. Say so in one sentence.
2. **Automatic success?** If there were no credible Cons, or the case is overwhelming, it **succeeds without a roll**. Treat the result as **Success** (9–11 band). Mouat: sensible arguments should succeed unless challenged.
3. **Count modifiers** (cap the net total at **±4**):

   | Modifier | Value |
   | --- | --- |
   | Each **strong** accepted Pro | +1 (a single exceptionally compelling Pro may be +2) |
   | Each **strong** accepted Con | −1 (a single exceptionally compelling Con may be −2) |
   | Weak, vague, or duplicate reason | 0 |
   | **Planned** COA executed as briefed in Phase I (or Phase III FRAGO) and still valid | +1 |
   | **Starting conditions or ongoing effects** that apply (`scenario/00-overview.md` §5) | ±1 each, as listed |
   | Each asset used in the COA that is **Degraded** (a package's counters count separately) | −1 each |

4. **Roll 2d6 in the dice program**, add the modifiers, and read the band:

   | Modified total | Result | Meaning |
   | --- | --- | --- |
   | **≤ 3** | **Critical failure** | Fails, and something goes wrong: losses, exposure, a backlash, a track moves against the actor. |
   | **4–6** | **Failure** | Doesn't happen, or has no meaningful effect. Assets may be Degraded if it was a risky combat action. |
   | **7–8** | **Partial success** | Happens, but limited or at a cost. Example: target Degraded instead of Destroyed, or success with own losses or a political cost. |
   | **9–11** | **Success** | Happens as argued. |
   | **≥ 12** | **Exceptional success** | Happens, plus a bonus. Example: an extra effect, a new established fact the team can build on, or a track moves in its favor. |

5. **Narrate in one or two sentences**, giving the reason for the result (the winning Pro or Con). Pros and Cons are valuable here because they explain *why* something failed.
6. Successful results become **established facts**. Loggers don't log every COA. They keep only the placement form (App. B).

### 4.2 Interacting COAs [CANON]

All COAs are briefed before any is resolved, so **they happen simultaneously across the {{ days(game_days, adj=True) }} turn window**. Because a team that briefs later cannot prevent an earlier team's COA from being rolled, a reactive move is resolved as an interacting or directly opposed COA.

- **Independent COAs** (different places or effects): resolve each normally, in briefing order ({{ first_team }}'s first).
- **Interacting COAs** (one affects the other's odds, e.g. BLUEFOR disperses its SAMs while REDFOR strikes them): fold the interaction into the modifiers. A well-timed counter-move is a strong Pro or Con even if nobody said it out loud.
- **Directly opposed COAs** (both can't succeed, e.g. both sides try to seize the same port): use an **opposed roll**. The program rolls 2d6 for each side, each side adds its own modifiers, and the higher total wins. On a tie, both are **Partial**, the situation stays contested, and the white cell describes a stalemate. With more than two teams, every team whose COA is opposed rolls at once and the highest total wins; a tie for highest leaves those teams Partial.

### 4.3 Time pressure

- **[PROPOSED]** If the {{ mins(steps.res.min) }} run out, the lead adjudicator makes the call on the spot. Resolving fast matters more than resolving perfectly.
- **[PROPOSED] Contentious calls** happen when both teams keep arguing. Don't debate. Either make the call, or take an estimative vote.
- **[CANON] Estimative vote.** For a contentious call (both teams keep arguing, or the white cell can't settle the modifiers in time), the lead adjudicator may skip counting modifiers and call a **10-second estimative vote**. Each white cell member shows 1–5 fingers for how likely the COA is to work. The white cell takes the **median**, and the dice program rolls against it:

  | Vote | 1 | 2 | 3 | 4 | 5 |
  | --- | --- | --- | --- | --- | --- |
  | Meaning | Remote | Unlikely | Even chance | Likely | Almost certain |
  | Happens on | 11+ on 2d6 (8%) | 9+ (28%) | 50% (percentage roll) | 6+ (72%) | 4+ (92%) |

  If it happens, treat it as a **Success**. If not, a **Failure**. The lead adjudicator announces "estimative vote" before voting, so players know which method decided the call. Time cost: about 10 seconds, and it usually saves time.
- **[CANON] No recalculation.** Because the timing is strict, an objection raised late (after its slot, or after the roll) **is not considered**, and a result is not re-run once announced.

### 4.4 Fog of war [CANON: white cell introduces fog of war; mechanics PROPOSED]

- Opponent assets marked **hidden** in the scenario stay off the central map until found by a successful ISR COA, revealed by their own use, or disclosed by an inject. Mentioning a hidden asset in a COA or in a Pro or Con counts as using it, whether or not the COA succeeds (White Cell Handbook §2.3).
- **RFI answers** reflect what your existing intelligence would plausibly know. That may be incomplete, uncertain ("unknown"), or wrong if the enemy has succeeded at deception. RFIs never reveal the enemy's secret objectives or secret COAs.
- **Injects** (§7) add friction: weather, civilian events, leaks, third-party moves.

### 4.5 Split counters [CANON: one counter per part; details PROPOSED]

An asset spread over several zones is printed as **one counter per part**, lettered after its ID. The letters are parts of the same asset, not new IDs.

| Asset (example) | Parts | Starting zones |
| --- | --- | --- |
| B-07 Early-warning radar network | B-07a, B-07b, B-07c | Z10, Z11, Z12 |
| B-06 NASAMS ×3 (hidden) | B-06a, B-06b, B-06c | BLUEFOR picks a zone for each part in Phase I and tells its logger |

The scenario lists its split counters in the packet force tables and in `scenario/data/assets.csv` (`parts` and `zone` columns; see `AGENTS.md`).

- Each part moves, is found, and is Degraded or Destroyed **on its own**. A strike on a zone touches only the parts in that zone.
- A COA, Pro, or Con may name one part ("B-07b") or the whole asset ("B-07", meaning every part). For a hidden asset, naming one part reveals only that part. Naming the asset without a letter reveals all of its parts.
- Time cost: none. The white cell already rules by zone.

---

## 5. Requests: RFIs and RFFs [CANON: one limit per turn for RFIs and RFFs combined, and a larger one in Phase I, due before it ends; the numbers are in `game.toml` `[turns]`]

| | RFI – Request for Information | RFF – Request for Forces |
| --- | --- | --- |
| Purpose | Ask what your side knows: enemy disposition, weather, a third party's stance, civilian situation | Ask your national command for more assets, or for authorities beyond the rules of engagement. Diplomacy needs no RFF (§6.2). |
| Limit | **Up to {{ requests }} requests per turn in total, RFIs and RFFs combined** (Phase I: {{ planning_requests }} due at minute {{ request_deadline }}, see §2.3) | (shared with RFIs) |
| Format | One question per Slack message, ≤ 1 sentence | Asset (from the scenario's RFF pool or a free-text request), destination, and purpose |
| Counts as COA? | No | No |
| Debate? | No | No |
| White cell response | Short written answer in a thread under the request, posted by the start of the next Prepare step | Approve, approve partially, or deny, with the **arrival turn** (`scenario/00-overview.md` §6). National politics shape approval (scenario tracks, e.g. Domestic Will). |

- **[PROPOSED]** A force that arrives by RFF, or that an inject creates, and has no printed counter goes on a **blank counter** ({% for s in sides %}{{ s.prefix }}-, {% endfor %}or grey X- for third parties) from the white cell counter sheet. The white cell writes a new ID on it (free-text RFFs from {% for s in sides %}{{ s.prefix }}-50{% if not loop.last %}, {% endif %}{% endfor %}; inject forces from X-01) and the zone.
- **[CANON] Arrival turns.** **N** is the turn the RFF is submitted (Phase I RFFs count as Turn 1). The white cell rules on it in that turn's resolve step. An arrival of N+1 means the next turn, N+2 the turn after that, and so on.
- **[CANON] Usable on arrival.** A force can be used in the COA of the turn it arrives. The white cell announces it and places its counter in the resolve step just before the arrival turn, so the team can plan with it during Prepare. Example: a team submits an RFF on Turn 3 for an N+1 asset and it is approved. It arrives on Turn 4 and can be part of the Turn 4 COA. An N+0 grant (new authorities) takes effect when approved, so it applies from the next COA. Time cost: none.
- **[CANON]** Forces that arrive by RFF are placed in their side's main base zone unless the RFF names another destination. The scenario names each side's main base zone (`scenario/00-overview.md` §6). Authorities and intelligence sharing get no counter on the map.
- **[CANON] Approvals stand.** Once the white cell approves an RFF or grants something through a COA (basing, recognition, authorities), it is not rescinded when the track or condition that allowed it later changes. Approved forces still arrive, and grants stay. Only another team can undo them, with a successful COA (a strike, or interdiction in transit). Time cost: none.
- **[PROPOSED]** A big RFF (a carrier strike group, a ground brigade, new authorities like permission to strike the enemy capital) is a **political** decision. The white cell may deny it, or demand a successful COA first to build the case.

---

## 6. Negotiation and diplomacy [CANON]

### 6.1 Parleys between teams

- **What it is.** A parley is a short face-to-face talk between two teams (or more, §2.6), held during **Prepare**. In the game world it stands for talks between their governments during the turn's {{ days(game_days) }}, whether direct, through a back channel, or through a mediator. It is the **only** way to get a decision from another team, because no COA can argue that a player-controlled actor agrees (§3.5).
- **What it is not.** It is not a COA and not a request. It has no roll and no Pros or Cons, doesn't count against the {{ requests }} requests, and needs no RFF (§6.2). It is not a way to talk to white-cell actors (third-party states, the press, populations). Those are persuaded with COAs.
- **Asking for one.** Either team's flight commander (or a delegate) asks the lead adjudicator. The lead adjudicator authorizes it and runs the parley timer in the timer program. A team asked to parley may decline.
- **Who and how long.** The flight commander (or a delegate) from each team meets at the white cell end of the table, and the lead adjudicator listens. The rest of each team keeps working on its COA. A parley lasts **≤ {{ parley }} min** (`game.toml` `[schedule]` `parley`), taken out of Prepare. Time cost: none, since Prepare doesn't get longer.
- **Closing it.** At the end, each side states aloud what it agreed to, and the lead adjudicator repeats the deal back. The logger notes it, including what each side says it agreed, on the objective status card (White Cell Forms). Players don't write agreements down.
- Whatever the players agree in person **happens** (no roll). The white cell applies its effects (counters, tracks, objective status card) in this turn's resolve step. Examples: prisoner exchanges, a local ceasefire, an agreement to open talks, a deal to let shipping through.
- Agreements are not self-enforcing. Breaking one is allowed, but it is an **established fact** that others can use in Pros and Cons (credibility and legitimacy), and the white cell may move tracks.
- If the sides later dispute what was agreed, the lead adjudicator decides, using the logger's note.

### 6.2 Diplomacy needs no RFF

- **Each team speaks for its whole government.** For diplomacy, the team is the national leadership: the President, the foreign ministry, and the commanders at once. It needs no RFF and no approval from the President or national command to negotiate or to make a diplomatic COA.
- This covers parleys and any agreement made in one, and diplomatic COAs aimed at white-cell actors: basing or overflight talks, recognition campaigns, mediation, pressure on a third party's backer, an offer of talks.
- **RFFs for authorities cover military limits only:** the directives in `scenario/00-overview.md` §7 that require national authority or approval, such as striking leadership targets in the enemy capital, putting ground forces on enemy soil, or engaging a third party's forces. An agreement that commits a team to one of those acts (e.g. ground forces in the other side's country as peacekeepers) still needs that authority before the forces act. A neutral state's consent to operate in its territory comes from a diplomatic COA, not an RFF.
- **White cell:** don't deny or scope down a diplomatic COA because no RFF was filed. Its odds come from Pros, Cons, and the tracks as usual. If a team posts an RFF asking permission to negotiate, the logger answers "No RFF needed: diplomacy is within your authority (Rules §6.2)," and it doesn't count against the request limit. Time cost: none.

---

## 7. Injects [CANON: white cell may deliver injects; content in scenario]

- The **kickoff inject** starts the war at the end of Phase I. It is **[CANON]** in function, and its wording is in `scenario/whitecell-injects.md` §1.
- **[CANON]** The lead adjudicator may deliver **at most one inject per turn**, during the resolve step. **[PROPOSED]** Injects should (a) add fog and friction, (b) force teams to adapt their plan, or (c) **bound behavior** that is going off the rails. Example: "[REDFOR's] legislature passes a resolution forbidding strikes on [the enemy capital]" **[CANON tool]**.
- **[CANON]** No event cards. Random events come only through white cell injects.
- **[PROPOSED] Consequence management:** at the end of each resolve step, the white cell states ongoing effects (refugees, burning port, market panic). Ongoing effects persist and can give ±1 to related COAs **until a successful COA removes them**.

---

## 8. White Cell Adjudication Guide [PROPOSED unless tagged]

### 8.1 Lead adjudicator checklist (per turn)

1. Start the timer program for Prepare ({{ clock(steps.prep.min) }}). Check that last turn's RFI answers are posted in each team channel.
2. At the end of Prepare, close requests: count the first {{ requests }} request posts per team (§2.5).
3. Call each team's COA in briefing order ({% for s in sides %}{{ s.label }}{% if s.coa %} {{ clock(s.coa.min) }}{% endif %}{% if not loop.last %}, then {% endif %}{% endfor %}). Don't allow interruptions.
4. Start the Cons prep. Call each team's Cons in the order of the turn clock (§2.2).
5. Resolve each COA: screen → auto-success? → modifiers → dice program → narrate.
6. Rule on RFFs and announce arrivals. State ongoing effects. Deliver an inject (optional).
7. Loggers move the map counters and tracks and update the placement forms. Start the next turn.

### 8.2 Judging reasons quickly

Ask four questions about each reason:

1. **Is it true?** It must be an established fact, a listed capability, or a reasonable assumption.
2. **Is it relevant** to *this* action and *this* effect?
3. **Is it new,** not a restatement of another reason already counted?
4. **Does it matter?** Would a real commander care?

Four yeses make it strong (±1). An exceptional reason, one that is decisive by itself, is ±2. Otherwise it's 0.

### 8.3 Doctrinal yardsticks (use them, and name them out loud in narration so cadets learn them)

- **COA validity (AFDP 5-0):** Feasible, Acceptable (risk vs. gain), Suitable (meets intent and objectives), Distinguishable, Complete. A COA that fails *Feasible* doesn't get rolled. One that fails *Acceptable* may succeed, but with a heavy cost.
- **Tenets of airpower (AFDP 3-0):** mission command, flexibility and versatility, synergistic effects, persistence, concentration, priority, balance.
- **Principles of joint operations (AFDP 3-0 / JP 3-0):** objective, offensive, mass, maneuver, economy of force, unity of command, security, surprise, simplicity, restraint, perseverance, legitimacy (plus unity of effort, as AFDP 3-0 lists it).
- **USAF core functions (AFDP 3-0):** Air Superiority, Global Precision Attack, Rapid Global Mobility, Global ISR, Command and Control.
- **ACE (AFDP 3-0 App. C):** dispersal to a network of smaller locations complicates enemy targeting, but it needs C2, logistics, and base defense to work.

### 8.4 Keeping the game on the rails

- **Over-reach** ("we invade and take their capital this turn"): scope it down to what is feasible in {{ days(game_days) }} with the assets on hand, or rule it impossible.
- **Laundry lists:** hold teams to 3 reasons and one action.
- **Off-the-rails behavior [CANON tool]:** use an inject that sets a national directive restricting it, or kill the COA outright.
- **Dominant players and nit-picking:** courtroom rules. "You had your slot." Move on.
- **[CANON] Behind schedule:** shorten **Prepare** (e.g. to 4 min, with the timer's Prepare menu; `game.toml` `[schedule]` `flex_options`). **Never cut the Cons**, which are where the learning happens.
- **[CANON] Late objections:** not recalculated (§4.3). Move on.

### 8.5 Several tables at once

If the game runs at several tables simultaneously, every white cell uses this document and the scenario document unchanged. They should agree beforehand on how generous to be with auto-success and on how big a single COA can be, so the tables stay comparable.

---

## 9. Game roles

### 9.1 Players (the teams)

- **[CANON]** Each team has an assigned **flight commander**. Who is assigned and when command changes hands is set in `EVENT-SETUP.md`.
- **[CANON]** **The team builds the rest of its own structure** during Phase I: who handles operations, intel, logistics, briefing, and so on. The rules don't prescribe staff roles. (Unless the scenario splits the team into cells, §9.4.)
- **[CANON]** Players **may use computers, online searches, and AI** during play, and every player may bring a laptop. The decisions and the briefs must still be the team's own.

### 9.2 White cell [CANON]

| Role | Per game | Job |
| --- | --- | --- |
| **Lead adjudicator** | 1 | Runs the timer program, gives injects, runs the dice program, final adjudication authority |
| **Logger** for each team ({{ teams }}) | 1 per team | Receives its team's Phase I brief and Phase III FRAGO. Keeps that team's placement form (App. B). Moves that team's counters. Watches the team's channel, counts its requests, and posts the lead adjudicator's answers there (§2.5). |

### 9.3 End of game [PROPOSED]

After the final turn's resolution, the white cell states the end state (map and tracks) and scores each team's three objectives as Achieved, Partial, or Not achieved, using the criteria in §3 of each team packet (`scenario/<team id>-packet.md`). The loggers record the result.

### 9.4 Cells within a team [PROPOSED]

A scenario may split a team into **cells** under its flight commander, for example an intelligence cell, a communications cell, and an air component (`game.toml` `[[side.cell]]`). Use cells when the point of the exercise is coordination inside a staff, or to give a large team (more than about 8 players) defined jobs. Without cells, §9.1 stands.

- **One COA per team.** Cells don't make their own COAs. Each cell proposes the COA it thinks matters most, and the flight commander chooses **one** for the team (Mouat: several players representing an actor work up alternative arguments, and the team leader chooses). A COA may use assets from any cell. The commander names the briefer.
- **Choosing cells.** `presets/cells.toml` has seventeen, from an intelligence cell to a legal cell, each with a brief for its players (`presets/README.md` §2). Two to four a team works best, chosen so their concerns pull against each other.
- **What a cell has.** A lead (a role title), a one-line job, and optionally its own brief (`handouts/<team>/cells/<cell>.md`) and its own assets (the `cell` column of `scenario/data/assets.csv`; the cell's short name prints on those counters). A cell brief may give the cell its own concern or an objective that pulls against another cell's, so the team has to agree before it acts ("a house divided", in Mouat's term). Keep it to one page.
- **Requests and Slack.** The team's {{ requests }} requests a turn are shared by its cells, and the team channel stays the record (§2.5). A team may open cell threads in its channel; the logger counts requests across the whole team.
- **What it is not.** Cells are not extra actors: they don't get turn slots, Cons slots, or their own objectives on the score sheet. A sub-team that needs its own COA every turn is a team (§2.6).
- Time cost: none. Cells work inside Prepare.

---

## 10. Worked example turn [PROPOSED, illustrative]

*This example uses a generic coastal scenario: Blueland (BLUEFOR) holds a strait coast, and Redland (REDFOR) is trying to reopen it. Replace it with a Turn 1 from your own scenario, using real asset IDs from the packets, once the forces are settled. These numbers are an illustration, not a prediction.*

**BLUEFOR COA ({{ clock(sides[0].coa.min) }}):** "Our Mark VI patrol boats (B-12) and maritime militia (B-18), covered by our Harpoon coastal-defense battery (B-08), establish an armed inspection zone across the Narrows, **in order to** move Sea Lane Access from Restricted to **Closed**. It works because: (1) the Narrows are only ~25 miles wide and sit completely inside the battery's ~75-mile anti-ship missile umbrella, so Redland surface ships can't escort freighters through safely; (2) the militia's armed boats blend in with coastal traffic and swarm any ship that tries to run the Narrows, giving us *surprise* and *mass*; (3) closing the strait pressures Redland's economy without us firing first on Redland warships."

**REDFOR COA ({{ clock(sides[1].coa.min) }}):** "A strike package of F-35As (R-01) and an EC-37B Compass Call (R-10), refueled by KC-46s (R-05), strikes Blueland's Patriot battery (B-04) covering the Narrows, **in order to** destroy it and open the air over the strait for our ISR. It works because: (1) the F-35A is a stealth aircraft built to penetrate integrated air defenses; (2) Compass Call jamming cuts the battery off from its early-warning radar network (B-07), which is *synergistic effects*; (3) the kickoff inject gives us *surprise*, because the battery hasn't had time to relocate."

**REDFOR Cons → BLUEFOR ({{ clock(sides[1].cons.min) }}):** "(1) Our RC-135 (R-07) and P-8A (R-14) have been watching the Narrows since Phase I and will track the patrol boats' formations and holds. (2) Shutting down an international strait by threatening merchant shipping will turn International Opinion against Blueland."

**BLUEFOR Cons → REDFOR ({{ clock(sides[0].cons.min) }}):** "(1) Patriot is a mobile system, and our Phase I brief said we'd relocate the battery at the outbreak of war. (2) Redland's fighters have to fly ~600 miles each way, so they depend on tankers."

**White cell resolution ({{ clock(steps.res.min) }}):**

- **BLUEFOR inspection zone:**
  - Pros 1 and 2 are strong (+2). Pro 3 is about effect, not success, so it counts 0 here.
  - REDFOR Con 1 is strong (−1), because the maritime ISR presence is an established fact. REDFOR Con 2 is about consequences, so it doesn't affect success but will shape the outcome.
  - Closing the Narrows was a planned COA in BLUEFOR's Phase I brief and is still valid (+1).
  - A starting condition says Blueland's regular forces and militia distrust each other, and this COA needs both (−1).
  - Net **+1**. Program rolls 6; 6 + 1 = **7 → Partial success.** The zone is declared and shipping halts, moving Sea Lane Access to **Closed**, but Redland's maritime patrol tracked the boats' patrol sectors (established fact). Consequence: International Opinion moves 1 toward Redland.
- **REDFOR strike:**
  - Pros 1 and 2 are strong (+2).
  - BLUEFOR Con 1 is strong (−1), because the relocation was briefed before the war, and it cancels REDFOR Pro 3 (surprise counts 0).
  - BLUEFOR Con 2 is true, but the KC-46s are part of the package, so it counts 0.
  - Net **+1**. Program rolls 9; 9 + 1 = **10 → Success.** The battery is caught during relocation and **Destroyed**. Counter removed.
- **RFFs:** REDFOR's request for an additional tanker detachment is approved, arriving Turn 2.
- **Ongoing effect:** "Inspection zone in the Narrows": −1 to any COA moving shipping through the strait until the coastal battery and patrol boats are suppressed.

---

## 11. Open decisions for the designer

Carried over from the first game played with these rules, where the designer settled them (re-confirm each one for a new scenario, or change it here): written traffic over Slack instead of paper, with briefs still given aloud: COAs and Cons in each group's public channel, requests, answers, and secret COAs in private team channels (§2.5), the estimative vote for contentious calls (§4.3), fixed briefing order (the first team in `[[side]]` first), simultaneous COAs within a turn, computer dice, timer program, oral five-paragraph Phase I brief, 4 combined Phase I requests due at minute 12, Phase III 1-minute FRAGO with up to 2 planned COAs, 3 combined requests per turn, no COAs in Phase I, secret COAs, cut Prepare not Cons, no late recalculation, flight-commander-only role assignment, no debrief content in the rules, no event cards, the term FRAGO (not FRAGORD), loggers keep a placement form instead of logging every move, one counter per part for assets spread over several zones (§4.5), RFF arrivals placed in each side's main base zone unless the RFF names another destination (§5), negotiation and diplomacy as written in §6 (parleys of ≤ 2 min during Prepare, and no RFF needed for diplomacy), RFF arrival turns counted from the turn submitted, with forces usable on arrival (§5), requests after the deadline not answered (§2.5), arguing about actors (§3.5), interacting and opposed COAs (§4.2), and at most one inject per turn (§7).

Open for every new scenario:

| ID | Decision | Draft assumes |
| --- | --- | --- |
| O1 | Adjudication details: the five result bands and the ±4 modifier cap (§4.1) | As written |
| O2 | Length of a turn in game time (§2.1) | About {{ days(game_days) }} (`game.toml` `game_days`) |
| O3 | The run of show (§2.1): the phases, their order and lengths, and the number of turns in each, which follow from the time the event has (`EVENT-SETUP.md` §3). Set in `game.toml` `[[block]]`. | The default four phases, with 4 and 3 turns |
| O4 | Slack channel prefix and group names (§2.5) | `[prefix]-group1-[room]` |
| O5 | Replace the generic worked example (§10) with one from the scenario | Generic example |
| O6 | More than two player teams (§2.6): whether to add one, and the Cons rule for three or more (up to 3 in total per team, spread as it likes) | Two teams |
| O7 | Cells within a team (§9.4) | No cells |

**From a check against Mouat's *Practical Advice on Matrix Games* v15** (`references/PracticalAdviceOnMatrixGames.pdf`). Most of these rules follow his advice: Pros and Cons, one action with a measurable effect, weighted probability on 2d6, automatic success when unopposed, established facts against reasonable assumptions, secret arguments for misdirection only, three layers and three-argument big projects, long-term arguments, free announcements, consequence management, negotiation in person, courtroom order, and the estimative vote for contentious calls. These are where the rules differ from his advice or leave it out. Each is a decision for the designer; the recommendation is in the last column.

| ID | Decision | Mouat's advice | Recommendation |
| --- | --- | --- | --- |
| O8 | Who votes in an estimative vote (§4.3) | Everyone present votes, independently and at the same time, and the median is taken; the arguing player may be kept out so no one votes for themselves (pp. 9–10, 13). The vote crowdsources the odds. | Let the players of the teams that didn't make the COA vote too, with the white cell, all showing fingers on the lead adjudicator's count. Time cost: none. Three white cell members alone are a small crowd. |
| O9 | Late objections (§4.3) | If a point comes late because the facilitator rushed the game, pause, apologize, and re-run the adjudication (p. 35). | Keep "no recalculation", except when the white cell itself cut a slot short: then hear the point and re-run once. Time cost: rare, under a minute. |
| O10 | A Turn Zero rehearsal (§2.1) | With inexperienced players, have two opposed actors make example arguments and discuss them before the game starts (pp. 14, 38). | Under the basic rules, add a 5-minute Turn Zero step to Phase I in which the lead adjudicator walks through the worked example (§10) with one Pro and one Con from each team. Time cost: 5 minutes, once. |
| O11 | Debrief content (`EVENT-SETUP.md` §3) | Each actor reads out its objectives and says why it did or didn't achieve them; then ask the room "who won?" If everyone agrees, look closer (p. 37). | Add those two prompts to the debrief steps in `game.toml` and the White Cell Handbook. The rules themselves stay free of debrief content. Time cost: none; it fits the existing debriefs. |
| O12 | Non-military markers on the map | Players argue about what they can see: if every counter is military, the arguments will be too. Put political, economic, social, information, and infrastructure effects on the map as markers (pp. 27, 36). | Print a sheet of generic effect markers (protest, refugees, outage, cyber intrusion, media story, sanctions) with the white cell's blank counters, and use them for ongoing effects (§7). Time cost: none. |
| O13 | Loose secret COA triggers (§3.4) | The facilitator makes sure the trigger is tight when the secret argument is written; if one slips through, the player makes an extra argument for why it fires (pp. 19–20). | When a secret COA is posted, the logger reads the trigger and asks for a fix in the thread if it is loose. A trigger that is still loose doesn't fire, as now. Time cost: none. |
| O14 | Several weak reasons (§4.1, §8.2) | Two or three weaker reasons may together count as one (p. 7). | Keep weak reasons at 0. Adding them up costs the white cell time it doesn't have, and the rule rewards laundry lists. |
| O15 | Number of turns (§2.1) | At least 6 turns, so players live with their decisions through two cycles of action, reaction, and counteraction (pp. 10, 17). | The default has 7. Keep 6 or more in any run of show; `python3 tools/schedule.py --check` warns below 6. |

## Appendix A — Phase I brief and Phase III FRAGO formats (AFDP 5-0 App. E) [CANON: format; outline PROPOSED]

**Phase I brief:** an **oral** brief to the team's logger, ≤ 3 minutes (minutes 15–18 of Phase I). Nothing written is required, and teams don't have to follow this outline; it is here for reference. The logger notes the planned COAs.

```text
1. SITUATION   Enemy: what we think they will do (most likely / most dangerous).
               Friendly: our key assets and where they are.
2. MISSION     WHO does WHAT, WHEN, WHERE, and WHY (one sentence).
3. EXECUTION   a. Commander's intent — purpose, end state, acceptable risk.
               b. Concept of operations — how we get there, in phases.
               c. Planned COAs (up to 3): Turn 1 … Turn 2 … Turn 3 …
               d. Coordinating instructions — restraints and ROE we operate under.
4. SUSTAINMENT RFFs submitted, basing, what we're short of.
5. COMMAND & SIGNAL  How our team is organized; who decides and who briefs.
```

**Phase III FRAGO (in the last minute of Phase III):** an **oral** brief by the new Phase III–IV flight commander to the logger, ≤ 1 minute.

```text
1. SITUATION UPDATE  What changed in Phase II (key losses, tracks, enemy actions).
2. UPDATED INTENT    Adjusted purpose, end state, and acceptable risk for Phase IV.
3. PLANNED COAs      Up to 2 new planned COAs for Phase IV (Turns 5–7).
```

## Appendix B — Placement form (one per team) [PROPOSED]

Each logger keeps one placement form for its team (`handouts/whitecell/forms.md` §4). It records where things are **now**, not a history. Loggers don't log every COA, roll, or move. The form holds:

- the planned COAs from the Phase I brief (Turns 1–3) and the Phase III FRAGO (up to 2, Turns 5–7), each ticked when executed as briefed (for the +1 in §4.1);
- each hidden counter's zone, the turn it was revealed, and its state, with one line per part of a split counter, including any parts whose zones a team chooses in Phase I (§4.5);
- approved RFFs, with the turn each arrives and where it is placed;
- visible counters that have moved, been Degraded, or been Destroyed since the starting setup.

When something changes, cross out the old entry and write the new one. Ongoing effects and big-project progress go on the public ongoing-effects sheet (`handouts/whitecell/forms.md` §2). The tracks are kept in the timer and dice program's tracker, on the room's screen.

## Appendix C — Probability cheat sheet (2d6, need modified total ≥ 7)

| Net modifier | −4 | −3 | −2 | −1 | 0 | +1 | +2 | +3 | +4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Natural roll needed | 11+ | 10+ | 9+ | 8+ | 7+ | 6+ | 5+ | 4+ | 3+ |
| Chance of at least Partial success | 8% | 17% | 28% | 42% | 58% | 72% | 83% | 92% | 97% |

**Estimative vote → target (for §4.3):** 1 = Remote (needs 11+ on 2d6, 8%) · 2 = Unlikely (9+, 28%) · 3 = Even chance (percentage roll, 50%) · 4 = Likely (6+, 72%) · 5 = Almost certain (4+, 92%). These follow Mouat's cheat card (10/30/50/70/90%) as closely as 2d6 allows. The dice program has an estimative-vote roll.

## Appendix D — Doctrine crosswalk (game mechanic → doctrine)

| Game element | Doctrine | File |
| --- | --- | --- |
| Turn structure (COA → Cons → resolution) | Action–Reaction–Counteraction wargaming | AFDP 5-0 Ch 6, p. 43–44 |
| White cell COA screening | COA validity: Feasible, Acceptable, Suitable, Distinguishable, Complete | AFDP 5-0 Ch 5, p. 39 |
| Phase I brief | Modified five-paragraph order | AFDP 5-0 App. E |
| Commander's intent in the Phase I brief | Mission command principles; CC-DC-DE | AFDP 1-1 |
| Pros and Cons vocabulary | Tenets of airpower; principles of joint operations | AFDP 3-0 Ch 1; JP 3-0 |
| Asset tags | Five USAF core functions | AFDP 3-0 |
| Basing and dispersal COAs | Agile Combat Employment | AFDP 3-0 App. C |
| Phase I competition → war | Competition continuum | AFDP 3-0; AFDP 3-99 |
| Cross-domain COAs (space, cyber, EMS) | JADO principles | AFDP 3-99 |
| Overall method | Matrix games, Pros/Cons system | Mouat, *Practical Advice on Matrix Games* v15 (`references/PracticalAdviceOnMatrixGames.pdf`) |

## Appendix E — Glossary

| Term | Meaning |
| --- | --- |
| **COA** | Course of action: the one action a team argues for each turn |
| **Pro / Con** | Reason for or against a COA's success |
| **Established fact** | Anything in the briefings or created by a successful COA. It stays true until another COA changes it. |
| **Reasonable assumption** | Something any professional would accept without proof (trained troops beat untrained ones) |
| **RFI / RFF** | Request for Information / Request for Forces |
| **Inject** | A white cell event that changes the situation |
| **White cell** | The neutral control group: adjudicator and loggers |
| **{{ team_slash }}** | The player teams in this game (`game.toml` `[[side]]`). REDFOR and BLUEFOR are the defaults; a scenario may add more, e.g. GRAYFOR (§2.6). |
| **Cell** | A part of a team with its own lead and job, under the team's flight commander (§9.4) |
| **Counter** | A printed piece on the central map representing an asset or effect |
| **Track** | A numeric value, shown on the white cell's screen, for something abstract (opinion, stability) |
| **Degraded / Destroyed** | Asset states. A Degraded asset gives −1 when used. A Destroyed one is removed. |
| **DIME / PMESII** | Instruments of power / dimensions of effect. A checklist for non-kinetic ideas. |

## Appendix F — Notes for AI agents

See `AGENTS.md` for the file map, editing rules, secrecy rules, and ID conventions.
