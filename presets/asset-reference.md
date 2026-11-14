# Asset Reference

**Audience:** designer and white cell. Generated from `presets/assets.csv` by `python3 tools/presets.py reference --write`: edit the CSV, not this page.

A catalog of 86 real U.S. systems, forces, and authorities to build a scenario's forces from (`DESIGN-GUIDE.md` §2.6, `presets/README.md` §3). Capabilities are unclassified, approximate, and simplified for play, and every entry has a limitation another team can use as a Con. Copy one into a team with `python3 tools/presets.py add-asset SIDE KEY`.

**Columns.** *Core fn* is the AFDP 3-0 core function, given for Air Force assets: AS = Air Superiority, GPA = Global Precision Attack, RGM = Rapid Global Mobility, GISR = Global ISR, C2 = Command and Control. *Cell* is the cell preset that usually owns it (`presets/cells.toml`). *RFF* is a typical arrival and approval when the asset is in an RFF pool. *Hidden* marks an asset that makes a good hidden counter.

## Fighters and attack aircraft

| Key | Asset | Service | Core fn | What it does | Key limitation | Cell | RFF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `f22` | F-22A Raptor squadron (~12) | USAF | AS | Stealth air superiority: sweeps and escorts | Small fleet; little air-to-ground load; needs tankers far from base | AIR | N+1, needs basing room |
| `f35a` | F-35A Lightning II squadron (~12) | USAF | AS, GPA | Stealth multirole strike, sensor fusion | Limited internal load; needs tankers; high maintenance | AIR | N+1, needs basing room |
| `f15e` | F-15E Strike Eagle squadron (~12) | USAF | GPA, AS | Long-range strike with a heavy payload | Not stealthy; needs suppression of air defenses in defended airspace | AIR | N+1, needs basing room |
| `f15ex` | F-15EX Eagle II squadron (~12) | USAF | AS | Long-range air-to-air missile carrier; homeland and base defense | Not stealthy; few fielded | AIR | N+2, needs basing room |
| `f16` | F-16C/D Fighting Falcon squadron (~12) | USAF | AS, GPA | Multirole air defense and strike | Outclassed by fifth-generation fighters; short range | AIR | N+1, routine |
| `f16cm` | F-16CM Wild Weasel squadron (~12) | USAF | GPA | Suppression of enemy air defenses (HARM) | Must close with the threat; losses likely against modern surface-to-air missiles | AIR | N+1, routine |
| `a10` | A-10C Thunderbolt II squadron (~12) | USAF | GPA | Close air support; attack on vehicles and small boats | Slow; very vulnerable to modern air defenses | AIR | N+1, routine |
| `f35b` | F-35B Lightning II detachment (~6, USMC) | USMC | — | Short-takeoff stealth fighters from small airfields or amphibious ships | Few aircraft; limited fuel and weapons | AIR | N+1, needs an amphibious ship or short strip |
| `fa18` | F/A-18E/F Super Hornet squadron (~12) | Navy | — | Carrier-based multirole fighter | Tied to its carrier; shorter range than land-based fighters | AIR | N+2, comes with a carrier |

**Notes.**

- `f22`: The best air-to-air fighter; few exist
- `f16`: Flown by many partner nations: a natural host-nation or coalition fighter
- `fa18`: Usually part of the carrier strike group counter

## Bombers and air-delivered mines

| Key | Asset | Service | Core fn | What it does | Key limitation | Cell | RFF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `b52` | B-52H Stratofortress (JASSM-ER/LRASM) | USAF | GPA | Standoff strike from home against land and sea targets | Whole-turn sortie; not stealthy | AIR | N+1, political: a strategic signal |
| `b1` | B-1B Lancer (LRASM) | USAF | GPA | Large payload; long-range anti-ship strike | Not stealthy; old fleet with low readiness | AIR | N+1, political: a strategic signal |
| `b2` | B-2A Spirit *(hidden)* | USAF | GPA | Stealth penetrating bomber | Very few airframes; a loss is a national shock | AIR | N+1, political: national approval |
| `quickstrike` | Quickstrike air-laid sea mines *(hidden)* | USAF | GPA | Bombers lay mines that close a channel or port | Indiscriminate: hurts neutral shipping; slow to clear afterward | AIR | N+1, political: affects neutral shipping |

