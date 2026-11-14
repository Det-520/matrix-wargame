#!/usr/bin/env python3
"""Generate the white cell site's mdbook source (site/src/) from the project markdown.

    tools/build_site.sh            # generate, then mdbook build  -> site/book/
    tools/build_site.sh serve      # generate, then mdbook serve  -> http://localhost:3000
    python3 tools/build_site.py    # generate only

The site has four parts, set out in pages() below:

- Running the game: the white cell's handouts and the timer program.
- Player handouts: what each audience gets (both teams, REDFOR, BLUEFOR), with
  each intelligence product on its own page.
- Designing a scenario: the design guide, rules, event setup, scenario files,
  map guide, writing guide, and repository guide.
- Downloads: build/ (and handouts/word/) exactly as released.

The markdown goes to mdbook almost as written. Front matter becomes the page
heading, audience lines and FORMAT NOTEs are dropped (as in the PDFs), and each
page gets an audience banner and its download links. Numbered headings get
short ids: `## 4.5 Split counters` -> `#sec-4-5`, `## Appendix B` -> `#app-b`.

Cross-references become links (Linker): a file path in backticks
(`RULES.md` §4.5), a document named by its title (Rules Handbook §2.3,
White Cell Forms §4), or a bare section (§3.2, App. B), which points into the
same document or, in a list such as "`RULES.md` §4.3, §5", the one named
just before. A reference to a section that doesn't exist is reported.
"""
import glob
import html
import os
import re
import shutil
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_handouts import FIN, H, PACKET_NAME, REF_PACKET_NAME, ROOT, WC, clean, front_matter, packet_markdown  # noqa: E402
from game import GAME  # noqa: E402

SITE = os.path.join(ROOT, "site")
SRC = os.path.join(SITE, "src")
G = GAME["game"]
WEEK, ASAP = "Common Scenario - 1WK RELEASE", "Common Matrix - ASAP RELEASE"

# Audience banner and accent for each top folder of the site.
AUDIENCE = {
    "whitecell": ("wc", "WHITE CELL ONLY"),
    "common": ("public", "BOTH TEAMS"),
    "redfor": ("red", "REDFOR ONLY"),
    "bluefor": ("blue", "BLUEFOR ONLY"),
    "design": ("wc", "DESIGNER AND WHITE CELL ONLY"),
}


# ---------------------------------------------------------------- the pages

def side_pages(side, label):
    rel = f"{label} - 24H RELEASE"
    letter_dl = [("formatted PDF", f"{rel}/{label} - Commander's Letter.pdf")]
    if os.path.exists(os.path.join(H, "word", f"{label} - Commander's Letter.docx")):
        letter_dl.append(("Word", f"word/{label} - Commander's Letter.docx"))
    intel = []
    for md in sorted(glob.glob(os.path.join(H, side, "intel", f"{side[0].upper()}I-*.md"))):
        code = os.path.basename(md)[:5]
        dl = [("Full Intel PDF", f"{rel}/{label} Full Intel.pdf")]
        for w in glob.glob(os.path.join(H, "word", code + " *.docx")):
            name = os.path.splitext(os.path.basename(w))[0]
            dl = [("formatted PDF", f"word/{name}.pdf"), ("Word", f"word/{name}.docx")]
        intel.append(dict(src=os.path.relpath(md, ROOT), page=f"{side}/intel/{code.lower()}.md", dl=dl, intel=True))
    return [
        dict(src=f"handouts/{side}/commanders-letter.md", page=f"{side}/commanders-letter.md", title="Commander's Letter", dl=letter_dl),
        dict(src=f"handouts/{side}/team-packet.md", page=f"{side}/team-packet.md", title="Team Packet",
             dl=[("PDF", f"{rel}/{label} Team Packet.pdf")]),
        dict(src=f"handouts/{side}/order-of-battle.md", page=f"{side}/order-of-battle.md", title="Order of Battle",
             dl=[("PDF", f"{rel}/{label} Order of Battle.pdf"), ("counters", f"{rel}/counters.pdf")]),
        dict(src=f"handouts/{side}/intel/00-read-me-first.md", page=f"{side}/intel/index.md", title="Intelligence Products",
             dl=[("Full Intel PDF", f"{rel}/{label} Full Intel.pdf")], children=intel),
    ]


