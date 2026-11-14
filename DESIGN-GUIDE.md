# Design Guide — Building a Scenario from the Base

**Audience:** designer. Mentions where secrets go, but holds none.

This guide takes you from an empty copy of the base to a game you can print. It follows the order that worked for the first game built this way: build the public world first, then each side's secrets, then the white cell's material, and the handouts last. Each step names the files it touches. `AGENTS.md` has the file map and the editing rules, and `RULES.md` has the mechanics, which a new scenario normally keeps as they are.

## 1. Plan backward from the releases

Players get material in three releases, and each one fixes how late you can still change things. `tools/build_handouts.py` `RELEASES` lists which file goes in which.

| Release | When it goes out | What's in it | Last chance to change |
| --- | --- | --- | --- |
| Common Matrix | As soon as possible | Rules handbook, player forms | The rules and forms |
| Common Scenario | 1 week before | Scenario brief, schedule, starting conditions, map | The public world, map, tracks, starting conditions |
| REDFOR and BLUEFOR | 24 hours before | Commander's letter, team packet, order of battle, intelligence products, counters | Forces, objectives, intelligence |
| White cell | Before the POC run-through | Everything else | Injects, ground truth, likely plans |

The rules handbook goes out before the scenario is announced, so it must not name anything in the scenario. Its examples use descriptive placeholders.

## 2. Steps

### 2.1 Set up the game

Edit `game.toml`: name, designer, event, date, tables, requests, and the run of show. The run of show (`[schedule]`, `[[block]]`, `[[turn_step]]`) is the game's phase structure and timing: which planning and turn blocks come in what order, how long each step is, and how many turns each phase has (`RULES.md` §2.1). The default is the first game's four phases in a 3-hour block. If the event is shorter or longer, or wants a different shape, set the run of show before anything else, because the turn count drives how many objectives can be reached and how many forms to print. `python3 tools/schedule.py` prints the result with clock times; copy it into `EVENT-SETUP.md` §3. The timer program, the schedule tables in the handouts, and the form counts follow on the next build.

To try timings out, open the timer program (`tools/whitecell-clock.html`), choose **Setup**, change the blocks and minutes, and watch the totals. **Copy as game.toml** gives the text to paste back into `game.toml`.

Then confirm or change each tag in `RULES.md` and record what you changed in `RULES.md` §11. If you rename or reshape the phases, update the handouts that name them (the Scenario Schedule's §1.2–1.4, the White Cell Checklist, the forms' planned-COA rows, and the Rules Handbook) by hand.

### 2.2 Write the premise

One paragraph: who is fighting over what, why now, and why neither side can simply win. A good premise:

- gives both sides something to **lose** as well as gain, so restraint is a real choice;
- has a **neutral or contested third party** (a host nation, a population, a shipping lane) that both sides can court, so non-kinetic COAs matter;
- puts one side **far from home** and the other on home ground, which gives you natural asymmetries (logistics against numbers, outside backers against local support);
- keeps the stakes **below total war**, with limits each government imposes on its own commander.

Write it as the BLUF in `scenario/00-overview.md` §1.

### 2.3 Build the public world

Fill in `scenario/00-overview.md`: background and a short timeline (`00-overview.md` §2), the actors and what everyone knows about them (`00-overview.md` §4), and the rules of engagement and national directives (`00-overview.md` §7). Everything here goes to both teams, so a fact belongs here only if both sides would really know it. Assume both sides read it closely.

### 2.4 Draw the map

See `map/README.md`. Aim for 10–15 zones, including an off-map home box for each side and one for each distant backer. Record the zones in `00-overview.md` §3.2 and the distances that matter in `00-overview.md` §3.3. Settle the zone IDs before you place forces, because the CSV, the packets, and the counters all use them.

### 2.5 Set the tracks and starting conditions

