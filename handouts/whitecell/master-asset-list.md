---
title: "Operation Example — Master Asset List"
subtitle: "Every team's assets, hidden ones included"
short: "Master Asset List"
---

**WHITE CELL ONLY.** *Fictional training scenario. All military systems are real U.S. systems, described with unclassified, approximate capabilities.*

**Hidden** assets (off the map until found, used, or disclosed by an inject) are the **bold** rows. All others are visible on the central map from the start.\
**Core function** (AFDP 3-0, REDFOR Air Force assets): AS, GPA, RGM, GISR, C2. **Joint** = Army, Navy, or Marine Corps.\
**Totals:** REDFOR [n] counters ([n] in theater, [n] at home, [n] hidden) · BLUEFOR [n] assets ([n] hidden) on [n] counters, counting each part of a split counter (Rules §4.5).

> **FORMAT NOTE (delete before printing):** TEMPLATE. Every row of every team packet's force table (`scenario/<team id>-packet.md` §1), in one place, one section per team in the order of `game.toml` `[[side]]`. When the Master Asset List and another white cell document disagree, this one wins, so update it whenever a packet changes. The rows below are the example assets.

## 1. REDFOR: [Red armed forces]

### 1.1 In theater

| ID | Asset · core function · zone | What it does | Limitation (BLUEFOR's Con) |
| --- | --- | --- | --- |
| R-01 | F-35A Lightning II squadron (~12) · AS, GPA · Z6 | Stealth multirole. Penetrates air defenses, precision strike, sensor fusion. | Limited internal load. Needs tankers far from base. High maintenance. |
| R-05 | KC-46A Pegasus tankers · RGM · Z6 | Air refueling for every other aircraft | Unarmed, high-value. Losing it grounds the strike plan. |

### 1.2 At home (Z1)

| ID | Asset · core function · zone | What it does | Limitation (BLUEFOR's Con) |
| --- | --- | --- | --- |
| R-16 | B-52H Stratofortress (JASSM-ER/LRASM) · GPA · Z1 | Standoff strike from home | A strike from home uses it for the whole turn. Not stealthy. |
| **R-18** | **B-2A Spirit · GPA · Z1 (hidden)** | **Stealth penetrating bomber** | **Very few airframes. A loss is a national shock.** |

### 1.3 RFF pool

| ID | Asset | Arrives | Approve when |
| --- | --- | --- | --- |
| R-30 | Additional F-35A squadron | N+1 | There is basing room at the forward base |

## 2. BLUEFOR: [Blue armed forces]

### 2.1 In place at start

| ID | Asset · owner · zone | What it does | Limitation (REDFOR's Con) |
| --- | --- | --- | --- |
| B-01 | F-16C/D Fighting Falcon squadron (~12) · [Air force] · Z11 | Multirole air defense and strike | Outclassed by fifth-generation fighters. One main base. |
| B-04 | Patriot battalion (PAC-2) · [Army] · Z10 | Denies the air over the coast to non-stealthy aircraft | Slow to relocate. Its radar emits. |
| B-07a, b, c | Early-warning radar network · [Air force] · Z10, Z11, Z12 | Cues fighters and Patriot | Fixed emitting sites, easy to find and jam |
| **B-09** | **Harpoon coastal-defense battery · [Navy] · Z10 (hidden)** | **Mobile anti-ship missiles** | **Needs targeting data. Exposed once it fires.** |

### 2.2 RFF pools

| ID | Asset | Arrives | Approve when |
| --- | --- | --- | --- |
| B-30 | Reserve mobilization: 2 infantry brigades | N+1 | Routine |
| B-40 | Arms shipment from [Backer] | N+2 | Routine. REDFOR may try to interdict it. |