def pages():
    """The site, as [(part title, [page])]. A page is a dict: src (repo path, or None), page (site path),
    title (else the front matter's short title or the first heading), dl [(label, path in build/)],
    children, text (markdown used in place of the file), intel (an intelligence product), note (a line above the page)."""
    return [
        ("Running the game", [
            dict(src="handouts/whitecell/checklist.md", page="whitecell/checklist.md",
                 dl=[("PDF", f"{WC}/White Cell Checklist.pdf")]),
            dict(src="handouts/whitecell/handbook.md", page="whitecell/handbook.md",
                 dl=[("PDF", f"{WC}/White Cell Handbook.pdf")]),
            dict(src="handouts/whitecell/table-setup.md", page="whitecell/table-setup.md",
                 dl=[("PDF", f"{WC}/White Cell Table Setup Guide.pdf")]),
            dict(src="handouts/whitecell/likely-plans.md", page="whitecell/likely-plans.md",
                 dl=[("PDF", f"{WC}/White Cell Likely Plans.pdf")]),
            dict(src="handouts/whitecell/intel-and-injects.md", page="whitecell/intel-and-injects.md", title="Intelligence and Injects",
                 dl=[("PDF", f"{WC}/White Cell Intelligence and Injects.pdf")]),
            dict(src="handouts/whitecell/master-asset-list.md", page="whitecell/master-asset-list.md",
                 dl=[("PDF", f"{WC}/Master Asset List.pdf"), ("counters", f"{WC}/counters.pdf")]),
            dict(src="handouts/whitecell/forms.md", page="whitecell/forms.md",
                 dl=[("PDF", f"{WC}/White Cell Forms.pdf")]),
            dict(src="handouts/whitecell/print-packet.md", page="whitecell/print-packet.md", text=packet_markdown(),
                 dl=[("PDF, one table", f"{WC}/{PACKET_NAME}"), ("PDF, reference forms only", f"{WC}/{REF_PACKET_NAME}")]),
            dict(src=None, page="whitecell/timer.md", title="Timer and Dice Program", text=TIMER),
        ]),
        ("Player handouts", [
            dict(src=None, page="common/index.md", title="Both Teams", text=INTROS["common"], children=[
                dict(src="handouts/common/rules-handbook.md", page="common/rules-handbook.md",
                     dl=[("PDF", f"{ASAP}/Player Rules Handbook.pdf")],
                     note=None if GAME["rules"]["set"] == "full" else
                     "**Not released in this game.** It uses the basic rules (`game.toml` `[rules]`), so players get the "
                     "Basic Rules instead. The full rules are here for the white cell's reference."),
                dict(src="handouts/common/basic-rules.md", page="common/basic-rules.md",
                     dl=[("PDF", f"{ASAP}/Basic Rules.pdf")]),
                dict(src="handouts/common/player-forms.md", page="common/player-forms.md",
                     dl=[("PDF", f"{ASAP}/Player Forms and Templates.pdf")]),
                dict(src="handouts/common/scenario-brief.md", page="common/scenario-brief.md",
                     dl=[("PDF", f"{WEEK}/Scenario Brief.pdf"), ("map", f"{WEEK}/map-full.pdf"), ("map tiles", f"{WEEK}/map-tiles.pdf")]),
                dict(src="handouts/common/scenario-schedule.md", page="common/scenario-schedule.md",
                     dl=[("PDF", f"{WEEK}/Scenario Schedule.pdf")]),
                dict(src="handouts/common/starting-conditions.md", page="common/starting-conditions.md",
                     dl=[("PDF", f"{WEEK}/Starting Conditions.pdf")]),
            ]),
            dict(src=None, page="redfor/index.md", title="REDFOR", text=INTROS["redfor"], children=side_pages("redfor", "REDFOR")),
            dict(src=None, page="bluefor/index.md", title="BLUEFOR", text=INTROS["bluefor"], children=side_pages("bluefor", "BLUEFOR")),
        ]),
        ("Designing a scenario", [
            dict(src="README.md", page="design/getting-started.md", title="Getting Started"),
            dict(src="DESIGN-GUIDE.md", page="design/design-guide.md", title="Design Guide"),
            dict(src="RULES.md", page="design/rules.md", title="Full Rules"),
            dict(src="EVENT-SETUP.md", page="design/event-setup.md", title="Event Setup"),
            dict(src="scenario/README.md", page="design/scenario/index.md", title="Scenario Files", children=[
                dict(src="scenario/00-overview.md", page="design/scenario/overview.md", title="Scenario Overview"),
                dict(src="scenario/redfor-packet.md", page="design/scenario/redfor-packet.md", title="REDFOR Packet"),
                dict(src="scenario/bluefor-packet.md", page="design/scenario/bluefor-packet.md", title="BLUEFOR Packet"),
                dict(src="scenario/whitecell-injects.md", page="design/scenario/injects.md", title="Injects"),
                dict(src="scenario/whitecell-ground-truth.md", page="design/scenario/ground-truth.md", title="Ground Truth"),
            ]),
            dict(src="map/README.md", page="design/map.md", title="Map"),
            dict(src="references/tongue-and-quill-summary.md", page="design/writing-guide.md", title="Writing Guide"),
            dict(src="AGENTS.md", page="design/repository-guide.md", title="Repository Guide"),
        ]),
    ]