**Notes.**

- `b52`: A bomber task force deployment is also a show of force

## Electronic warfare

| Key | Asset | Service | Core fn | What it does | Key limitation | Cell | RFF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ea18g` | EA-18G Growler squadron (~5) | Navy | — | Airborne electronic attack: jams radars and communications | Emits, so it is found; needs escort | AIR | N+1, routine |
| `ec37b` | EC-37B Compass Call | USAF | AS | Jams enemy command-and-control and radar from standoff | Unarmed high-value aircraft; few airframes | AIR | N+1, routine |
| `mald` | ADM-160 MALD decoy stock *(hidden)* | USAF | GPA | Air-launched decoys and jammers that saturate air defenses | Used up when launched; buys time, destroys nothing | AIR | N+1, routine |

**Notes.**

- `mald`: Good hidden asset: the enemy sees a bigger raid than it is

## Tankers

| Key | Asset | Service | Core fn | What it does | Key limitation | Cell | RFF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `kc46` | KC-46A Pegasus tanker detachment | USAF | RGM | Air refueling: extends every aircraft's range and time on station | Unarmed high-value target; losing it grounds the strike plan | LOG | N+1, routine |
| `kc135` | KC-135R Stratotanker squadron | USAF | RGM | Air refueling | Old airframes; unarmed; needs a long runway | LOG | N+1, routine |

## Airlift

| Key | Asset | Service | Core fn | What it does | Key limitation | Cell | RFF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `c17` | C-17A Globemaster III squadron | USAF | RGM | Strategic and tactical airlift; outsize cargo to short fields | Each lift is a target; every team wants it | LOG | N+1, routine |
| `c130j` | C-130J Super Hercules squadron | USAF | RGM | Tactical airlift and airdrop to austere strips | Slow; vulnerable to shoulder-fired missiles | LOG | N+1, routine |
| `c5m` | C-5M Super Galaxy | USAF | RGM | Heaviest strategic airlift | Needs large airfields; low readiness | LOG | N+1, routine |
| `mv22` | MV-22B Osprey squadron (USMC) | USMC | — | Tiltrotor assault transport | Limited payload; vulnerable at landing zones | LOG | N+1, routine |
| `ch47` | CH-47F Chinook company | Army | — | Heavy-lift helicopters | Short range; vulnerable to shoulder-fired missiles | LOG | N+1, routine |

## Logistics and sealift

| Key | Asset | Service | Core fn | What it does | Key limitation | Cell | RFF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `sealift` | Military Sealift Command roll-on/roll-off ships | Navy | — | Moves heavy equipment and supplies by sea | Slow; needs a port and an escort | LOG | N+3, routine |
| `aps` | Army prepositioned stocks (APS) afloat | Army | — | Equipment for a brigade, already afloat in the region | Needs a port and troops flown in to use it | LOG | N+2, routine |
| `fuel` | Expeditionary fuel and munitions resupply | USAF | RGM | Restores sortie rates after shortages | Takes a turn; convoys and airlift can be hit | LOG | N+1, routine |

**Notes.**

- `fuel`: An RFF that answers a logistics Con

## Command and control

| Key | Asset | Service | Core fn | What it does | Key limitation | Cell | RFF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `e3` | E-3G Sentry (AWACS) | USAF | C2 | Airborne early warning and control of the air battle | High-value target; must stay back from enemy fighters | AIR | N+1, routine |
| `e2d` | E-2D Advanced Hawkeye | Navy | — | Carrier-based early warning and control | Tied to its carrier | SEA | N+2, comes with a carrier |
| `e11` | E-11A BACN | USAF | C2 | Airborne communications relay that links forces that can't talk directly | Single point of failure; unarmed | AIR | N+1, routine |
| `aoc` | Air Operations Center | USAF | C2 | Plans and directs the air campaign (the air tasking order cycle) | Large and fixed: a priority target; the order cycle runs about 72 hours | AIR | — |
| `crc` | Control and Reporting Center | USAF | C2 | Ground radar and battle management of the air picture | Emits; must relocate to survive | AMD | N+1, routine |

**Notes.**

- `aoc`: Usually off-map at a main base

## Intelligence, surveillance, and reconnaissance

| Key | Asset | Service | Core fn | What it does | Key limitation | Cell | RFF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `rc135` | RC-135V/W Rivet Joint | USAF | GISR | Signals intelligence: finds and identifies emitters | Unarmed; must fly close to the border; needs escort | INT | N+1, routine |
| `rq4` | RQ-4B Global Hawk | USAF | GISR | High-altitude, long-endurance wide-area imagery | Unarmed; easy prey for fighters and surface-to-air missiles | INT | N+1, routine |
| `mq9` | MQ-9A Reaper squadron | USAF | GISR, GPA | Persistent armed overwatch; small precision strikes | Slow; easily shot down in defended airspace | INT | N+1, routine |
| `u2` | U-2S Dragon Lady | USAF | GISR | High-altitude imagery and signals collection | One aircraft per area; predictable tracks | INT | N+1, routine |
| `p8` | P-8A Poseidon squadron | Navy | — | Maritime patrol, anti-submarine and anti-ship warfare | Vulnerable to fighters; slow to the area | SEA | N+1, routine |
| `mq4c` | MQ-4C Triton | Navy | — | Persistent maritime surveillance | Unarmed; vulnerable | SEA | N+1, routine |
| `humint` | Human intelligence source network *(hidden)* | Joint | — | Reports on intentions and leadership decisions | Slow and uncertain; can be fed false information | INT | — |
| `comm-imagery` | Commercial satellite imagery contract | Joint | — | Daily unclassified imagery that can be shared with partners and the press | Weather-limited; the other side can buy it too | SPC | N+0, routine |

**Notes.**

- `humint`: Hidden: the enemy doesn't know who talks
- `comm-imagery`: A non-kinetic lever: evidence for the information cell

## Space

| Key | Asset | Service | Core fn | What it does | Key limitation | Cell | RFF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `opir` | SBIRS / Next-Gen OPIR missile warning | USSF | — | Detects missile launches worldwide | Warns only; stops nothing | SPC | — |
| `wgs` | WGS satellite communications | USSF | — | Wideband satellite communications for deployed forces | Can be jammed; limited bandwidth | SPC | — |
| `gps` | GPS constellation | USSF | — | Precision navigation and timing for weapons and forces | Can be jammed locally; the enemy uses it too | SPC | — |
| `ccs` | Counter Communications System *(hidden)* | USSF | — | Ground-based jamming of enemy satellite communications | Temporary, local effect; reveals intent | SPC | N+1, political: counterspace needs national approval |

## Cyber

| Key | Asset | Service | Core fn | What it does | Key limitation | Cell | RFF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `cyber-cmf` | Cyber Mission Force team (USCYBERCOM) *(hidden)* | Joint | — | Offensive cyber operations against networks and infrastructure | Takes turns to prepare; effects are uncertain, temporary, and lost once used | CYB | N+2, political: offensive cyber needs national approval |
| `cpt` | Cyber Protection Team | Joint | — | Defends networks and critical infrastructure | Defense only; can't be everywhere | CYB | N+1, routine |

## Air and missile defense

| Key | Asset | Service | Core fn | What it does | Key limitation | Cell | RFF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `patriot` | Patriot battalion (PAC-3 MSE) | Army | — | Air and missile defense of a key area | Slow to relocate; radar emits; interceptors limited | AMD | N+2, routine |
| `thaad` | THAAD battery | Army | — | Upper-tier ballistic missile defense | Very few batteries; does one job; its radar is a target | AMD | N+2, political: strategic signal |
| `mshorad` | M-SHORAD platoon (Stryker) | Army | — | Short-range air defense against drones and helicopters | Short range; few vehicles | AMD | N+1, routine |
| `stinger` | Stinger air defense teams *(hidden)* | Army | — | Shoulder-fired low-altitude air defense | Very short range; no use against high-flying aircraft | AMD | N+1, routine |
| `c-uas` | Counter-drone system (Coyote interceptors, LIDS) | Army | — | Defends a base against drones | Short range; easily saturated | AMD | N+1, routine |

**Notes.**

- `stinger`: Easy to hide, so a good hidden asset

## Long-range fires and coastal defense

| Key | Asset | Service | Core fn | What it does | Key limitation | Cell | RFF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `himars` | M142 HIMARS battery (GMLRS, ATACMS) | Army | — | Precision rockets and missiles, about 300 km with ATACMS | Must be in range; few reloads; shoot and move | LAND | N+1, routine |
| `typhon` | Typhon Mid-Range Capability battery (SM-6, Tomahawk) | Army | — | Long-range land attack and anti-ship strike from land | Large and hard to hide; a political flashpoint for the host | LAND | N+2, political: host-nation consent |
| `nmesis` | NMESIS anti-ship missile battery (USMC) *(hidden)* | USMC | — | Ground-based anti-ship missiles hidden on islands and coasts | Needs targeting data from others; few launchers | LAND | N+1, routine |
| `harpoon-cd` | Harpoon coastal defense battery *(hidden)* | Navy | — | Mobile anti-ship missiles | Needs targeting data; exposed once it fires | LAND | N+2, routine |

## Naval forces

| Key | Asset | Service | Core fn | What it does | Key limitation | Cell | RFF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `csg` | Carrier strike group (Nimitz class) | Navy | — | An air wing at sea: sustained strike and fleet air defense | A huge political signal and a prime target; slow to arrive | SEA | N+3, political: a major national decision |
| `ddg` | Arleigh Burke-class destroyer (Aegis) | Navy | — | Fleet air and missile defense; Tomahawk land attack | About 96 missile cells, which can't be reloaded at sea | SEA | N+1, routine |
| `ssn` | Virginia-class attack submarine *(hidden)* | Navy | — | Covert anti-ship and anti-submarine warfare, Tomahawk strike, ISR | Hard to communicate with; few weapons; a loss is grave | SEA | N+2, routine |
| `ssgn` | Ohio-class guided-missile submarine (SSGN) *(hidden)* | Navy | — | Up to 154 Tomahawks; carries special operations forces | Only four exist; slow to arrive | SEA | N+3, political: strategic asset |
| `arg` | Amphibious ready group with Marine expeditionary unit | Navy | — | About 2,000 Marines with amphibious lift, helicopters, and F-35B | Slow; vulnerable close to shore; a visible escalation | SEA | N+3, political: escalation |
| `lcs-mcm` | Littoral combat ship with mine countermeasures | Navy | — | Clears sea mines from channels and ports | Lightly armed; slow, exposed work | SEA | N+2, routine |
| `cutter` | Coast Guard National Security Cutter | USCG | — | Law enforcement, inspection, and escort below the threshold of war | Lightly armed; a combat role is an escalation | SEA | N+1, routine |

**Notes.**

- `cutter`: A gray-zone tool: enforce without a warship

## Ground forces

| Key | Asset | Service | Core fn | What it does | Key limitation | Cell | RFF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ibct` | Infantry brigade combat team (airborne) | Army | — | Rapid airborne or air-landed infantry | Light: little armor or air defense; needs airlift | LAND | N+1, political: troops on the ground |
| `sbct` | Stryker brigade combat team | Army | — | Medium mechanized force; quick moves by road | Thin armor against tanks; needs a lot of fuel | LAND | N+2, political: troops on the ground |
| `abct` | Armored brigade combat team (Abrams, Bradley) | Army | — | Heavy armor | Weeks to arrive by sea; a large supply tail | LAND | N+3, political: troops on the ground |
| `mlr` | Marine littoral regiment | USMC | — | Small units spread across islands: anti-ship missiles, air defense, sensors | Small units; hard to resupply under fire | LAND | N+2, routine |
| `ah64` | AH-64E Apache battalion | Army | — | Attack helicopters against armor and small boats | Vulnerable to shoulder-fired missiles; short range | LAND | N+1, routine |
| `javelin` | Javelin anti-tank teams *(hidden)* | Army | — | Portable anti-armor missiles | Short range; few missiles per team | LAND | N+1, routine |
| `switchblade` | Switchblade 600 loitering munitions *(hidden)* | Army | — | Small drones that find and strike vehicles and boats | Small warhead; short range; can be jammed | LAND | N+1, routine |
| `small-uas` | Small drone teams (Group 1 UAS) | Army | — | Local reconnaissance and spotting | Short range and endurance; easy to jam | INT | N+0, routine |

