#!/usr/bin/env python3
"""The run of show in game.toml ([schedule], [[block]], [[turn_step]], [[track]]) as
schedule tables and a configured timer program.

    python3 tools/schedule.py                    # print the players' schedule table
    python3 tools/schedule.py whitecell          # print the white cell's table
    python3 tools/schedule.py --write            # refresh the generated tables and the timer's settings
    python3 tools/schedule.py --check            # exit 1 if any of them is out of date
    python3 tools/schedule.py --clock OUT.html   # write a copy of the timer program set up from game.toml

--write (run by tools/build_handouts.sh and tools/build_site.sh, so the PDFs, the site, and
the timer always match game.toml) fills in the settings block in tools/whitecell-clock.html
and every generated table, which sits between two comments in the markdown:

    <!-- mw:begin schedule -->            players: what each block asks of them
    <!-- mw:begin schedule-whitecell -->  white cell: what to do and say in each step
    <!-- mw:end -->

Clock times count from [schedule] start; with no start they are minutes from the start
of the game. Standard library only.
"""
import html
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from game import GAME, ROOT, clock_config, clock_time, fill, fmt_num, run_of_show  # noqa: E402

CLOCK_SRC = os.path.join(ROOT, "tools", "whitecell-clock.html")
CONFIG_RE = re.compile(r'(<script type="application/json" id="mw-config">)(.*?)(</script>)', re.S)
REGION_RE = re.compile(r"(<!-- mw:begin (schedule(?:-whitecell)?) -->\n)(.*?)(<!-- mw:end -->)", re.S)
WORDS = ["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]


def cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def span(a, b):
    return f"{clock_time(a)}–{clock_time(b)}"


def count(n):
    return WORDS[n] if n < len(WORDS) else str(n)


def turns_name(b):
    rng = f"Turn {b['first']}" if b["first"] == b["last"] else f"Turns {b['first']}–{b['last']}"
    return f"{b['name']} – {rng}"


def turns_text(b, sep=" · "):
    n, length = len(b["turns"]), fmt_num(b["turn_len"])
    head = f"{count(n).capitalize()} {length}-minute turn{'s' if n != 1 else ''}:"
    return head + " " + sep.join(f"**Turn {t}:** {span(a, z)}" for t, a, z in b["turns"])


def text(b, s, key):
    return fill(s.get(key, ""), first=b.get("first", ""), last=b.get("last", ""), min=s.get("min", ""))


def players_table():
    rows = ["| Time | Min | Block | What you do |", "| --- | --- | --- | --- |"]
    for b in run_of_show():
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
    return "\n".join(rows) + "\n"


def whitecell_table():
    rows = ["| Clock | Min | Block / step | White cell actions |", "| --- | --- | --- | --- |"]
    for b in run_of_show():
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
    return "\n".join(rows) + "\n"


TABLES = {"schedule": players_table, "schedule-whitecell": whitecell_table}


def markdown_files():
    try:
        out = subprocess.run(["git", "ls-files", "*.md"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
        files = out.split()
    except (OSError, subprocess.CalledProcessError):
        files = [os.path.relpath(os.path.join(d, f), ROOT) for d, _, fs in os.walk(ROOT) for f in fs if f.endswith(".md")]
    return [f for f in files if not f.startswith(("references/", "build/", "site/book/", "site/src/"))]


def refresh(write):
    """Fill in every generated table. Returns the files that were (or would be) changed."""
    tables = {k: f() for k, f in TABLES.items()}
    changed = []
    for rel in markdown_files():
        path = os.path.join(ROOT, rel)
        with open(path, encoding="utf-8") as f:
            old = f.read()
        if "mw:begin schedule" not in old:
            continue
        new = REGION_RE.sub(lambda m: m.group(1) + tables[m.group(2)] + m.group(4), old)
        if new != old:
            changed.append(rel)
            if write:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)
    old, new = clock_html()
    if new != old:
        changed.append(os.path.relpath(CLOCK_SRC, ROOT))
        if write:
            write_clock(CLOCK_SRC)
    return changed


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
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(clock_html()[1])


def main(argv):
    if "--clock" in argv:
        write_clock(argv[argv.index("--clock") + 1])
    elif "--write" in argv or "--check" in argv:
        changed = refresh("--write" in argv)
        for rel in changed:
            print(("updated " if "--write" in argv else "out of date: ") + rel)
        if "--check" in argv and changed:
            sys.exit("Run python3 tools/schedule.py --write")
    elif len(argv) <= 1 or argv[1] in TABLES or "schedule-" + argv[1] in TABLES:
        name = argv[1] if len(argv) > 1 else "schedule"
        sys.stdout.write(TABLES.get(name, TABLES.get("schedule-" + name))())
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
