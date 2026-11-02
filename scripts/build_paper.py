"""Render analyses/<slug>/paper.md as paper.html — one self-contained file.

Purpose: a readable, sendable version of the paper draft with its figures and
tables in place. Figures referenced from paper.md are embedded in the HTML
(base64), so paper.html is one file that opens offline and can be mailed. For a
PDF, open paper.html in a browser and use Print → Save as PDF; the page carries
print styles (no figure split across pages).

Inputs:  analyses/<slug>/paper.md. Figures are referenced with markdown image
         syntax, paths relative to paper.md, with the caption as alt text:
             ![Fig. 1. Transport genes up in coculture …](analysis/figures/fig1.png)
         Tables are GitHub-style markdown tables.
Output:  analyses/<slug>/paper.html. Missing figures are reported and left as
         a visible placeholder, so the build never hides a broken reference.

Usage (from the repo root):
    uv run python scripts/build_paper.py analyses/2026-11-03-my_question
    uv run python scripts/build_paper.py            # every analysis with a paper.md
"""
from __future__ import annotations

import argparse
import base64
import html
import re
import sys
from pathlib import Path

import markdown

MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".svg": "image/svg+xml", ".gif": "image/gif"}

CSS = """
:root { color-scheme: light; }
body { margin: 0; background: #f9f9f7; color: #0b0b0b;
  font: 16px/1.6 system-ui, -apple-system, "Segoe UI", sans-serif; }
main { max-width: 780px; margin: 0 auto; padding: 40px 24px 80px; background: #fcfcfb; }
h1 { font-size: 26px; line-height: 1.25; }
h2 { font-size: 19px; margin-top: 2em; border-bottom: 1px solid #e1e0d9; padding-bottom: 4px; }
h3 { font-size: 16px; }
figure { margin: 1.5em 0; text-align: center; break-inside: avoid; }
figure img { max-width: 100%; height: auto; }
figcaption { font-size: 14px; color: #52514e; text-align: left; margin-top: 6px; }
.missing { border: 2px dashed #d03b3b; color: #d03b3b; padding: 16px; }
table { border-collapse: collapse; margin: 1.2em 0; font-size: 14px;
  font-variant-numeric: tabular-nums; break-inside: avoid; }
th, td { border-bottom: 1px solid #e1e0d9; padding: 4px 10px; text-align: left; vertical-align: top; }
th { border-bottom: 2px solid #c3c2b7; }
code { font-size: 13px; }
@media print {
  body, main { background: #fff; }
  main { max-width: none; padding: 0; }
  h2 { break-after: avoid; }
}
"""

IMG = re.compile(r'<p>\s*<img alt="([^"]*)" src="([^"]+)"\s*/?>\s*</p>')


def embed_figures(body: str, base: Path) -> tuple[str, list[str]]:
    """Turn each standalone <img> into a <figure> with the image inlined."""
    missing = []

    def repl(m: re.Match) -> str:
        alt, src = html.unescape(m.group(1)), html.unescape(m.group(2))
        caption = f"<figcaption>{html.escape(alt)}</figcaption>" if alt else ""
        path = (base / src).resolve()
        mime = MIME.get(path.suffix.lower())
        if src.startswith(("http:", "https:", "data:")) or not mime or not path.exists():
            missing.append(src)
            return (f'<figure><div class="missing">Figure not found: '
                    f"{html.escape(src)}</div>{caption}</figure>")
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        return (f'<figure><img alt="{html.escape(alt)}" '
                f'src="data:{mime};base64,{data}">{caption}</figure>')

    return IMG.sub(repl, body), missing


def build(root: Path) -> list[str]:
    src = root / "paper.md"
    text = src.read_text(encoding="utf-8")
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])
    body, missing = embed_figures(body, root)
    m = re.search(r"^#\s+(.+)$", text, re.M)
    title = m.group(1).strip() if m else root.name
    page = ("<!DOCTYPE html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">\n"
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f"<title>{html.escape(title)}</title>\n"
            f'<meta name="description" content="Paper draft rendered from paper.md">\n'
            f"<style>{CSS}</style></head><body><main>\n{body}\n</main></body></html>\n")
    (root / "paper.html").write_text(page, encoding="utf-8")
    return missing


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("analyses", nargs="*", type=Path,
                    help="analysis folders (default: every analysis with a paper.md)")
    args = ap.parse_args(argv)
    roots = args.analyses or sorted(p.parent for p in Path("analyses").glob("*/paper.md"))
    status = 0
    for root in roots:
        if not (root / "paper.md").exists():
            print(f"skip {root}: no paper.md", file=sys.stderr)
            continue
        missing = build(root)
        for src in missing:
            print(f"warning: {root / 'paper.md'}: figure not found: {src}", file=sys.stderr)
            status = 1
        print(f"wrote {root / 'paper.html'}")
    return status


if __name__ == "__main__":
    sys.exit(main())