def walk(items):
    for p in items:
        yield p
        yield from walk(p.get("children", []))


def all_pages(site):
    for _, items in site:
        yield from walk(items)


# ---------------------------------------------------------------- generated text

TIMER = """# Timer and Dice Program

The lead adjudicator runs this program on the room's TV, where both teams can see it. It keeps the whole run of show on one screen: the block and turn timers, the dice, the result bands, the estimative vote, the parley timer, and the tracks.

**[Open the timer and dice program](../tools/whitecell-clock.html)**. Once it has loaded it works offline; save the page to keep a copy.

- It holds durations only, so it runs at any start time. If `game.toml` sets a start time, each block shows its planned start.
- Its run of show, turn steps, and tracks come from `game.toml` (`[schedule]`, `[[block]]`, `[[turn_step]]`, `[[track]]`), the same settings that make the schedule tables in the handouts. Its result bands and estimative vote follow `RULES.md` §4.
- **Setup** (top right) changes the schedule, the turn steps, and the tracks in the browser. **Apply** saves the change in that browser only. **Download page** saves a copy of the program with the change built in, for the room's laptop. **Copy as game.toml** gives the text to paste into `game.toml`, so the next build carries it into the handouts and this site.
"""

INTROS = {
    "common": "# Both Teams\n\nReleased to every player. Nothing here is secret.\n\n"
              "- **As soon as possible**, before the scenario is announced: the Rules Handbook and Player Forms.\n"
              "- **One week before**: the Scenario Brief, Scenario Schedule, Starting Conditions, and the map.\n",
    "redfor": "# REDFOR\n\nReleased to REDFOR only, 24 hours before the event. Never show these pages to BLUEFOR.\n",
    "bluefor": "# BLUEFOR\n\nReleased to BLUEFOR only, 24 hours before the event. Never show these pages to REDFOR.\n",
}


def demo_note():
    """With MW_DEMO=1 (the base's GitHub Pages build), say what the site is and where its source is."""
    if not os.environ.get("MW_DEMO"):
        return ""
    repo = os.environ.get("GITHUB_REPOSITORY")
    src = f" The source is at [{repo}]({os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{repo})." if repo else ""
    return ("> **Demo.** This is the matrix wargame base, built from its placeholder scenario (Redland and Blueland) "
            "to show what the tools make: the handouts, the release PDFs, and the "
            "[timer and dice program](tools/whitecell-clock.html). A real scenario's site shows both sides' secrets, "
            f"so don't publish one where players can find it.{src}\n\n")