Tracks (`00-overview.md` §5.1) record what the map can't: opinion, will, stability, access. Use three to five, each with a short scale (−3 to +3, or 0 to 5) and stated triggers at the ends. Every track should be movable by both sides, and at least one should be easier to move with words than with weapons. Put the same tracks in `game.toml` `[[track]]`, which the timer program shows.

Starting conditions (§5.2, and `handouts/common/starting-conditions.md`, which repeats them as cue cards) are standing ±1 modifiers with a stated way to remove them. Two or three for each side is enough. Each one should give the other side an obvious target for a COA.

### 2.6 Build the forces

Fill in each packet's §1 (`scenario/redfor-packet.md`, `scenario/bluefor-packet.md`) and mirror every row in `scenario/data/assets.csv`. Then run:

```bash
python3 tools/check_assets.py && python3 tools/make_counters.py
```

- **Real U.S. systems**, unclassified and approximate, with an Air Force emphasis. Use real names on both sides, so cadets learn the systems whichever side they play.
- **Every asset has a limitation** the other side can use as a Con. If you can't think of one, the asset is too strong or too vague.
- Tag REDFOR Air Force assets with their **AFDP 3-0 core function**.
- **One or two hidden assets a side** (`visibility` = hidden). Each needs a hint in the other side's intelligence that a careful team could catch, and a row in the ground truth.
- **RFF pools** let a side ask for more as the game goes on. Give each RFF an arrival turn and a cost: approval, basing room, a track, or giving the other side warning.
- Put an asset spread over several zones on **one row with `parts`**, so it prints one counter for each zone.
- The side with fewer assets needs advantages that **don't fit on a counter**: home ground, population, a backer, starting conditions in its favour.

Asset counts that worked for four tables of 9–10 cadets were about 30 for the larger side and 20–25 for the smaller, plus their RFF pools. More than that slows the white cell.

### 2.7 Write the objectives

Each side gets **three secret objectives** (packet §3), each with criteria the white cell can score at the end: achieved, partly achieved, or not achieved. Good objectives:

- can't be settled by a single COA;
- include at least one that a negotiated outcome can satisfy for **both** sides, which gives the teams a reason to talk;
- include one that is directly opposed to the other side's, through a track or a zone;
- leave a trace the white cell can see. If the map and tracks don't record it, add a line to the objective status card (`scenario/whitecell-ground-truth.md` §3).

Make the larger side's objectives aggressive and the other side's defensive, so a win by the larger side is possible but costly.

### 2.8 Write the intelligence estimates and the ground truth

Each packet's §2 says what that side believes about the other. Make each estimate **partly wrong**: miss a hidden asset, overrate one capability, misread an intention. Then record the truth, row by row, in `scenario/whitecell-ground-truth.md` §1, so every table's white cell answers RFIs the same way.

### 2.9 Write the intelligence products and commander's letters

The products (RI-xx and BI-xx in `handouts/<side>/intel/`) are the in-world documents behind each estimate: imagery reports, source reports, intercepts, embassy cables, press clippings. Each is about a page, in the voice of whoever wrote it (`references/tongue-and-quill-summary.md` §6). List them in each side's `00-read-me-first.md` and explain them in the product key (`handouts/whitecell/intel-and-injects.md` §3). Ten to fifteen a side worked well. Fewer than that, and a hidden asset is either obvious or impossible to find.

The commander's letter (`handouts/<side>/commanders-letter.md`) is the government's guidance in official format: the situation, the authorities and limits, the intent, and the objectives as an attachment. Set its letterhead in `game.toml` `[[tq]]`. If an intelligence product should be in Tongue and Quill format too, add a `[[tq]]` entry whose key starts with its ID.

### 2.10 Write the injects

`scenario/whitecell-injects.md`: one kickoff inject that starts the crisis at the end of Phase I, and a pool of 10–15 to choose from, at most one per turn. Write each one so it can be read aloud in 30 seconds. Give each a purpose (punish stalling, reward a good argument, bring in a third party, test a weak spot) and the turns where it fits. Include a few that help each side, and one that offers a way out (a mediation offer, a ceasefire proposal). Copy the pool into `handouts/whitecell/intel-and-injects.md`.

