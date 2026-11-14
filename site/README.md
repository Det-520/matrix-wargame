# White cell site

The site holds every document in the game: the white cell's handouts, each audience's handouts (with one page per intelligence product), the design documents, and downloads of the release files. It is built with [mdbook](https://rust-lang.github.io/mdBook/). **White cell only:** it shows every team's secrets.

- **Build:** `tools/build_site.sh` from the project root, after `tools/build_handouts.sh`. `tools/build_site.py` writes the pages into `src/`, then mdbook builds them into `book/`. Open `book/index.html`, or host `book/` anywhere that serves static files.
- **Preview:** `tools/build_site.sh serve` opens <http://localhost:3000>.
- **What goes on it:** `pages()` in `tools/build_site.py` lists every page, with its source file and download links. Add a page there when you add a handout.
- **Links:** the build links cross-references such as `RULES.md` §4.5, Rules Handbook §2.3, or a bare §3.2, and reports any that name a section that doesn't exist. Numbered headings get short ids (`#sec-4-5`, `#app-b`).
- **Hand-written:** `book.toml` (mdbook settings; the title comes from `game.toml`), `theme/custom.css` (the audience banners and accents), `theme/head.hbs` (keeps search engines out), and `theme/favicon.svg`.
- **Generated, not in git:** `src/` and `book/`. Don't edit them: change the project markdown and rebuild.
