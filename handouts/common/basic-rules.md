---
title: "Matrix Wargame — Basic Rules"
subtitle: "[Event] · [Month Year]"
short: "Basic Rules"
---

**Audience:** every player, REDFOR and BLUEFOR{% if rules == "full" %}, and especially anyone playing a matrix wargame for the first time{% endif %}. Nothing in it is secret. Released ASAP, before the scenario; scenario details in the examples are replaced with bracketed placeholders.

{% if rules == "full" %}

**This is a short version of the Player Rules Handbook,** for your first game. It covers everything you need to play. The white cell runs the game by the full rules, so a few things left out here (secret COAs, estimative votes) may still come up at the table. When they do, the white cell explains them, and §7 says where to read about them.

{% else %}

**These are the rules for this game.** It uses the basic rule set: everything you need to play is here.

{% endif %}

*All countries, people, and events in this scenario are fictional. All military systems are real U.S. systems, described with unclassified, approximate capabilities.*

| Part | What it covers |
| --- | --- |
| **1. The game in one page** | What you do and how you win the argument |
| **2. A turn** | The turn clock and an example turn |
| **3. COAs, Pros, and Cons** | How to build a COA and the reasons for and against it |
| **4. How the white cell decides** | Modifiers, the dice, and your odds |
| **5. Everything else** | Requests, counters, negotiation, roles, Slack, end of game |
| **6. Reference** | Doctrine in brief and a glossary |

<!-- pagebreak -->

## 1. The game in one page

1. **You win by arguing well.** There are no unit stats. Each turn your team proposes **one course of action (COA)** and gives **up to three reasons it will work** (Pros). The other team gives **up to three reasons it won't** (Cons). The **white cell** weighs the reasons, sets the odds, rolls two dice with a computer program, and tells you what happens.
2. **Two teams.** You are **REDFOR** or **BLUEFOR**. Your team's documents give you your forces, your intel, and **three secret objectives**. Don't show them to the other team.
3. **One COA per turn:** one main action with a measurable effect. Several assets can work together in it, but it can't do two unrelated things.
4. **Brief it out loud,** in this form:

   > "Our COA: **[action]** in order to **[measurable effect]**. It will work because: **(1)** … **(2)** … **(3)** …"

5. **Answer theirs** in your Cons slot:

   > "Their COA will fail or fall short because: **(1)** … **(2)** … **(3)** …"

6. **Good reasons are specific and true.** Point to your assets, the map, what already happened in the game, and doctrine.
7. **The odds.** With no strong reasons either way, a COA works on 7 or more on two dice (58%). Each strong Pro adds 1 and each strong Con subtracts 1.
8. **Requests.** Each turn you may post up to **{{ requests }} requests** in your team's secret Slack channel: questions (RFIs) or requests for more forces (RFFs).
9. **The day.** A planning phase comes first (no COAs: you build your plan and brief it to the white cell), then the turns. The Scenario Schedule gives the phases and times. **BLUEFOR always goes first** in a turn.
10. **No interrupting.** Speak in your slot, stay silent in theirs. A point you miss is lost.
11. **The point** is good decisions and clear reasoning under pressure: plan, brief, defend your choices, and adapt.

<!-- pagebreak -->

## 2. A turn

### 2.1 The turn clock

Each turn is **{{ mins(turn_min) }}** of real time and about **{{ days(game_days) }}** of game time. Both teams' COAs happen at the same time across those {{ days(game_days) }}. A timer on the room's screen runs the clock.

{{ turn_clock_table() }}

### 2.2 Example turn

*Scenario details are replaced with bracketed placeholders such as [FIGHTER JET].*

**REDFOR COA:** "A strike package of [FIGHTER JET]s and an [EW AIRCRAFT], refueled by [TANKER]s, strikes [AIR DEFENSE UNIT] **in order to** destroy it and open the air over [STRAIT AREA] for our ISR. It will work because: (1) the [FIGHTER JET] is a stealth aircraft built to get through air defenses; (2) [EW AIRCRAFT] jamming cuts [AIR DEFENSE UNIT] off from its early-warning radar, which is *synergistic effects*; (3) the war just started, so we have *surprise*."

**BLUEFOR Cons:** "(1) [AIR DEFENSE SYSTEM] is mobile, and our planning brief said we would move [AIR DEFENSE UNIT] when the war began. (2) Their fighters have to fly ~[XXX] miles each way, so they depend on tankers."

**White cell:** Pros 1 and 2 are strong (+2). Con 1 is strong (−1), because the move was briefed before the war, and it also cancels Pro 3 (no surprise). Con 2 is true, but the tankers are part of the package, so it counts 0. **Net +1.** The program rolls 9, and 9 + 1 = **10, a Success.** [AIR DEFENSE UNIT] is caught on the move and is **Destroyed**.