### 2.11 Fill in the handouts

Most handouts repeat the scenario files in the form each audience uses. Work through them in release order:

1. `handouts/common/scenario-brief.md` and `starting-conditions.md` (from `00-overview.md`).
2. `handouts/<side>/team-packet.md` and `order-of-battle.md` (from the packets and the CSV).
3. `handouts/whitecell/master-asset-list.md`, `intel-and-injects.md`, and `likely-plans.md`.

`likely-plans.md` describes the two or three plans each side is most likely to try, with how the white cell should rule on each. Write it after the playtest (§3), from what the playtesters did.

Then build, read every PDF once on paper, and fix the markdown, never the PDF.

## 3. Playtest

Play the game at least once, all the way through, before the POC run-through. Two people a side and one adjudicator is enough. Watch for:

- **Balance.** Does each side have at least three strong non-kinetic COAs? Can any one COA settle an objective? Is a win by the larger side costly?
- **Dead turns.** If a side has nothing useful to do for two turns, give it a lever: an RFF, an inject, or a track it can move.
- **Leaks.** Can a team learn the other side's hidden assets or objectives from a public file? Check the scenario brief, the map, the starting conditions, and the rules handbook's examples.
- **Time.** The white cell has 2 minutes to resolve both COAs. If rulings keep needing the ground truth, add a line to the likely plans.

Record what changed, and update the open decisions in `scenario/README.md`.

## 4. Lessons learned

- **Keep it simple.** The designer turned down turn-order switching, event cards, and recalculating late objections. Every rule you add has to be taught to new cadets in a few minutes and run by a white cell with 2 minutes a turn. State the time cost of each new rule.
- **Secrecy follows files.** A team packet is a set of files, not a file with parts cut out. Indirect leaks are the common ones: a public file that names a capability only the hidden asset list has, or a rules example that uses a real asset name.
- **Stable IDs.** Assets, zones, objectives, injects, and intelligence products are referenced on forms, counters, and the site. Add new IDs, and never renumber.
- **Relative in-game dates.** Date intelligence products and letters D−x, not with the real event date, so the game world doesn't depend on when it runs.
- **Be consistent across products.** Either every official product carries an in-world classification line or none does. Players read an uneven pattern as a clue.
- **The objective status card is white cell only.** It lists what the hidden objectives care about, so it stays face down with the logger.
- **Assets in several zones** get one counter for each part (B-07a, b, c), so the map shows where each part is and each part can be hit on its own.
- **RFF arrivals** go to each side's main base zone unless the RFF names another destination. Say which zone that is in `00-overview.md` §6.
- **Tracks belong on the screen.** A paper track board and its markers were dropped. The clock shows the tracks on the room's TV, and the white cell moves them there.
- **Use less ink on paperwork.** Forms and slips print without shaded bars. Colour stays on the game pieces: counters, map, and cue cards.
- **Print one packet per table.** The Print Packet puts everything a table needs in order, with the right number of copies, and pads every document to an even page count for double-sided printing.
- **Build, don't hand-edit.** Every PDF comes from markdown. If something must be finished by hand, write down what changed, or the next build undoes it.

## 5. Before each release

- [ ] `python3 tools/check_assets.py` passes.
- [ ] `npx markdownlint-cli2` reports 0 issues.
- [ ] `tools/build_all.sh` runs clean, and you have read the release's PDFs on paper.
- [ ] No `[placeholder]` text is left in the release's files: `grep -rn "\[[A-Z][a-z]" handouts/common` (and the side folders for the 24-hour release).
- [ ] Nothing in a public file names a hidden asset, objective, or inject.
- [ ] Each side's files hold nothing of the other side's.
- [ ] `game.toml` matches the scenario: name, run of show, and tracks. `python3 tools/schedule.py --check` passes, and the timer program in `build/White Cell/` shows the right blocks and tracks.
