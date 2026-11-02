# Figures and reports

Every figure in an analysis is made with the **`dataviz` skill** (bundled with
Claude Code). Load it before writing the first line of plotting code, in the
coding subagent as well as the main thread. It owns the method: pick the form,
assign colour by the job it does, validate, apply mark specs, add hover, check
accessibility, render and look. This file supplies only what dataviz leaves to the
project: the **colour parameters** below, the **figure conventions** research
figures need, and the **milestone report**.

Each Run milestone produces two kinds of visual output:

| Output | For whom | Where |
|---|---|---|
| Static figures (PNG ≥ 300 DPI + SVG) | `paper.md`, slides, the eventual paper | `<milestone>/figures/` |
| HTML reports — a `summary.html` plus one page per aspect | the researcher, throughout the milestone and at the decide gate | `<milestone>/reports/`, all listed in `analyses/<slug>/index.html` |

## Colour parameters (the template's dataviz "design system")

Use these in place of dataviz's reference diverging pair and sequential hue.
Everything else (categorical order, surfaces, ink, status colours) is dataviz's
reference palette unchanged.

| Job | Light | Dark | Notes |
|---|---|---|---|
| Diverging — **up** (log2FC > 0) | orange `#eb6834` | `#d95926` | dataviz categorical slot 2 |
| Diverging — **down** (log2FC < 0) | blue `#2a78d6` | `#3987e5` | dataviz categorical slot 1 |
| Diverging — midpoint (0 / no change) | gray `#f0efec` | `#383835` | dataviz neutral midpoint |
| Sequential — ranks, percentiles, counts | violet ramp, matplotlib `Purples` | — | one hue, never blue (blue already means "down") |
| Ordinal tiers (e.g. confidence tiers) | `#9e9ac8, #7b74b5, #61409b, #470f84` | `#9e9ac8, #7b74b5, #61409b` | lightest step clears 2:1 on the surface |

Validated with dataviz's validator (orange/blue poles pass all checks all-pairs in
both modes; the tier ramps pass `--ordinal`). If you add a palette, validate it —
the Python validator runs without Node:

```bash
uv run python -I -X utf8 "<dataviz base dir>/scripts/validate_palette.py" "#2a78d6,#eb6834" --mode light --pairs all
```

The dataviz skill prints its base directory when it loads. Keep `-X utf8` on
Windows: `-I` ignores `PYTHONUTF8`, and the report's arrows crash a cp1252 console.

Matplotlib form of the diverging map — symmetric limits so zero sits on the gray:

```python
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
SPOCK_DIVERGING = LinearSegmentedColormap.from_list(
    "spock_diverging", ["#2a78d6", "#f0efec", "#eb6834"])   # down, 0, up
lim = np.nanmax(np.abs(values))
norm = TwoSlopeNorm(vmin=-lim, vcenter=0, vmax=lim)
```

Every figure script reads its numbers from the milestone's `data/` CSVs (never
from values typed into the script) and saves both forms, under the same stem:

```python
def save_figure(fig, stem: Path) -> None:
    """stem = <milestone>/figures/<name>, no suffix."""
    fig.savefig(stem.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(stem.with_suffix(".svg"), bbox_inches="tight")
```

## Figure conventions for research figures

Applied on top of dataviz's mark specs and anti-patterns:

- **Direction colours never swap.** Orange = up, blue = down, in every figure of
  every milestone. Say which contrast "up" means in the axis or colorbar label
  ("log2FC, coculture vs axenic").