def index_page(site):
    by_src = {p["src"]: p for p in all_pages(site)}

    def ln(src, title=None):
        return "[%s](%s)" % (title or by_src[src]["title"], by_src[src]["page"])
    rows = "\n".join("| **%s** | %s |" % (part, ", ".join("[%s](%s)" % (p["title"], p["page"]) for p in items))
                     for part, items in site)
    return f"""# {G['name']}

<p class="mw-subtitle">{html.escape(G['event'])} · {html.escape(G['date'])}</p>

{demo_note()}Every document in the game, for the designer, the lead adjudicators, and the loggers. This site shows **both sides' secrets**: hidden assets, secret objectives, intelligence ground truth, and injects. Keep it off every screen the players can see.

## During the game

- [Timer and dice program](tools/whitecell-clock.html), on the room's TV
- {ln('handouts/whitecell/checklist.md')}: everything to do, in order, from a week out to cleanup
- {ln('handouts/whitecell/handbook.md')}: running a turn, adjudication, scoring
- {ln('handouts/whitecell/table-setup.md')}: devices, table layout, and where every counter starts
- {ln('handouts/whitecell/likely-plans.md')} and {ln('handouts/whitecell/intel-and-injects.md')}
- {ln('handouts/whitecell/master-asset-list.md')} and {ln('handouts/whitecell/forms.md')}

## Before the game

- {ln('handouts/whitecell/print-packet.md')}: everything one table prints, in one PDF
- [Downloads](downloads.md): every release folder, as it goes to each audience
- {ln('DESIGN-GUIDE.md')}: building or changing the scenario

## What's here

| Part | Pages |
| --- | --- |
{rows}
| **Downloads** | [Release files](downloads.md) |

The banner at the top of each page says who may see it. To search, press `S` or use the magnifier. Every page is generated from the project markdown by `tools/build_site.sh`: change the markdown, not the site.
"""


# ---------------------------------------------------------------- headings and references

SEC_HEAD = re.compile(r"^#{1,3} +(?:(\d+(?:\.\d+)*)\.?|Appendix ([A-Z])\b)(?= )")


def sec_id(num=None, app=None):
    return "sec-" + num.replace(".", "-") if num else "app-" + app.lower()


def headings(text):
    """The section ids a document's headings define."""
    return {sec_id(*m.groups()) for m in (SEC_HEAD.match(ln) for ln in text.split("\n")) if m}


def add_ids(text):
    """Give numbered headings short ids, at the end of the line: `## 4.5 Title {#sec-4-5}`."""
    def one(line):
        m = SEC_HEAD.match(line)
        return f"{line} {{#{sec_id(*m.groups())}}}" if m else line
    return "\n".join(one(ln) for ln in text.split("\n"))


# Documents named by title. "Handbook" and "Team Packet" alone depend on where they appear (Linker.doc_for_title).
TITLES = {
    "Player Rules Handbook": "handouts/common/rules-handbook.md",
    "Rules Handbook": "handouts/common/rules-handbook.md",
    "Basic Rules": "handouts/common/basic-rules.md",
    "White Cell Handbook": "handouts/whitecell/handbook.md",
    "White Cell Checklist": "handouts/whitecell/checklist.md",
    "White Cell Forms": "handouts/whitecell/forms.md",
    "Table Setup Guide": "handouts/whitecell/table-setup.md",
    "Intelligence and Injects": "handouts/whitecell/intel-and-injects.md",
    "Likely Plans": "handouts/whitecell/likely-plans.md",
    "Master Asset List": "handouts/whitecell/master-asset-list.md",
    "Scenario Brief": "handouts/common/scenario-brief.md",
    "Scenario Schedule": "handouts/common/scenario-schedule.md",
    "Starting Conditions": "handouts/common/starting-conditions.md",
    "Player Forms": "handouts/common/player-forms.md",
    "REDFOR Team Packet": "handouts/redfor/team-packet.md",
    "BLUEFOR Team Packet": "handouts/bluefor/team-packet.md",
    "Design Guide": "DESIGN-GUIDE.md",
    "EVENT-SETUP": "EVENT-SETUP.md",
    "Team Packet": None,
    "Handbook": None,
    "Rules": "RULES.md",
}
TITLE_ALT = "|".join(re.escape(t) for t in sorted(TITLES, key=len, reverse=True))
SEC = r"(?:§§? ?(?P<num>\d+(?:\.\d+)*)|App\. ?(?P<app>[A-F])\b)"
REF = re.compile(
    r"(?P<named>(?:`(?P<path>[\w./-]+\.md)`|(?<![\w-])(?P<title>" + TITLE_ALT + r"))(?:,? (?P<sec>" + SEC + r"))?)"
    r"|(?P<bare>" + SEC.replace("?P<num>", "?P<bnum>").replace("?P<app>", "?P<bapp>") + r")")