## Basing and Agile Combat Employment

| Key | Asset | Service | Core fn | What it does | Key limitation | Cell | RFF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ace` | Agile Combat Employment package (3 dispersal airfields) *(3 counters)* | USAF | RGM | Spreads aircraft across several airfields, so the enemy must find and strike each one | Lower sortie rate; each site needs fuel, munitions, and defense | ACE | N+1, needs host-nation consent |
| `red-horse` | RED HORSE civil engineer squadron | USAF | RGM | Builds and repairs airfields; rapid runway repair | Needs airlift and materials; slow under attack | ACE | N+1, routine |
| `secfor` | Security Forces squadron | USAF | — | Base defense against raids and sabotage | Defends one base; lightly armed | ACE | N+1, routine |
| `emeds` | Expeditionary medical support (field hospital) | USAF | — | Field hospital; treats casualties and civilians | No combat value; must be protected | CA | N+1, routine |

**Notes.**

- `emeds`: A humanitarian lever for the opinion tracks

## Special operations

| Key | Asset | Service | Core fn | What it does | Key limitation | Cell | RFF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `sof-oda` | Special Forces detachment (ODA) *(hidden)* | Army | — | Trains and advises partner forces; special reconnaissance | Small; capture is a political crisis | SOF | N+1, political: troops on the ground |
| `seals` | Navy SEAL platoon *(hidden)* | Navy | — | Maritime raids and reconnaissance | Small and high-risk; needs a way in and out | SOF | N+1, political: troops on the ground |
| `mc130j` | MC-130J Commando II | USAF | RGM | Low-level infiltration and refueling for special operations | Few; vulnerable once detected | SOF | N+1, routine |
| `ac130j` | AC-130J Ghostrider gunship | USAF | GPA | Precise firepower at night | Only at night, and only where air defenses are weak | SOF | N+1, routine |

## Information and civil affairs

| Key | Asset | Service | Core fn | What it does | Key limitation | Cell | RFF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `miso` | Military information support operations team | Army | — | Messaging to populations and forces | Slow effect; backfires if exposed | INFO | N+1, routine |
| `ca-team` | Civil affairs team | Army | — | Works with local authorities and the population | No combat power | CA | N+1, routine |

## Authorities and packages (RFF items, not map counters)

| Key | Asset | Service | Core fn | What it does | Key limitation | Cell | RFF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `auth-strike` | Authority to strike targets in [ENEMY HOMELAND] | Joint | — | Lifts a rule-of-engagement limit | An escalation that costs opinion and may draw in others | JAG | N+0, political: national approval |
| `auth-cyber` | Authority for offensive cyber operations | Joint | — | Allows the cyber cell's offensive operations | Attribution risk; may provoke a response in kind | JAG | N+0, political: national approval |
| `sanctions` | Economic sanctions package | Joint | — | Pressure on the enemy's economy and will | Slow; hurts partners and neutrals too | POL | N+1, political: needs partners |
| `arms-transfer` | Arms transfer package (Stinger, Javelin, Harpoon, PAC-3) | Joint | — | Reloads and new weapons for a partner | Can be intercepted in transit | POL | N+2, routine |
| `humanitarian` | Humanitarian aid airlift | Joint | — | Food and medicine into a crisis zone | Needs safe airspace and a landing site | CA | N+1, routine |
| `intel-share` | Intelligence-sharing agreement with a partner | Joint | — | Shares the picture with a partner, improving its RFIs and COAs | Risk of leaks | INT | N+0, routine |
| `reserves` | Reserve mobilization (2 brigades) | Army | — | More ground forces for home defense | Costly if repeated; untrained at first | LAND | N+1, political: domestic cost |

**Notes.**

- `auth-strike`: Not a counter: record it on the placement form
