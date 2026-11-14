#!/usr/bin/env python3
"""The run of show in game.toml as tables for the documents, and as the timer program's settings.

    python3 tools/schedule.py                    # print the players' schedule table
    python3 tools/schedule.py whitecell          # print the white cell's (turn-clock, turn-clock-whitecell: one turn)
    python3 tools/schedule.py values             # list the names a document template can use
    python3 tools/schedule.py --write            # refresh the timer program's settings
    python3 tools/schedule.py --check            # exit 1 if the timer is stale or any template fails to render;
                                                 # also prints design advice (fewer than 6 turns, an odd team count)
    python3 tools/schedule.py --clock OUT.html   # write a copy of the timer program set up from game.toml

The documents are Jinja2 templates (tools/game.py render()), filled in when the handouts
and the site are built, so nothing in the markdown goes stale. A document places a
generated table with

    {{ schedule_table() }}                 players: what each block asks of them
    {{ schedule_table("whitecell") }}      white cell: what to do and say in each step
    {{ turn_clock_table() }}               players: the steps of one turn ([[turn_step]] brief)
    {{ turn_clock_table("whitecell") }}    white cell: the steps of one turn ([[turn_step]] say)

--write (run by tools/build_handouts.sh and tools/build_site.sh) fills in the settings
block in tools/whitecell-clock.html. --check (run in CI) also renders every markdown
file under both rule sets, so a misspelled name fails the build. Clock times count from
[schedule] start; with no start they are minutes from the start of the game.
"""
import html
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from game import (GAME, ROOT, RULE_SETS, warnings, clock_config, clock_len, clock_time, fill, fmt_num,  # noqa: E402
                  game_texts, render, run_of_show, values, word)

CLOCK_SRC = os.path.join(ROOT, "tools", "whitecell-clock.html")
CONFIG_RE = re.compile(r'(<script type="application/json" id="mw-config">)(.*?)(</script>)', re.S)


def cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def span(a, b):
    return f"{clock_time(a)}–{clock_time(b)}"


def turns_name(b):
    rng = f"Turn {b['first']}" if b["first"] == b["last"] else f"Turns {b['first']}–{b['last']}"
    return f"{b['name']} – {rng}"


def turns_text(b, sep=" · "):
    n, length = len(b["turns"]), fmt_num(b["turn_len"])
    head = f"{word(n).capitalize()} {length}-minute turn{'s' if n != 1 else ''}:"
    return head + " " + sep.join(f"**Turn {t}:** {span(a, z)}" for t, a, z in b["turns"])


def text(b, s, key):
    return fill(s.get(key, ""), first=b.get("first", ""), last=b.get("last", ""), min=s.get("min", ""))


def players_table(g):
    rows = ["| Time | Min | Block | What you do |", "| --- | --- | --- | --- |"]
    for b in run_of_show(g):
        mins = fmt_num(b["end"] - b["start"])
        if b.get("turns"):
            what = turns_text(b) + (f" · {b['brief']}" if b.get("brief") else "")
            rows.append(f"| {span(b['start'], b['end'])} | {mins} | **{cell(turns_name(b))}** | {cell(what)} |")
            continue
        parts = [b["brief"]] if b.get("brief") else []
        steps = [s for s in b["steps"] if s.get("brief")]
        if len(b["steps"]) == 1 and steps:
            parts.append(text(b, steps[0], "brief"))
        else:
            for s in steps:
                m0, m1 = fmt_num(s["start"] - b["start"]), fmt_num(s["end"] - b["start"])
                parts.append(f"**{span(s['start'], s['end'])} (min {m0}–{m1}):** {text(b, s, 'brief')}")
        rows.append(f"| {span(b['start'], b['end'])} | {mins} | **{cell(b['name'])}** | {cell(' · '.join(parts))} |")
    return "\n".join(rows)


def whitecell_table(g):
    rows = ["| Clock | Min | Block / step | White cell actions |", "| --- | --- | --- | --- |"]
    for b in run_of_show(g):
        mins = fmt_num(b["end"] - b["start"])
        if b.get("turns"):
            rows.append(f"| **{span(b['start'], b['end'])}** | **{mins}** | **{cell(turns_name(b))}** | "
                        f"{cell('Run ' + turns_text(b)[0].lower() + turns_text(b)[1:])} |")
        elif len(b["steps"]) == 1:
            rows.append(f"| **{span(b['start'], b['end'])}** | **{mins}** | **{cell(b['name'])}** | "
                        f"{cell(text(b, b['steps'][0], 'say'))} |")
        else:
            rows.append(f"| **{span(b['start'], b['end'])}** | **{mins}** | **{cell(b['name'])}** | |")
            for s in b["steps"]:
                rows.append(f"| {span(s['start'], s['end'])} | {fmt_num(s['min'])} | • {cell(s['name'])} | "
                            f"{cell(text(b, s, 'say'))} |")
    return "\n".join(rows)


