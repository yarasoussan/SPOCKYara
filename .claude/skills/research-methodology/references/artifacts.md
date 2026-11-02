# Artifacts guide

Research questions produce files, not chat messages. Chat is for reasoning and dialogue; data, statistics, figures, and milestone narratives go to disk.

## Contents

1. [When to create an analysis directory](#when-to-create-an-analysis-directory)
2. [Directory structure per analysis](#directory-structure-per-analysis)
3. [Scaffold creation](#scaffold-creation)
4. [Per-milestone folders](#per-milestone-folders)
5. [paper.md and gaps_and_friction.md](#papermd-and-gaps_and_frictionmd)
6. [Data and figure conventions](#data-and-figure-conventions)
7. [Git tracking](#git-tracking)
8. [Log verbosity](#log-verbosity)
9. [References](#references)

## When to create an analysis directory

Create when:
- The question requires statistical computation
- Multiple data extractions feed into an analysis
- Results need to be shared or revisited
- The work takes more than 2–3 tool calls
- Figures or publication-ready tables are needed

Simple lookups stay in chat:
- "What is gene PMM0120?" — MCP lookup, answer in chat
- "How many genes respond to nitrogen?" — MCP summary, answer in chat
- "List the catalase genes" — MCP query, table in chat

## Directory structure per analysis

```
analyses/<slug>/
  paper.md                  # paper-ready writeup (drops into a manuscript), grows across the arc
  paper.html                # paper.md with figures embedded (generated: scripts/build_paper.py)
  index.html                # front page linking every report + the paper (generated: scripts/build_report_index.py)
  gaps_and_friction.md      # transitional — methodology/KG/tooling friction log
  .gitignore                # per-analysis, created at scaffolding
  proposal.md               # question + KG entries + enumerated framing (the plan)
  proposal_notebook.md      # brainstorming record: grounding queries, counts, rejected alternatives
  proposal_critical_review.md   # only when the proposal critic found something
  methods/
    notebook.md
    reports/                # summary.html + one page per aspect, rebuilt from data/
    <module_name>.py        # ad-hoc methods module
    scripts/, data/, figures/
  analysis/
    notebook.md, reports/, scripts/, data/, figures/
  evaluation/
    notebook.md, reports/, scripts/, data/, figures/
```

**Slug format:** `YYYY-MM-DD-<descriptor>` where descriptor is snake_case, 2–4 words reflecting the research question (e.g., `2026-04-23-n_limitation_signature`). Same-day collisions: append a letter suffix (`-a`, `-b`).

**Why per-milestone folders:** keeps each Run milestone's artifacts self-contained and reviewable; avoids an analysis-wide `scripts/` or `results/` that becomes a dumping ground and loses milestone context. The Plan phase is a conversation, so it produces two files at the root (`proposal.md` + `proposal_notebook.md`), not a folder.

## Scaffold creation

**Who:** Claude proposes the slug; the user approves or counter-proposes.
**When:** at the start of the Plan phase, before any folder or file is written.

1. **Propose a slug** based on the user's initial prompt. Confirm with the user before writing anything — no scaffold exists until the slug is confirmed.
2. **Create the minimal scaffold:**
   ```
   analyses/<slug>/
     paper.md              # skeleton with empty section headers: Question, Background, Methods, Results, Discussion, References
     gaps_and_friction.md  # header only; entries added as friction occurs
     .gitignore            # per-analysis (template below)
     proposal.md           # empty; converges through the Plan-phase brainstorming
     proposal_notebook.md  # empty; captures grounding queries and dialogue
   ```
3. **Run the Plan-phase brainstorming.** `proposal.md` converges (question + KG entries + enumerated framing); `proposal_notebook.md` captures the grounding queries, counts, and rejected alternatives.
4. **Commit as you go:** the scaffold is the first iteration commit; each design-review round is another. **At Plan-phase approval:** `paper.md`'s Question and Background sections are populated and the Plan approval commit lands (see [step-protocol.md — Commit structure](step-protocol.md#commit-structure)).

Run-milestone folders (`methods/`, `analysis/`, `evaluation/`) are created **progressively** — each folder (and its `scripts/` / `data/` / `figures/` subfolders as needed) is created when that milestone begins, not pre-created at scaffold time. This avoids empty folders cluttering the analysis during work in progress.

## Per-milestone folders

Each Run-milestone folder contains:
- **`notebook.md`** — narrative + decide-gate checklist, owned by the main thread (see [research-notebook.md](research-notebook.md))
- **`scripts/`** — Python scripts that do the milestone's work (authored by the coding subagent)
- **`data/`** — script outputs (CSV/TSV); inputs from prior milestones referenced by relative path
- **`figures/`** — static PNG/SVG outputs, made with the `dataviz` skill (see [figures-and-reports.md](figures-and-reports.md))
- **`reports/`** — the milestone's HTML reports: a required `summary.html` plus one page per aspect, self-contained, built by `scripts/build_reports.py` from `data/` and listed in the analysis's `index.html` (see [figures-and-reports.md](figures-and-reports.md#milestone-reports--milestonereports-and-the-analysis-indexhtml))
- **`critical_review.md`** — at the analysis and evaluation milestones, at a methods milestone that emits a data artifact, and after a delta pass; **only when the critic found something**: its findings plus the author's disposition for each (a clean review is a one-line note in `notebook.md`, not a file). See the `critical-review` skill and [step-protocol.md GATE C](step-protocol.md)

The Plan phase has no folder — it produces `proposal.md` + `proposal_notebook.md` at the analysis root (plus `proposal_critical_review.md` when the proposal critic found something), because it is a conversation, not a computation.

### QC artifacts

QC artifacts live in the same `scripts/` / `data/` / `figures/` subfolders with a **`qc_` filename prefix** (e.g., `scripts/qc_check_tp_coverage.py`, `data/qc_tp_coverage.csv`, `figures/qc_tp_coverage_histogram.png`). No separate `qc/` subfolder. The prefix sorts QC files together in listings without creating a binary main/QC split at the folder level.

### Methods module (methods milestone only)

`methods/<module_name>.py` holds the ad-hoc method module (scoring function, enrichment utility, etc.). Subsequent milestones import from it by relative path. See [research-notebook.md — Code lifecycle](research-notebook.md) for the methodology-first → productization-later pattern.

### Script requirements

Scripts must be:
- Self-contained
- Documented at the top (purpose, inputs, outputs)
- Deterministic (seeded if random)
- Have clear I/O — no hardcoded absolute paths; arguments via CLI

### Script naming

- **Pipeline scripts (numbered within the milestone):** `01_select_experiments.py`, `02_compute_scores.py`
- **QC scripts:** `qc_<what_is_checked>.py`
- **Ad-hoc exploration scripts:** `explore_<what>.py` — kept in `scripts/` for reproducibility even if one-off

## paper.md and gaps_and_friction.md

Both live at the analysis root. Content rules are in [research-notebook.md](research-notebook.md):
- `paper.md` — paper-ready writeup for the eventual paper's reader (no internal vocabulary or file paths), skeleton sections from day 1, populated during the Plan phase and each milestone's decide phase
- `gaps_and_friction.md` — transitional friction log, distinct from decisions (which live in milestone notebooks or `proposal.md`)

## Data and figure conventions

### data/
- Format: CSV (preferred) or TSV
- One file per extraction query or script output
- Include metadata columns (organism, experiment_id, locus_tag) when relevant
- Name descriptively: `de_genes_med4_nitrogen.csv`, not `output.csv`

### figures/
- Made with the `dataviz` skill, using the template's colour parameters and figure conventions in [figures-and-reports.md](figures-and-reports.md) (orange = up, blue = down; a colorbar on every heatmap)
- PNG at 300 DPI minimum for notebook inclusion
- SVG (or PDF) for publication-ready figures
- Axis labels, legends, and titles mandatory

## Git tracking

For per-milestone commit timing, hard gates, and redo commits, see [step-protocol.md](step-protocol.md).

### Per-analysis .gitignore

Created during scaffolding (at the start of the Plan phase). Default template:
```
# Large intermediate data reproducible from KG
# (list specific files here, not blanket patterns)
__pycache__/
```

No blanket repo-level rules for `analyses/*/data/` or `analyses/*/figures/`. Tracking decisions are explicit, per-file, and logged in the milestone's `notebook.md`.

### What to track vs gitignore

| Track in git | Gitignore (list explicitly) |
|---|---|
| Signatures, scores, applied subsets (small CSVs) | Raw DE extracts (large CSVs, reproducible from KG) |
| Figures (PNG/PDF/SVG) | `__pycache__/` |
| `notebook.md`, `paper.md`, `gaps_and_friction.md` | |
| Scripts (all) | |

Rule of thumb: if it's small and captures analytical decisions, track it. If it's large and reproducible by rerunning a script, gitignore it explicitly and document the regeneration command in the milestone's `notebook.md` or in `paper.md` Methods.

## Log verbosity

Each milestone's scripts should emit enough diagnostic output to verify the milestone without rerunning. Two capture paths:

- **Short logs:** paste into the milestone's `notebook.md` (Results or Surprises sections)
- **Long logs:** per-script log file at `<milestone>/data/<script_name>.log`, referenced from `notebook.md`

**Minimum content:** summary statistics (row counts, gene counts, filter funnel), diagnostic traces (marker gene values at key stages), edge-case results (tie-breaking outcomes, classification boundary cases).

A log that says "N genes built" is insufficient. A log that shows the filter funnel (how many started → passed each filter → final count), marker gene traces, and classification edge cases is sufficient.

Scripts with `--explore` or `--verbose` flags should write their diagnostic output to the log file as well as stdout. The log is the persistent record; stdout is for the interactive session.

## References

References (publications cited in the analysis) live in **`paper.md`'s References section**, not a separate file. Every reference must be resolved through `list_publications` and cited by DOI — never from intrinsic knowledge (see [anti-hallucination.md — Category 5.2](anti-hallucination.md#52-publication-attribution-from-training-knowledge)).

KG version, tool versions, statistical software, and Python package versions go in `paper.md`'s Methods section.
