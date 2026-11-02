"""Build analyses/<slug>/index.html — the front page linking every report.

Purpose: one page per analysis that lists every HTML report the milestones
produced, grouped by milestone (methods → analysis → evaluation), plus links to
the analysis's paper and proposal. Run it whenever a report is added, renamed
or retitled; it is cheap and deterministic (no timestamps), so re-running it
only changes index.html when the set of reports changes.

Inputs:  analyses/<slug>/<milestone>/reports/*.html (summary.html listed
         first in each milestone, the rest alphabetically). Each report should carry
         <title> and <meta name="description" content="one line">; both are
         read for the listing (a report missing either is listed by file name
         and reported as a warning).
Output:  analyses/<slug>/index.html (self-contained, opens offline).

Usage (from the repo root):
    uv run python scripts/build_report_index.py analyses/2026-11-03-my_question
    uv run python scripts/build_report_index.py            # every analysis
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

MILESTONES = [
    ("methods", "Methods"),
    ("analysis", "Analysis"),
    ("evaluation", "Evaluation"),
]
ROOT_DOCS = [
    ("paper.html", "Paper draft, with figures (print to PDF from here)"),
    ("paper.md", "Paper draft (markdown source)"),
    ("proposal.md", "Proposal (the plan)"),
]


class _HeadReader(HTMLParser):
    """Collect <title> text and <meta name="description"> content."""

    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.description = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "meta" and (a.get("name") or "").lower() == "description":
            self.description = (a.get("content") or "").strip()

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def read_report(path: Path) -> tuple[str, str, list[str]]:
    """Return (title, description, warnings) for one report file."""
    reader = _HeadReader()
    reader.feed(path.read_text(encoding="utf-8", errors="replace"))
    title = " ".join(reader.title.split())
    warnings = []
    if not title:
        warnings.append(f"{path}: no <title>; listed by file name")
        title = path.stem.replace("_", " ")
    if not reader.description:
        warnings.append(f'{path}: no <meta name="description">')
    return title, reader.description, warnings


def analysis_title(root: Path) -> str:
    """First markdown heading of proposal.md, else the folder name."""
    proposal = root / "proposal.md"
    if proposal.exists():
        for line in proposal.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.match(r"#\s+(.+)", line)
            if m:
                return m.group(1).strip()
    return root.name


def collect(root: Path) -> tuple[list[tuple[str, list[tuple[str, str, str]]]], list[str]]:
    """Reports grouped by milestone: [(label, [(href, title, description)])]."""
    groups, warnings = [], []
    known = {name for name, _ in MILESTONES}
    extra = sorted(p.name for p in root.iterdir()
                   if p.is_dir() and p.name not in known and (p / "reports").is_dir())
    for name, label in MILESTONES + [(n, n) for n in extra]:
        items = []
        pages = sorted((root / name / "reports").glob("*.html"),
                       key=lambda p: (p.name != "summary.html", p.name))
        for page in pages:
            title, desc, w = read_report(page)
            warnings += w
            items.append((page.relative_to(root).as_posix(), title, desc))
        groups.append((label, items))
    return groups, warnings


CSS = """
:root { color-scheme: light dark; }
body { margin: 0; background: #f9f9f7; color: #0b0b0b;
  font: 15px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }
main { max-width: 760px; margin: 0 auto; padding: 32px 20px 64px; }
h1 { font-size: 22px; margin: 0 0 4px; }
h2 { font-size: 15px; margin: 28px 0 8px; color: #52514e;
  text-transform: uppercase; letter-spacing: .04em; }
.sub { color: #52514e; margin: 0 0 20px; }
ul { list-style: none; margin: 0; padding: 0; }
li { background: #fcfcfb; border: 1px solid rgba(11,11,11,.10);
  border-radius: 6px; padding: 10px 14px; margin: 0 0 8px; }
a { color: #256abf; font-weight: 600; text-decoration: none; }
a:hover { text-decoration: underline; }
.desc { color: #52514e; display: block; font-weight: 400; }
.empty { color: #898781; font-style: italic; }
@media (prefers-color-scheme: dark) {
  body { background: #0d0d0d; color: #f0efec; }
  h2, .sub, .desc { color: #c3c2b7; }
  li { background: #1a1a19; border-color: rgba(255,255,255,.10); }
  a { color: #5598e7; }
}
"""


def render(root: Path) -> tuple[str, list[str]]:
    groups, warnings = collect(root)
    e = html.escape
    out = [
        "<!DOCTYPE html>",
        '<html lang="en"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{e(analysis_title(root))} — reports</title>",
        f"<style>{CSS}</style></head><body><main>",
        f"<h1>{e(analysis_title(root))}</h1>",
        f'<p class="sub">{e(root.name)} · built by scripts/build_report_index.py</p>',
    ]
    docs = [(f, label) for f, label in ROOT_DOCS if (root / f).exists()]
    if docs:
        out.append("<h2>Documents</h2><ul>")
        out += [f'<li><a href="{e(f)}">{e(label)}</a>'
                f'<span class="desc">{e(f)}</span></li>' for f, label in docs]
        out.append("</ul>")
    for label, items in groups:
        out.append(f"<h2>{e(label)}</h2>")
        if not items:
            out.append('<p class="empty">No reports yet.</p>')
            continue
        out.append("<ul>")
        for href, title, desc in items:
            line = f'<li><a href="{e(href)}">{e(title)}</a>'
            if desc:
                line += f'<span class="desc">{e(desc)}</span>'
            out.append(line + "</li>")
        out.append("</ul>")
    out.append("</main></body></html>\n")
    return "\n".join(out), warnings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("analyses", nargs="*", type=Path,
                    help="analysis folders (default: every folder in analyses/)")
    args = ap.parse_args(argv)
    roots = args.analyses or sorted(p for p in Path("analyses").iterdir() if p.is_dir())
    for root in roots:
        if not root.is_dir():
            print(f"skip {root}: not a folder", file=sys.stderr)
            continue
        page, warnings = render(root)
        (root / "index.html").write_text(page, encoding="utf-8")
        for w in warnings:
            print(f"warning: {w}", file=sys.stderr)
        print(f"wrote {root / 'index.html'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