def turn_rows(g):
    at = 0.0
    for s in g["turn_step"]:
        yield s, f"{clock_len(at)}–{clock_len(at + s['min'])}", clock_len(s["min"])
        at += s["min"]


def turn_clock_players(g):
    rows = ["| Step | Clock | Time | Who | What happens |", "| --- | --- | --- | --- | --- |"]
    for s, span_, dur in turn_rows(g):
        rows.append(f"| **{cell(s['name'])}** | {span_} | {dur} | {cell(s.get('who', ''))} | {cell(s.get('brief', ''))} |")
    return "\n".join(rows)


def turn_clock_whitecell(g):
    rows = ["| Step | Turn clock | Duration | Lead adjudicator says or does |", "| --- | --- | --- | --- |"]
    for s, span_, dur in turn_rows(g):
        say = fill(s.get("say", ""), turn="N", min=s["min"])
        rows.append(f"| **{cell(s['name'])}** | {span_} | {dur} | {cell(say)} |")
    return "\n".join(rows)


def tables(rule_set=None):
    """The table functions a template can call, for one rule set (the texts in game.toml may differ by rule set)."""
    g = game_texts(rule_set=rule_set)
    return {
        "schedule_table": lambda who="players": (whitecell_table if who == "whitecell" else players_table)(g),
        "turn_clock_table": lambda who="players": (turn_clock_whitecell if who == "whitecell" else turn_clock_players)(g),
    }


def markdown_files():
    try:
        out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "*.md"],
                             cwd=ROOT, capture_output=True, text=True, check=True).stdout  # new files too
        files = out.split()
    except (OSError, subprocess.CalledProcessError):
        files = [os.path.relpath(os.path.join(d, f), ROOT) for d, _, fs in os.walk(ROOT) for f in fs if f.endswith(".md")]
    return [f for f in files if not f.startswith(("references/", "build/", "site/book/", "site/src/"))]


def check_templates():
    """Render every markdown file under every rule set; render() stops on the first error."""
    for rule_set in RULE_SETS:
        for rel in markdown_files():
            with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
                render(f.read(), where=rel, rule_set=rule_set)


def clock_html():
    """tools/whitecell-clock.html with game.toml's settings in its mw-config block."""
    with open(CLOCK_SRC, encoding="utf-8") as f:
        src = f.read()
    data = json.dumps(clock_config(), ensure_ascii=False, indent=1).replace("</", "<\\/")
    new, n = CONFIG_RE.subn(lambda m: m.group(1) + "\n" + data + "\n" + m.group(3), src)
    if n != 1:
        sys.exit(f"{os.path.relpath(CLOCK_SRC, ROOT)}: no mw-config block to fill in")
    title = html.escape(GAME["game"]["name"]) + " · White Cell Clock"
    return src, re.sub(r"<title>[^<]*</title>", lambda m: f"<title>{title}</title>", new, count=1)


def write_clock(out):
    page = clock_html()[1]  # before opening `out`, which may be the source itself
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)


def show(v, indent=""):
    for k, x in v.items():
        if isinstance(x, dict):
            print(f"{indent}{k}:")
            show(x, indent + "  ")
        else:
            print(f"{indent}{k} = {fmt_num(x) if isinstance(x, (int, float)) else x!r}")


def main(argv):
    if "--clock" in argv:
        write_clock(argv[argv.index("--clock") + 1])
    elif "--write" in argv or "--check" in argv:
        old, new = clock_html()
        if "--check" in argv:
            for w in warnings():
                print("advice:", w)
            check_templates()
            if new != old:
                sys.exit("out of date: tools/whitecell-clock.html. Run python3 tools/schedule.py --write")
        elif new != old:
            write_clock(CLOCK_SRC)
            print("updated tools/whitecell-clock.html")
    elif argv[1:] == ["values"]:
        show(values())
        print("functions: mins(m), clock(m), word(n), Word(n), days(d), days(d, adj=True), ticks(first=1), "
              "turn_columns(), turn_rule(), team_rows(row), schedule_table(who), turn_clock_table(who)")
    else:
        who = argv[1] if len(argv) > 1 else "players"
        t = tables()
        fn = {"players": lambda: t["schedule_table"](), "whitecell": lambda: t["schedule_table"]("whitecell"),
              "turn-clock": lambda: t["turn_clock_table"](), "turn-clock-whitecell": lambda: t["turn_clock_table"]("whitecell")}
        if who not in fn:
            sys.exit(__doc__)
        print(fn[who]())


if __name__ == "__main__":
    main(sys.argv)