LIST_GAP = re.compile(r"^(?:,|;|,? and|,? or)? ?$")
PUBLICATION = re.compile(r"(?:AFDP|JP|AFH|AFI|AFMAN) [\d.-]+,? $")


class Linker:
    def __init__(self, site):
        self.page = {}      # repo path -> site page
        self.ids = {}       # repo path -> its section ids
        for p in all_pages(site):
            if p["src"]:
                self.page[p["src"]] = p["page"]
                self.ids[p["src"]] = headings(source_text(p)[1])
        self.problems = []

    def resolve_path(self, path):
        if path in self.page:
            return path
        hits = [s for s in self.page if s.endswith("/" + path)]
        return hits[0] if len(hits) == 1 else None

    @staticmethod
    def doc_for_title(title, here):
        if title == "Handbook":
            return "handouts/whitecell/handbook.md" if here.startswith("handouts/whitecell/") else "handouts/common/rules-handbook.md"
        if title == "Team Packet":
            side = re.match(r"handouts/(redfor|bluefor)/", here)
            return f"handouts/{side.group(1)}/team-packet.md" if side else None
        return TITLES[title]

    def href(self, here_page, doc, anchor=None):
        if self.page[doc] == here_page and anchor:
            return "#" + anchor
        rel = os.path.relpath(self.page[doc], os.path.dirname(here_page) or ".")
        return rel + ("#" + anchor if anchor else "")

    def anchor(self, doc, num, app, here, shown):
        """The id of a section, or of its nearest parent. None (and a report) if there is none."""
        if app:
            if sec_id(app=app) in self.ids[doc]:
                return sec_id(app=app)
        else:
            parts = num.split(".")
            while parts:
                if sec_id(".".join(parts)) in self.ids[doc]:
                    return sec_id(".".join(parts))
                parts.pop()
        self.problems.append(f"{here}: '{shown}' names no section of {doc}")
        return None

    def line(self, text, here, here_page):
        out, pos, last_doc, last_end = [], 0, None, -1
        for m in REF.finditer(text):
            start, end = m.span()
            if m.group("named"):
                doc = self.resolve_path(m.group("path")) if m.group("path") else self.doc_for_title(m.group("title"), here)
                if not doc or (m.group("title") and not m.group("sec")):
                    continue  # unknown, or a title on its own: just a name
                if m.group("sec"):
                    a = self.anchor(doc, m.group("num"), m.group("app"), here, m.group(0))
                    if a is None:
                        continue
                elif doc == here:
                    continue
                else:
                    a = None
                last_doc = doc
            else:
                before = text[:start]
                if PUBLICATION.search(before) or re.search(r"\w['’]s $", before):
                    continue  # a doctrine publication's appendix, or "each packet's §1"
                doc = last_doc if last_doc and LIST_GAP.match(text[last_end:start]) else here
                if doc not in self.page:
                    continue
                a = self.anchor(doc, m.group("bnum"), m.group("bapp"), here, m.group(0))
                if a is None:
                    continue
            last_end = end
            out += [text[pos:start], "[%s](%s)" % (m.group(0), self.href(here_page, doc, a))]
            pos = end
        out.append(text[pos:])
        return "".join(out)

    def link(self, text, here, here_page):
        """Link the references in a page's markdown, outside code blocks, headings, HTML, inline code, and links."""
        out, fence = [], False
        for ln in text.split("\n"):
            if re.match(r"^\s*(```|~~~)", ln):
                fence = not fence
            if fence or re.match(r"^\s*(#{1,6} |<)", ln):
                out.append(ln)
                continue
            keep = []

            def hide(m):
                if re.fullmatch(r"`[\w./-]+\.md`", m.group(0)):
                    return m.group(0)  # a path we may link
                keep.append(m.group(0))
                return "\x00%d\x00" % (len(keep) - 1)
            masked = re.sub(r"!?\[[^\]]*\]\([^)]*\)|`[^`]*`", hide, ln)
            out.append(re.sub(r"\x00(\d+)\x00", lambda m: keep[int(m.group(1))], self.line(masked, here, here_page)))
        return "\n".join(out)


