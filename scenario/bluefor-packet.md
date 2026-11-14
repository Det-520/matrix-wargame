# [Scenario name] — BLUEFOR Packet ([Blue nation])

**Audience:** the BLUEFOR team and the white cell. **Never give this file to REDFOR.**
**Owner:** [designer] · **Version:** 0.1 ([date]) · Read `scenario/00-overview.md` first.

This packet holds your forces (including hidden ones the enemy doesn't know about), your outside-support options, your intelligence estimate, and your three secret objectives. Status tags work as defined in `RULES.md` §0. All numbers are **[PROPOSED]** unless tagged.

> **TEMPLATE.** The force rows below are examples so the tools run. Replace them with the scenario's forces, keep the IDs stable once anything references them, and mirror every row in `scenario/data/assets.csv`. BLUEFOR should have **fewer** counters than REDFOR and make up for it with starting conditions and outside support. Each asset needs a stated limitation REDFOR can use as a Con.

---

## 1. Forces — [Blue armed forces]

### 1.1 Conventions

- **Counter states:** Ready · Degraded (−1 when used) · Destroyed (removed).
- **Visibility:** *Visible* counters start on the central map. *Hidden* counters stay on your sheet until you use them or the enemy finds them (`RULES.md` §4.4).
- **Split counters:** B-07 has one counter per part (a, b, c), and each part acts and takes damage on its own (`RULES.md` §4.5). The zone column gives each part's starting zone in letter order.
- Capability notes are unclassified, approximate, and simplified for play.
- Your force is smaller than REDFOR's. Your strength comes from your starting conditions (`scenario/00-overview.md` §5.2).

### 1.2 In place at start

| ID | Asset | Owner | Zone | Vis. | What it does | Key limitations (Con fodder) |
| --- | --- | --- | --- | --- | --- | --- |
| B-01 | **F-16C/D Fighting Falcon** squadron (~12) | [Air force] | Z11 [Blue capital] | Visible | Multirole air defense and strike | Outclassed by fifth-generation fighters and AWACS-supported forces. One main base makes it vulnerable. |
| B-04 | **Patriot battalion** (PAC-2) | [Army] | Z10 [Blue coast] | Visible | Denies the air over the coast to non-stealthy aircraft. Can engage missiles. | Mobile but slow to relocate. Its radar emits when active, which signals intelligence can find. |
| B-07 | **Early-warning radar network** (3 sites) | [Air force] | Z10, Z11, Z12 | Visible | Cues fighters and Patriot. Each site watches its own zone. | Fixed sites that emit, so they are easy to find and jam |
| B-09 | **Harpoon coastal-defense battery** | [Navy] | Z10 [Blue coast] | **Hidden** | Mobile anti-ship missiles that threaten any ship near the coast | Needs targeting data from radar or patrol craft. Exposed once it fires. |

### 1.3 RFF pool: national mobilization

Arriving forces, including outside support (§1.4), are placed on **Z11** unless the RFF names another destination (`RULES.md` §5).

| ID | Asset | Arrives | Approval notes |
| --- | --- | --- | --- |
| B-30 | Reserve mobilization: 2 infantry brigades | N+1 | Routine. Costs BLUEFOR economically if repeated. |

### 1.4 RFF pool: outside support ([Backer])

| ID | Asset | Arrives | Approval notes |
| --- | --- | --- | --- |
| B-40 | **Arms shipment**: Stinger, Javelin, Harpoon reloads, PAC-2 interceptors | N+2 | **Routine.** REDFOR can try to interdict it with a COA. |

---

## 2. Intelligence estimate (what [Blue nation] believes)

*The estimate may be incomplete or wrong. Use RFIs and ISR COAs to confirm. All visible REDFOR counters are on the central map.*

> **TEMPLATE.** Five to ten bullets of what BLUEFOR believes about REDFOR's hidden forces, intentions, and allies. Make some right, some exaggerated, and some wrong, and record the truth in `scenario/whitecell-ground-truth.md` §1.

- **[Topic]:** [what BLUEFOR believes]

---

## 3. Secret objectives

*Three objectives, scored at game end (`RULES.md` §9.3). BLUEFOR's are defensive. At least one REDFOR and one BLUEFOR objective should be achievable together, so a negotiated outcome is possible.*

| # | Objective | Achieved | Partial | Not achieved |
| --- | --- | --- | --- | --- |
| B1 | **"[Objective]"** | [measurable end state] | | |
| B2 | **"[Objective]"** | | | |
| B3 | **"[Objective]"** | | | |