**What to take from it:** specific Pros win, and the best Cons attack the reasons, not the goal.

## 3. COAs, Pros, and Cons

### 3.1 Building a COA

A COA has two parts:

1. **Action:** who does what, where, with which assets.
2. **Measurable effect:** what will be true on the map or the tracks if it works, e.g. "[AIR DEFENSE UNIT] destroyed" or "[SHIPPING TRACK] moves to Open."

**One action, one effect.** A strike package of several aircraft is one action. Two unrelated things are two COAs, so pick one. Choosing priorities is the point.

**Some effects take more than one turn.** A hidden target has to be found before it can be struck, and a coalition takes more than one meeting. The white cell tells you up front how many successful COAs it takes (never more than 3). An effect that can't finish in {{ days(game_days) }}, such as a blockade, starts on success and keeps going until someone stops it.

**Think beyond kinetic.** Diplomatic, information, cyber, economic, logistics, and deception COAs are all valid and often stronger. Run through **DIME** (Diplomatic, Informational, Military, Economic) when you need an idea. Your team speaks for its whole government, so you can make a diplomatic COA without asking anyone's permission.

**Arguing about others.** You can argue about the other team's forces (their tired crews, their radar gap). You can't argue that the other team *agrees* to something: ask them in person (§5.3).

### 3.2 Strong reasons

Before you give a Pro or a Con, check it the way the white cell will:

1. **Is it true?** Something in the briefings, a listed capability, something that happened earlier in the game, or an assumption any professional would accept.
2. **Is it relevant** to *this* action and *this* effect?
3. **Is it new,** not a restatement of a reason already given?
4. **Does it matter?** Would a real commander care?

Four yeses make a strong reason, worth +1 or −1; a single decisive one can be worth 2. Weak, vague, or repeated reasons are worth 0, and three weak reasons are worse than one strong one because they used up your time.

**Common calls:**

- Only the first 3 reasons count.
- A Pro about why the effect *matters* ("this hurts their economy") counts 0. It says why the COA matters, not why it works.
- A Con about *costs* ("this will cause civilian casualties") doesn't change the odds, but the white cell uses it to shape what happens.
- A Con that answers a Pro cancels it. Neither counts.
- Doctrine counts only when you say how it applies.
- Every asset in the order of battle has a stated limitation. Those are your Cons.
- Your intel reports may be wrong. Confirm the important ones with an RFI before you build a Pro on them.

## 4. How the white cell decides

1. **Screen.** A COA that can't be done in {{ days(game_days) }} with the assets you have, where they are, is ruled impossible or scaled down.
2. **Automatic success.** An obviously sound COA with no credible Cons succeeds without a roll.
3. **Count modifiers** (the total is capped at ±4):

   | Modifier | Value |
   | --- | --- |
   | Each strong Pro | +1 (a decisive one +2) |
   | Each strong Con | −1 (a decisive one −2) |
   | Each **Degraded** asset used in the COA | −1 |
   | Ongoing effects or starting conditions the white cell has announced | ±1 each |

4. **Roll two dice,** add the modifiers, and read the result:

   | Total | Result | Meaning |
   | --- | --- | --- |
   | **≤ 3** | **Critical failure** | Fails, and something goes wrong |
   | **4–6** | **Failure** | Doesn't happen, or has no real effect |
   | **7–8** | **Partial success** | Happens, but limited or at a cost |
   | **9–11** | **Success** | Happens as argued |
   | **≥ 12** | **Exceptional success** | Happens, plus a bonus |

5. **Narrate.** What succeeds becomes an **established fact** that both teams can build on later.

**Your odds at a glance**

| Net modifier | −4 | −3 | −2 | −1 | 0 | +1 | +2 | +3 | +4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Chance of at least Partial | 8% | 17% | 28% | 42% | 58% | 72% | 83% | 92% | 97% |

**A plan pays off.** A COA your team briefed in its planning phase, carried out as briefed and still valid, earns +1.

**When the two COAs collide.** Both COAs happen at the same time, so they can affect each other. The white cell folds that into the odds (moving the SAMs you are striking counts as a Con even if nobody said it), or, if both can't succeed, rolls them against each other: the higher total wins.

**No do-overs.** An objection raised after its slot isn't considered, and a result isn't re-run once announced.

## 5. Everything else

### 5.1 Requests

| | RFI – Request for Information | RFF – Request for Forces |
| --- | --- | --- |
| What | A question about the situation | More assets, or authorities beyond your rules of engagement |
| Answer | In a thread under your post, by the next Prepare | Approved or denied, with the turn the forces arrive |