# ---------------------------------------------------------------- writing pages

def read(src):
    return open(os.path.join(ROOT, src), encoding="utf-8").read()


def quote(path):
    return "/".join(urllib.parse.quote(p) for p in path.split("/"))


def banner(page):
    cls, text = AUDIENCE.get(page.split("/")[0], ("wc", "WHITE CELL ONLY"))
    return f'<div class="mw-banner mw-aud-{cls}">// {text} //</div>\n\n'


def downloads_line(page, files):
    up = os.path.relpath("downloads", os.path.dirname(page) or ".")
    links = " · ".join('<a href="%s/%s">%s</a>' % (quote(up), quote(p), html.escape(label)) for label, p in files)
    return f'<p class="mw-downloads"><span>Download</span> {links}</p>\n\n'


def heading(meta):
    """The front matter's title and subtitle as the page heading. In "Operation Example — X" the first part goes above."""
    kicker, _, main = meta["title"].partition(" — ")
    if not main:
        kicker, main = "", meta["title"]
    out = f'<p class="mw-kicker">{html.escape(kicker)}</p>\n\n' if kicker else ""
    out += f"# {main}\n\n"
    if meta.get("subtitle"):
        out += f'<p class="mw-subtitle">{html.escape(meta["subtitle"])}</p>\n\n'
    return out


def first_heading(text):
    m = re.search(r"^#{1,2} (.+)$", text, re.M)
    return re.sub(r"[*_`]", "", m.group(1)).strip() if m else None


def source_text(p):
    """A page's markdown, without front matter, audience lines, or FORMAT NOTEs: (meta, text)."""
    meta, text = front_matter(p.get("text") or read(p["src"]))
    if p["src"]:
        text = clean(text, is_intel=p.get("intel", False), where=p["src"])
    return meta, text


def fix_images(text, src, page):
    """Copy the images a page uses into src/assets/img/ and point the markdown at them."""
    def one(m):
        alt, path = m.group(1), m.group(2)
        if re.match(r"^[a-z]+:", path):
            return m.group(0)
        full = os.path.normpath(os.path.join(ROOT, os.path.dirname(src), path))
        os.makedirs(os.path.join(SRC, "assets", "img"), exist_ok=True)
        shutil.copyfile(full, os.path.join(SRC, "assets", "img", os.path.basename(full)))
        return "![%s](%s)" % (alt, os.path.relpath(os.path.join("assets", "img", os.path.basename(full)), os.path.dirname(page)))
    text = re.sub(r"\)\{width=[^}]*\}", ")", text)
    return re.sub(r"!\[((?:[^\]]|\][^(])*)\]\(([^)]+)\)", one, text)


def draw_boxes(text):
    """A form's ☐ as a drawn box, as in the PDFs (custom.css), not a font glyph of varying size.
    Code blocks keep the character, since HTML there would show as text."""
    out, fence = [], False
    for ln in text.split("\n"):
        if re.match(r"^\s*(```|~~~)", ln):
            fence = not fence
        out.append(ln if fence else ln.replace("☐", '<span class="mw-box" aria-hidden="true">☐</span>'))
    return "\n".join(out)