- **Fold change over rank percentiles** when the reader needs to judge size. Label
  both ends of the axis or colorbar in words ("← lower in coculture · higher in
  coculture →"). Use ranks only when comparing across platforms, and then say so.
- **Every heatmap has a colorbar**, with units, and a **divider between condition
  blocks** (e.g. axenic | coculture, or one per experiment) so arms can't be read
  as one series.
- **Label genes as `name (locus_tag)`** or locus tag alone — never name alone (Rule 2).
- **Summary figures stay at one word per cell** ("up", "down", "flat", "n/a") or one
  number. Dense text grids go to a table, not a figure.
- **One layer and one platform per panel.** RNA and protein, or microarray and
  RNA-seq, go in separate panels with the layer named in each panel title — never
  one shared axis (see [statistical-rigor.md](statistical-rigor.md#cross-omics-comparison-rna-vs-protein)).
- **Captions state what is plotted, from which experiments, and n.** A caption is
  description, not interpretation (Rule 9).

## Milestone reports — `<milestone>/reports/` and the analysis `index.html`

**What they are.** Self-contained HTML pages that let the researcher look at a
milestone's results instead of reading about them: the findings, the figures,
and tables they can sort and filter. A report is a view of the milestone's
files, not a new source of claims.

**Layout.** One page per *aspect*, so no single page carries everything:

```
analyses/<slug>/
  index.html                    # front page: every report, by milestone (generated)
  methods/reports/
    summary.html                # required: the milestone's entry page
    transport_tiers.html        # one page per aspect worth looking at on its own
  analysis/reports/
    summary.html
    coculture_vs_axenic.html
  evaluation/reports/
    summary.html                # the analysis's conclusion page
```

- **`summary.html` (required, one per milestone)**, in this order:
  1. **What this milestone asked** — two or three plain sentences from the
     co-define agreement.
  2. **Findings table** — the same summary table as `notebook.md` Results.
  3. **Links to the milestone's aspect pages**, one line each.
  4. **Files** — relative links to the scripts, data and figures behind it.
- **Aspect pages (as many as the data needs)** — one question each ("tier members
  per strain", "coculture vs axenic by route"), with its figures, captions and
  sortable data tables (locus tags in every table). Split when a page needs
  scrolling past unrelated figures to reach the next point; name the file by the
  aspect, in snake_case.
- **Every page carries `<title>` and `<meta name="description" content="one
  line">`.** The index is built from these two tags.
- The evaluation `summary.html` is the analysis's conclusion page: its findings
  table is the conclusion's findings table, followed by the numbered meanings
  (see [research-notebook.md — paper.md growth pattern](research-notebook.md#papermd-growth-pattern)).

**Iterate in place.** Reports change many times inside a milestone, as the
researcher asks for follow-ups. Rebuild the page; don't keep `_v2` copies or
dated variants. Git history is the record of earlier versions, and the decide
commit captures the state that was approved.

**The index.** `analyses/<slug>/index.html` lists every report, grouped by
milestone (summary first), plus links to `paper.md` and `proposal.md`. It is
generated, never hand-written. Rebuild it whenever a page is added, renamed or
retitled:

```bash
uv run python scripts/build_report_index.py analyses/<slug>
```

It warns about pages missing a title or description. Tell the researcher to
bookmark the index: it is the one page to open.

**The paper, rendered.** `paper.md` stays the source (it is what drops into a
manuscript), and `scripts/build_paper.py` renders it as `paper.html` at the
analysis root, with every figure embedded and every table in place: one file
to read, send, or print to PDF. Rebuild it whenever `paper.md` or a figure it
cites changes; it exits non-zero, with a visible placeholder in the page, when
a referenced figure is missing:

```bash
uv run python scripts/build_paper.py analyses/<slug>
```

The paper cites the static PNG/SVG figures, not the interactive reports.

**Interactive when it helps.** Add interaction where the reader would otherwise go
back to the CSV: hover on heatmap cells and points to show gene name, locus tag,
experiment, value and padj; sort and filter on gene tables; toggles to show one
experiment or organism at a time. A figure with a handful of values stays static.
dataviz's interaction reference covers the hover layer and filter placement.

**How they are built.**
- The coding subagent writes `scripts/build_reports.py` in the milestone folder,
  which reads the milestone's `data/` and writes every page in `reports/`. Pages
  are rebuilt from the data, never edited by hand.
- **Self-contained and offline:** data inlined as JSON, plain HTML/SVG/JS per
  dataviz, no CDN or network fetch. A page must open by double-click from a lab
  laptop and still work from a git checkout years later. Share the page's look:
  one small CSS block with the colour parameters above, reused by every page.
- **Printable, for a PDF.** Include an `@media print` block (light colours,
  hidden filter controls, no page break inside a figure or table row), so the
  browser's Print → Save as PDF gives a clean PDF to send or archive. No PDF
  tooling is needed.
- **The main thread owns their words.** The "what this milestone asked" text and
  any interpretation come from `notebook.md`, which the main thread writes; the
  subagent does not compose conclusions for a report.
- **Render and look before presenting** (dataviz step 7): open each changed page,
  check the numbers in the findings table against `data/`, and check labels don't
  collide. A report whose numbers disagree with `notebook.md` is a Blocker.
