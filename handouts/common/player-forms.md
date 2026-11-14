---
title: "Matrix Wargame — Player Forms and Templates"
subtitle: "OPORD/FRAGO format, COA and Cons worksheets, request slips, Slack templates · [Month Year]"
short: "Player Forms"
---

**Audience:** every player. **Printing:** each team needs 1 OPORD/FRAGO format page, {{ turns }} COA worksheets, {{ turns }} Cons worksheets, {{ slip_pages }} pages of request slips (3 to a page, {{ slips }} slips){% if rules == "full" %}, and {{ secret_coas }} secret COA slips{% endif %}. The white cell's Print Packet already holds this many for each team, plus spares; its Reference Forms version holds one of each per team, to copy from. The forms are black and white, so print them in greyscale. Requests, COAs, Cons{% if rules == "full" %}, and secret COAs{% endif %} are **posted in Slack** ({% if rules == "full" %}Rules Handbook §2.11{% else %}Basic Rules §5.4{% endif %}): use the worksheets to draft, the copy-and-paste templates in §5 to post, and the paper slips only if Slack goes down.

## 1. Five-Paragraph OPORD and FRAGO Format

For reference. Your Phase I brief and Phase III FRAGO don't have to follow this format, but it is a good structure if you want one.

<!-- mw:form med -->

| Five-Paragraph OPORD/FRAGO Format | |
| --- | --- |
| **1. SITUATION** | |
| **2. MISSION** | |
| **3. EXECUTION** | |
| &emsp;a. Concept of operations | |
| &emsp;b. Tasks to subordinate units | |
| &emsp;c. Coordinating instructions | |
| **4. SUSTAINMENT** | |
| **5. COMMAND AND SIGNAL** | |

<!-- pagebreak -->

## 2. COA Worksheet

<!-- mw:form -->

| COA WORKSHEET | |
| --- | --- |
| **Turn / Team** | Turn ___ / {{ team_boxes }} |
| **Planned COA?** | ☐ Yes ☐ No |

<!-- mw:form tall -->

| WHAT YOU WILL DO | |
| --- | --- |
| **Action** (who, what, where, which assets) | |
| **In order to** (measurable effect) | |
| **Pro 1** | |
| **Pro 2** | |
| **Pro 3** | |
| **Public statement** (optional) | |

<!-- pagebreak -->

## 3. Cons Worksheet

<!-- mw:form -->

| CONS WORKSHEET | |
| --- | --- |
| **Turn / Team** | Turn ___ / {{ team_boxes }} |
| **Their COA** (in a few words) | |

<!-- mw:form tall -->

| WHY IT WON'T WORK | |
| --- | --- |
| **Con 1** | |
| **Con 2** | |
| **Con 3** | |

<!-- pagebreak -->

## 4. Request Slips

<!-- mw:begin slips -->

<!-- mw:form -->

| REQUEST SLIP | |
| --- | --- |
| **Turn / Team / Type** | Turn ___ / {{ team_boxes }} / ☐ RFI ☐ RFF |
| **Details** | |
| | |
| | |
| *White cell answer* | |

---

<!-- mw:form -->

| REQUEST SLIP | |
| --- | --- |
| **Turn / Team / Type** | Turn ___ / {{ team_boxes }} / ☐ RFI ☐ RFF |
| **Details** | |
| | |
| | |
| *White cell answer* | |

---

<!-- mw:form -->

| REQUEST SLIP | |
| --- | --- |
| **Turn / Team / Type** | Turn ___ / {{ team_boxes }} / ☐ RFI ☐ RFF |
| **Details** | |
| | |
| | |
| *White cell answer* | |

<!-- mw:end -->

<!-- pagebreak -->

## 5. Slack Templates

Copy a template into Slack, fill in the blanks, and post it. COAs and Cons go in your **group channel** (public); requests{% if rules == "full" %} and secret COAs{% endif %} go in your **team channel** (secret). Use asset IDs (R-01, B-07b). Brief the same thing aloud in your slot: only what is said aloud counts.

### 5.1 COA (group channel, by the end of your COA slot)

```text
COA | Turn __ | Team ______ | Planned COA: Y/N
Action (who, what, where, which assets):
In order to (measurable effect):
Pro 1:
Pro 2:
Pro 3:
Public statement (optional):
```

### 5.2 Cons (group channel, by the end of your Cons slot)

```text
CONS | Turn __ | Team ______
Against (team and COA, in a few words):
Con 1:
Con 2:
Con 3:
```

### 5.3 Request (team channel, one message per request, during Prepare)

```text
RFI/RFF | Turn __ | Team ______
RFI: (one question, one sentence)
RFF: Asset (pool ID or free text) | Destination | Purpose
```

{% if rules == "full" %}

### 5.4 Secret COA (team channel, once per phase)

```text
SECRET COA | Turn __ (or Planning) | Team ______ | Phase II/IV
The trap or deception (what, where, which assets):
Precise trigger (If ... then ...):
Intended effect:
```

{% endif %}

{% if rules == "full" %}

<!-- pagebreak -->

## 6. Secret COA Slip

<!-- mw:form -->

| SECRET COA SLIP | |
| --- | --- |
| **Turn / Team / Phase** | Turn ___ (or ☐ posted in planning) / {{ team_boxes }} / ☐ II ☐ IV |

<!-- mw:form tall -->

| THE TRAP | |
| --- | --- |
| **The trap or deception** (what, where, which assets) | |
| **Precise trigger** ("If … then …") | |
| **Intended effect** | |
| *White cell: fired on turn / result* | |

{% endif %}