def write_page(p, linker):
    meta, text = source_text(p)
    if p["src"]:
        text = fix_images(text, p["src"], p["page"])
    here = p["src"] or p["page"]
    body = linker.link(add_ids(text), here, p["page"])
    body = draw_boxes(body)
    if meta.get("title"):
        head = heading(meta)
    else:
        m = re.search(r"^# .*\n", body, re.M)
        head, body = (body[:m.end()], body[m.end():]) if m else (f"# {p['title']}\n", body)
    if not p["src"] and p.get("children"):
        body += "\n" + "\n".join("- [%s](%s)" % (c["title"], os.path.relpath(c["page"], os.path.dirname(p["page"])))
                                 for c in p["children"]) + "\n"
    # a file this build didn't release (the Player Rules Handbook under the basic rules) gets no link
    dl = [(label, f) for label, f in p.get("dl", [])
          if os.path.exists(os.path.join(H, f) if f.startswith("word/") else os.path.join(FIN, f))]
    note = f"> {p['note']}\n\n" if p.get("note") else ""
    out = banner(p["page"]) + head.strip() + "\n\n" + (downloads_line(p["page"], dl) if dl else "") + note + body.strip() + "\n"
    path = os.path.join(SRC, p["page"])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)


def downloads_page():
    dst = os.path.join(SRC, "downloads")
    shutil.copytree(FIN, dst)
    word = os.path.join(H, "word")
    if os.path.isdir(word) and any(f.endswith((".pdf", ".docx")) for f in os.listdir(word)):
        shutil.copytree(word, os.path.join(dst, "word"))
    lines = [banner("downloads.md").strip(), "", "# Downloads", "",
             "The release files exactly as they go to each audience. Each release folder goes only to the audience its name gives."
             + (" `word` holds the Tongue and Quill documents as Word files, for editing." if os.path.isdir(os.path.join(dst, "word")) else ""), ""]
    for folder in sorted(os.listdir(dst)):
        if os.path.isdir(os.path.join(dst, folder)):
            lines += [f"## {folder}", ""]
            lines += ["- [%s](downloads/%s)" % (f, quote(f"{folder}/{f}")) for f in sorted(os.listdir(os.path.join(dst, folder)))]
            lines.append("")
    with open(os.path.join(SRC, "downloads.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def summary(site):
    lines = ["# Summary", "", "[Home](index.md)", ""]

    def item(p, depth):
        lines.append("%s- [%s](%s)" % ("  " * depth, p["title"].replace("[", "\\[").replace("]", "\\]"), p["page"]))
        for c in p.get("children", []):
            item(c, depth + 1)
    for part, items in site:
        lines += [f"# {part}", ""]
        for p in items:
            item(p, 0)
        lines.append("")
    lines += ["---", "", "[Downloads](downloads.md)", ""]
    return "\n".join(lines)


def main():
    if not os.path.isdir(FIN):
        sys.exit("build/ is missing: run tools/build_handouts.sh first")
    if os.path.isdir(SRC):
        shutil.rmtree(SRC)
    os.makedirs(os.path.join(SRC, "tools"))
    shutil.copyfile(os.path.join(ROOT, "tools", "whitecell-clock.html"), os.path.join(SRC, "tools", "whitecell-clock.html"))

    site = pages()
    for p in all_pages(site):
        if "title" not in p:
            meta, text = source_text(p)
            p["title"] = meta.get("short") or first_heading(text) or os.path.basename(p["page"])
    linker = Linker(site)
    for p in all_pages(site):
        write_page(p, linker)
    downloads_page()
    with open(os.path.join(SRC, "index.md"), "w", encoding="utf-8") as f:
        f.write(banner("index.md") + index_page(site))
    with open(os.path.join(SRC, "SUMMARY.md"), "w", encoding="utf-8") as f:
        f.write(summary(site))

    for problem in linker.problems:
        print("unresolved reference:", problem)
    print("generated", os.path.relpath(SRC, ROOT))


if __name__ == "__main__":
    main()
