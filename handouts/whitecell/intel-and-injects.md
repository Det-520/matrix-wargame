---
title: "Operation Example — White Cell Intelligence and Injects"
subtitle: "Ground truth, answering RFIs, intelligence product key, injects"
short: "White Cell Intelligence and Injects"
---

**WHITE CELL ONLY.** *Fictional training scenario.*

> **FORMAT NOTE (delete before printing):** TEMPLATE. §1 and §4 are copied from `scenario/whitecell-ground-truth.md` and `scenario/whitecell-injects.md`. §3, the product key, exists only here: write it as you write the products. Keep the section headings: the white cell site splits this document into one page per `##` section and links to "Intelligence product key" and "Injects" by name.

## 1. Ground truth

Each team's intelligence estimate is **deliberately partly wrong**, and its intelligence products mix true, misleading, and irrelevant reports. This table is what is actually true.

| Topic | Truth | Where REDFOR's estimate is wrong | Where BLUEFOR's estimate is wrong |
| --- | --- | --- | --- |
| [Topic] | | | |

## 2. Answering RFIs

Answer from what that side would plausibly know: incomplete, uncertain ("unknown"), or wrong if the enemy has succeeded at deception. **Never** reveal secret objectives{% if rules == "full" %} or secret COAs{% endif %}. Write answers in one or two sentences. The logger posts each one in a thread under the team's request in its team channel by the start of the next Prepare.

- **Hidden counters** are revealed by a successful ISR **COA**, not by an RFI. An RFI can give hints ("signals intelligence suggests additional air defense emitters in the interior") but not a location.
- **An RFI that asks to confirm an intelligence product** gets an answer consistent with the key (§3): confirm what is true (without giving locations of hidden counters), cast doubt on what is false, and say "no further information" about noise.
- **RFIs about what a side can't hide** (visible counters, radar emissions, ships in port) get good answers from a side with the ISR to see them.
- **Questions about white-cell actors' intentions** get a hedged answer that matches §1.
- [Any starting condition or RFF that changes how fully a side's RFIs are answered, e.g. local lookouts or shared intelligence.]

### Sample answers

*Write one sample answer for each RFI you expect in Phase I, so every table answers the same way.*

| RFI | Answer |
| --- | --- |
| REDFOR: "[Question]" | "[Answer]" |
| BLUEFOR: "[Question]" | "[Answer]" |

<!-- pagebreak -->

## 3. Intelligence product key

Both sides' products were written so that each team has **true hints** about the enemy's hidden assets and secret objectives, **misleading reports** that reinforce its estimate's errors, and **noise**. Use this key when a team builds a Pro or Con on a product (Handbook §5.2) or files an RFI about one.

**Verdicts:** **True** (accurate) · **Partly true** (accurate facts, wrong conclusion) · **False** (wrong or planted) · **Noise** (true but not decisive).

### 3.1 REDFOR products (RI-xx)

| ID | What it says | Verdict | What it points to |
| --- | --- | --- | --- |
| RI-01 | A ship from [Blue's backer] offloaded ~10 large tarped vehicles at [the port]. They drove inland. | [**True**] | [The hidden asset it hints at, and what that means for REDFOR] |

### 3.2 BLUEFOR products (BI-xx)

| ID | What it says | Verdict | What it points to |
| --- | --- | --- | --- |
| BI-01 | Unmarked four-engine aircraft landed at night at [a remote airfield] and left before dawn. | [**Partly true**] | [What it really was] |

## 4. Injects

### 4.1 Kickoff inject (read aloud at the end of Phase I)

> "[The kickoff inject, word for word, from `scenario/whitecell-injects.md` §1.]"

### 4.2 Inject pool

At most one per turn, the lead adjudicator's choice (Rules §7).

| ID | Inject | Purpose | Suggested timing |
| --- | --- | --- | --- |
| I-01 | [Inject] | | |
| I-13 | **Bounding directive** (use if needed): national command forbids an escalating behavior. | Keeps the game on the rails | As needed |