- **Up to {{ requests }} per turn, RFIs and RFFs combined** ({{ planning_requests }} in Phase I). One Slack message per request, posted in your team channel by the end of Prepare. Late or extra requests aren't answered.
- Reinforcements take time: the ruling says which turn they arrive, and you can use them in that turn's COA.
- You don't need an RFF to negotiate or make a diplomatic COA.

### 5.2 Counters

- Each asset is a counter: **Ready**, **Degraded** (−1 when used), or **Destroyed** (removed).
- **Visible** counters are on the map for both teams to see. **Hidden** counters stay on your team sheet until the enemy finds them or you use them. Naming a hidden asset in a COA, Pro, or Con counts as using it, and it then goes on the map.
- **Split counters.** An asset spread over several zones has a lettered counter in each (B-07a, B-07b). Each part moves and takes damage on its own. Name one part, or the whole asset (B-07) to mean every part.
- **Injects** are events the white cell adds (weather, leaks, third countries acting), at most one per turn.

### 5.3 Negotiation

During Prepare, your flight commander may ask the lead adjudicator for a **parley**: up to {{ mins(parley) }} face to face with one person from the other team. Whatever you both agree **happens**, with no roll. You can break a deal later, but the broken deal becomes an established fact the other side can use.

### 5.4 Roles and Slack

- Your **flight commander** leads the team, makes the final call, and briefs. Everyone else takes whatever job the commander needs: operations, intel, logistics, briefing.
- The **lead adjudicator** runs the clock and the dice and has the final say. A **logger** for each side hears briefs and moves counters.
- Bring a laptop. Post your COA, Pros, and Cons in your **group channel** (both teams see it), and your requests in your **team channel** (only your team and the white cell see it). Use asset IDs (R-01, B-07). Only what your briefer says aloud counts; the post is the written record.

### 5.5 End of game

After the last turn the white cell scores each team's three secret objectives as **Achieved**, **Partial**, or **Not achieved**. The two sides' objectives aren't always opposed, so both teams can achieve something. Talking to the other team can pay off.

## 6. Reference

### 6.1 Doctrine in brief

Cite these by name in your reasons, and say *how* they apply.

- **Tenets of airpower** (AFDP 3-0): mission command, flexibility and versatility, synergistic effects, persistence, concentration, priority, balance.
- **Principles of joint operations** (AFDP 3-0, JP 3-0): objective, offensive, mass, maneuver, economy of force, unity of command, security, surprise, simplicity, restraint, perseverance, legitimacy.
- **Is your COA valid?** (AFDP 5-0) Can we do it with what we have (feasible)? Is it worth the risk (acceptable)? Does it move us toward our objectives (suitable)?

{% if rules == "full" %}

The Player Rules Handbook §3.1 explains each one.

{% endif %}

### 6.2 Glossary

| Term | Meaning |
| --- | --- |
| **COA** | Course of action: the one action a team argues for each turn |
| **Pro / Con** | A reason for or against a COA's success |
| **Established fact** | Anything in the briefings or created by a successful COA |
| **RFI / RFF** | Request for Information / Request for Forces |
| **White cell** | The neutral control group: the lead adjudicator and loggers |
| **Inject** | A white cell event that changes the situation |
| **Counter** | A printed piece on the map for an asset or effect |
| **Track** | A value on the white cell's screen for something abstract (opinion, stability) |
| **DIME** | Instruments of power: Diplomatic, Informational, Military, Economic |
| **ISR** | Intelligence, surveillance, and reconnaissance |

{% if rules == "full" %}

## 7. What the full rules add

The Player Rules Handbook has the complete rules, and this game uses all of them. These are the parts left out or cut short here. Read them once you're comfortable with the basics; the white cell explains any of them at the table when it comes up.

| Rule | What it does | Where |
| --- | --- | --- |
| **Secret COAs** | One hidden, triggered COA per phase, for traps and misdirection | Player Rules Handbook §2.4 |
| **Big projects, layers, and long-term COAs** | The details, and public announcements | Player Rules Handbook §2.2 |
| **Interacting and opposed COAs** | How the white cell decides which case applies, and ties | Player Rules Handbook §2.7 |
| **Estimative vote** | A quick white cell vote in place of counting modifiers when a call is too close | Player Rules Handbook §2.7 |
| **Parley details** | Who parleys, how a deal is closed, and what a broken deal costs | Player Rules Handbook §2.6 |
| **RFF details** | Arrival turns, where new forces arrive, and big political RFFs | Player Rules Handbook §2.9 |

{% endif %}
