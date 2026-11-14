# [Scenario name] — REDFOR Packet ([Red nation])

**Audience:** the REDFOR team and the white cell. **Never give this file to BLUEFOR.**
**Owner:** [designer] · **Version:** 0.1 ([date]) · Read `scenario/00-overview.md` first.

This packet holds your forces (including hidden ones the enemy doesn't know about), your intelligence estimate, and your three secret objectives. Status tags work as defined in `RULES.md` §0. All numbers are **[PROPOSED]** unless tagged.

> **TEMPLATE.** The force rows below are examples so the tools run. Replace them with the scenario's forces, keep the IDs stable once anything references them, and mirror every row in `scenario/data/assets.csv` (`python3 tools/check_assets.py` checks the two match). REDFOR should have **more** counters than BLUEFOR, and each asset needs a stated limitation BLUEFOR can use as a Con.

---

## 1. Forces — [Red armed forces]

### 1.1 Conventions

- **Counter states:** Ready · Degraded (−1 when used) · Destroyed (removed).
- **Visibility:** *Visible* counters start on the central map. *Hidden* counters stay on your sheet until you use them or the enemy finds them (`RULES.md` §4.4).
- Capability notes are unclassified, approximate, and simplified for play.
- **Core function** tags (AFDP 3-0): AS = Air Superiority, GPA = Global Precision Attack, RGM = Rapid Global Mobility, GISR = Global ISR, C2 = Command and Control.
- **Joint** marks non-Air Force systems (Army, Navy, Marine Corps).

### 1.2 In theater at start ([Red forward base], Z6, unless noted)

| ID | Asset | Vis. | Core fn | What it does in the game | Key limitations (Con fodder) |
| --- | --- | --- | --- | --- | --- |
| R-01 | **F-35A Lightning II** squadron (~12) | Visible | AS, GPA | Stealth multirole. Penetrates air defenses, precision strike, sensor fusion (shares its picture with others). | Limited internal weapons load. Needs tankers for persistence far from base. High maintenance demand. |
| R-05 | **KC-46A Pegasus** tanker detachment | Visible | RGM | Air refueling: extends range and persistence of every other aircraft | Unarmed, a high-value target. Losing it grounds the strike plan. |

### 1.3 Available from home (off-map, Z1)

| ID | Asset | Vis. | Core fn | What it does in the game | Key limitations (Con fodder) |
| --- | --- | --- | --- | --- | --- |
| R-16 | **B-52H Stratofortress** with JASSM-ER and LRASM | Visible | GPA | Standoff strike from home, against land and sea targets | A strike from home uses the counter for the whole turn. Not stealthy, so it stays outside defended airspace. |
| R-18 | **B-2A Spirit** | Hidden | GPA | Stealth penetrating bomber | Very few airframes. Losing one is a national shock. |

### 1.4 RFF pool

Request these with an RFF. Arrival is counted from the turn the request is submitted (`scenario/00-overview.md` §6). Arriving forces are placed on **Z6** unless the RFF names another destination (`RULES.md` §5).

| ID | Asset | Arrives | Approval notes |
| --- | --- | --- | --- |
| R-30 | Additional **F-35A** squadron | N+1 | Needs basing room at the forward base |

---

## 2. Intelligence estimate (what [Red nation] believes)

*The estimate may be incomplete or wrong. Use RFIs and ISR COAs to confirm. All visible BLUEFOR counters are on the central map.*

> **TEMPLATE.** Five to ten bullets of what REDFOR believes about BLUEFOR's hidden forces, intentions, and backers. Make some right, some exaggerated, and some wrong, and record the truth for each in `scenario/whitecell-ground-truth.md` §1.

- **[Topic]:** [what REDFOR believes]

---

## 3. Secret objectives

*Three objectives, scored at game end (`RULES.md` §9.3). REDFOR's are aggressive. Each should be checkable from the map, the tracks, or the objective status card, and no single COA should be able to settle one. At least one should be reachable through talks, so the teams have a reason to negotiate.*

| # | Objective | Achieved | Partial | Not achieved |
| --- | --- | --- | --- | --- |
| R1 | **"[Objective]"** | [measurable end state] | | |
| R2 | **"[Objective]"** | | | |
| R3 | **"[Objective]"** | | | |
