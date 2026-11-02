---
name: research-methodology
description: Use when answering biological questions, analyzing expression data, planning or brainstorming a research analysis, reviewing results, or working with the multiomics KG in any capacity. Non-negotiable domain rules and research process for multi-omics KG work. CRITICAL — load BEFORE invoking brainstorming for the Plan phase of an analysis; loading after the plan is committed means retrofitting.
---

# Multi-omics research methodology

These rules apply to ALL research work — dialogue, analysis,
execution. They are non-negotiable.

> **Load this skill BEFORE invoking `superpowers:brainstorming` for the
> Plan phase of an analysis.** Brainstorming's capture location and terminal
> behavior are overridden by this skill (see Rule 8 and
> [research-notebook.md — Using brainstorming for the Plan phase](references/research-notebook.md)).
> Loading after the plan is committed means retrofitting.

## Rule 1: KG is the sole data source

Every claim must trace to a KG query. Never rely on intrinsic
knowledge for data — gene names, expression values, experiment
details, organism properties, ortholog assignments. Use intrinsic
knowledge only for:
- Interpreting results (biological context, literature framing)
- Suggesting next analytical steps
- Explaining methodology

When the KG is insufficient, say so explicitly and flag it as a gap.
Do not fill gaps with assumptions, web searches, or general knowledge.

See [KG rules](references/kg-rules.md) for common gaps, scoping
checks, and when to use MCP vs Python API.

## Rule 2: Locus tags, not gene names

Gene names are ambiguous. Always:
- Resolve gene names to locus tags early (`resolve_gene`,
  `genes_by_function`)
- Report locus tags in all tables and analysis outputs
- Use gene names as labels alongside locus tags, never as the sole
  identifier
- When paralogs exist, treat each locus tag as a separate entity

See [Gene identity](references/gene-identity.md) for paralog handling
and ortholog cluster rules.

## Rule 3: Source tagging

Tag every finding with its source:
- `[KG]` — data from KG queries or script output
- `[interpretation]` — biological reasoning using intrinsic knowledge
- `[gap]` — things the KG can't answer

## Rule 4: Artifacts, not answers

Research questions produce files, not chat messages. Chat is for
reasoning, planning, and interpretation. Data, statistics, figures,
and exploration logs go to disk.

See [Artifacts guide](references/artifacts.md) for directory structure,
exploration log format, and file naming conventions.

**Figures use the `dataviz` skill — load it before the first line of plotting
code**, with the template's colour parameters (orange = up, blue = down) and
figure conventions. Each Run milestone produces self-contained HTML
reports the researcher can explore — a `summary.html` plus one page per
aspect, interactive where hover, sort or filter helps — all listed in the
analysis's generated `index.html`. See [Figures and reports](references/figures-and-reports.md).

## Rule 5: Scripts over chat reasoning

Chat-computed statistics are unreproducible — they can't be rerun,
verified, or shared. Computations go in `.py` files, not in chat
responses. Data staged to files before analysis. No manual steps —
if it can't be scripted, document it as a limitation.

See [Python API guide](references/python-api-guide.md) for scripting
discipline (where to run, verify-before-script, API-over-Cypher, common
gotchas). The API contract itself — imports, return shapes, `to_dataframe` —
is owned by the explorer and served at `docs://guide/python_api`.

**Call the highest-level tool that answers the question; don't reinvent or
re-wrap what the package ships.** Before building any scoring/statistics
utility, check the package's analysis surface (e.g. `pathway_enrichment` runs
the whole DE→ORA pipeline in one call — don't hand-roll Fisher, and don't wrap
its primitives either). Reserve custom code for composition the tool genuinely
doesn't do. Reinventing risks subtle errors (wrong background, lost
normalization) and wastes effort.

**Exception: interactive discovery steps.** Steps that are
inherently exploratory (browsing available data, classifying
experiments, scoping what the KG contains) may be done
interactively rather than scripted. These steps must still produce
a frozen output file (CSV) and a notebook entry documenting the
reasoning. Computations — statistics, scores, enrichment — always
go in scripts. See [Research notebook — Code lifecycle](references/research-notebook.md#code-lifecycle-analysis-first-productize-later) for the pattern.

## Rule 6: Statistical rigor

Expression data without proper statistical treatment produces
misleading claims — wrong background sets, uncorrected multiple
testing, and magnitude comparisons across platforms are common
failure modes.

See [Statistical rigor](references/statistical-rigor.md) for what
the KG provides, what you must compute in scripts, and what to flag.

## Rule 7: Don't hallucinate

See [Anti-hallucination](references/anti-hallucination.md) for
concrete failure modes and prevention patterns.

## Rule 8: The research arc — Plan, then Run

Every analysis is two phases: a **Plan** phase that converges on a
research proposal, and a **Run** phase that executes against it.
**Open the analysis by posting the arc as a plain-language to-do list**
so the researcher sees the whole path and where you are — ordinary
words, not internal codes.

The arc leans on the superpowers skills where they genuinely fit, and
keeps its own machinery only where research work needs something they
don't provide.

### Plan — uses `superpowers:brainstorming`

The Plan phase is one grounded brainstorming conversation that
converges on a single **`proposal.md`** at the analysis root:

- **Question** — the locked research question, and what it is for: a
  standalone result or part of a paper (or a rewrite of one), and whose
  hypothesis it is — ask; it changes who is anchored to the answer
- **KG entries** — the publications, experiments, organisms, and data
  types that bear on it, *enumerated from the KG, not memory*
- **Framing** — stated concretely (see below)

Three overrides apply to brainstorming here (see
[research-notebook.md](references/research-notebook.md)): the design doc
is `proposal.md` in the analysis folder, not `docs/superpowers/specs/`;
the dialogue is grounded in live KG queries, not assumptions; and the
terminal action is **begin the Run phase**, not `writing-plans`. Each
design-review round is committed; the Plan phase closes with an
approval commit.

**Review the proposal before execution.** The proposal is the
highest-leverage artifact — a flaw propagates through all three Run
milestones and is the most expensive to unwind — so the Plan phase
closes on a review, in order: (1) **self-review** — read `proposal.md`
with fresh eyes for vagueness, a missing stats decision, an
unnamed/uncheckable validation set, a missing falsifiability check /
expected-negative, a missing design-comparability row, or
contradiction, and fix inline;
(2) **critical review** — the fresh-context critic runs on every
proposal, interpretation-only (no data yet), via the `critical-review`
skill; (3) **design review with the researcher** — not a sign-off: the
researcher's design thinking happens here, so present a short list of
the open design choices, each with your recommendation and the critic
findings that bear on it, and expect changes; (4) **delta critic pass**
over whatever the design review changed, then back to (3) until the
researcher approves with no further change. Begin the Run phase only
then. See
[step-protocol.md — The Plan phase](references/step-protocol.md).

**Framing is enumerated, not sketched.** The recurring failure is a
vague plan that looks fine, gets approved, then falls apart in
execution and forces a redo. Concreteness surfaces a bad plan *at plan
time*. Every framing states, specifically:

- **Hypothesis** — in prose
- **Approach** — how you'll analyze and why it answers the question,
  concrete enough to poke holes in (not the code itself)
- **Statistics plan** — a deliberate decision every time: the specific
  statistical test(s) and thresholds, *or* an explicit "no formal
  stats, because descriptive," with the reasoning. Never left implicit.
- **Validation set** — the specific genes or pathways whose behavior is
  already known, named, with the behavior expected if the method works
  ("glnA should score high under N-limitation — if it doesn't,
  something's wrong")
- **Falsifiability check** — named in advance: the result that would say
  the method found *nothing real* (or is only flagging noise), and a
  **pre-registered expected-negative** — a class that should *not* score
  if the signal is genuine. The validation set says what a *hit* looks
  like; this says what a *miss* looks like. Without it a true null and a
  noise result are indistinguishable, and a negative finding cannot be
  trusted. A null is a valid outcome; the evaluation milestone writes it
  up as a bounded negative, not a non-result.
- **Design comparability** — per experiment used: its role; what each
  arm is compared against and that reference sample's physiological
  state (growth phase, nutrient status, sampling day); whether contrasts
  share samples or one fitted model; and what it can and cannot confirm.
  The KG doesn't hold every culture state — **ask the researcher**. A
  comparable metric over incomparable designs is the recurring hole
  (an FDR family size, then a late-decline "early" reference and
  contrasts that were one fitted model).

**Say what the methods milestone is.** If the method *builds* the
entity set (transport systems, a candidate list, tiers, classes), the
methods milestone is a **discovery milestone**: plan for many decisions
at its decide gate and for four verification layers instead of one
spot-run — real-format fixtures, a pilot against an independent
MCP-only answer key, an API-usage review, and a random sample of every
bin before its rule is approved. See
[research-notebook.md — Phase 1](references/research-notebook.md#phase-1--analysis-code-methodology-first).

**Two principles, working together.** *Just-in-time* governs **what**
the plan commits to — only what the data so far supports; no
speculative padding for what the analysis might later need.
*Enumeration* governs **how** it states those commitments — concretely
and reviewably. Ground the conversation in KG counts before you frame;
start with the simplest framing that fits; add predictions or stability
checks only when a specific finding forces them.

See [Research notebook — Just-in-time formalization](references/research-notebook.md#just-in-time-formalization)
for the per-phase concrete rules.

### Run — the iterate loop

The Run phase executes the proposal across three milestones, each in
its own named folder: **`methods/` → `analysis/` → `evaluation/`**.
Each milestone advances through the loop **co-define → do → show →
explore → decide** — the researcher agrees the milestone's scope at
*co-define* (before the work) and approves at *decide* (after it).
**Commit every iteration** (`<slug> <phase>: iteration — …`), and close
each milestone with an approval commit (`… approved — …`) only after
explicit approval. When the evaluation milestone is approved, **ask the
researcher to push** — forks are public, so never push unasked. See
[step-protocol.md — Commit structure](references/step-protocol.md#commit-structure).

- **co-define** — before doing the work, say in plain words what you
  propose this milestone should do and why, and let the researcher
  shape it. Default to co-defining every milestone; the researcher may
  wave through a routine one, but never skip co-define for a genuine
  judgment call (what to compare, how to define a set, which controls).

Research execution is exploratory, so the Run loop is **ours, not
`superpowers:executing-plans`** — that skill assumes a locked,
pre-specified plan with bite-sized tasks, which fights how analysis
actually unfolds. But call the superpowers skills at the beats where
they do fit:

- verifying a new method against hand-computed toy data →
  `superpowers:test-driven-development`
- an analysis that breaks or returns something surprising →
  `superpowers:systematic-debugging`
- before claiming a milestone is done →
  `superpowers:verification-before-completion` (this *is* the
  decide-gate checklist)
- an adversarial second opinion before claims land → the
  `critical-review` skill, at the **analysis** milestone (data-integrity
  + interpretation) and the **evaluation** milestone (interpretation
  only) — and at the **methods** milestone too whenever it emits a data
  artifact that downstream milestones consume (a parts list, a
  classification table, a curated gene set): that file carries claims —
  labels, confidence flags, class assignments — so it gets the
  data-integrity lens, not a pass because "methods is only code."
  The critic reviews only that milestone's own files (the proposal and
  earlier milestones are trusted inputs), with a lens matched to the
  milestone, so the researcher reviews a vetted milestone, not a first
  draft. Kept light: matched lens, milestone-scoped, artifact only when
  it finds something. **A milestone that keeps producing after its
  critic pass earns a delta pass** over the new work before it closes.
  See [step-protocol.md GATE C](references/step-protocol.md).

**Exploration is expected to exceed the plan.** You cannot foresee
everything, and good exploration is *led by* the results. Findings you
did not plan for are welcome — that is discovery, not scope drift. The
only requirement is that they still pass through the decide gate before
being committed as findings.

**Delegate execution to a coding subagent; keep judgment in the main
thread.** The KG queries and script iterations that make up *do* and
*show* generate a lot of noise. Run them in a coding subagent
(`superpowers:subagent-driven-development`) so the researcher-facing
thread keeps only the artifacts and the decisions. Use the template's
**`kg-coder`** agent, which preloads this skill and `dataviz`, and
continue it with `SendMessage` across the milestone. The subagent writes
and runs the scripts, queries the KG, and produces the tables and
figures; it is re-invoked for each exploration question as it arises.
Two rules keep this from quietly breaking the skill's guarantees:

- **The domain rules ride along.** The subagent loads
  `research-methodology` (or at least the KG / gene-identity /
  python-api / anti-hallucination references) into its own context — a
  fresh agent that doesn't know locus-tags-not-names or
  cumulative-vs-per-timepoint counts produces exactly the errors those
  rules prevent. Keep the *same* subagent alive across invocations so
  the rules and analysis context persist and it doesn't re-hallucinate
  on a later call.
- **Artifacts come back, not conclusions.** The subagent returns
  committed scripts, data, figures, logs, and a factual run-manifest
  (what ran, command lines, row counts, candidate anomalies). It does
  not get to *conclude*. The main thread reads the real files and owns
  what they mean — that is what preserves the anomaly-catch (a heatmap
  narrated "all 5 UP" while the data file shows them negative).

**The main thread owns `notebook.md`.** The subagent authors code, data,
figures, and logs; the main thread authors the notebook — pasting the
subagent's factual run-manifest verbatim into the mechanical sections
and writing every interpretive section (Context, what the results mean,
Surprises, Decisions, Advance rationale) itself, with the researcher.
Single owner keeps the judgment record coherent and keeps conclusions
where the researcher is. See
[research-notebook.md — Code lifecycle](references/research-notebook.md#code-lifecycle-analysis-first-productize-later).

### What this replaces

- **No `spec.md` / `plan.md`** — `proposal.md` is the plan; the Run
  milestones execute it
- **No global `decisions.md`** — decisions live in the milestone's
  `notebook.md` where they were forced
- **No `hypotheses.md`** — the hypothesis lives in `proposal.md`
- **No cross-file labels** (H1/P3/D8/T4) — labels are document-scoped
  and must be paired with a short readable name in the same paragraph
- **`proposal.md` + per-milestone `notebook.md` + single `paper.md`**
  at the analysis root replace the single exploration notebook +
  methods.md + caveats.md. `paper.md` is written for the paper's
  reader — journal prose that drops into a manuscript, with no internal
  vocabulary, file paths or process history; its conclusion opens with
  a findings table and numbered meanings, caveats in their own section
- **`gaps_and_friction.md`** (transitional) captures methodology / KG /
  tooling friction — and what worked — each entry type-tagged
  (`[pitfall]`, `[bkm]`, `[kg-gap]`, `[tool]`, `[method-gap]`), distinct
  from decisions

See [Step protocol](references/step-protocol.md) for commit timing,
decide-gate checklist, hard gates, and redo path. See
[Research notebook](references/research-notebook.md) for notebook
format, `paper.md` growth, `gaps_and_friction.md`, and the
brainstorming override for the Plan phase. See
[Artifacts guide](references/artifacts.md) for directory structure and
scaffold creation.

## Rule 9: Plain language; describe before interpreting

Write in plain English. Numbers and direction first, interpretation
second. Don't reach for fancy vocabulary when ordinary words work.

**No unagreed vocabulary with the researcher.** Don't introduce terms,
codes, or step-IDs in conversation that you haven't defined and the
researcher hasn't accepted — internal labels (gene-set IDs, ontology
codes, "decide gate", bare step numbers used as names) read as opaque
shorthand and shut the researcher out. If a technical term is genuinely
needed, say what it means in plain words the first time. The test: could
the researcher restate what you just said back to you? If not, you've
leaned on jargon.

**Banned before the evaluation milestone** — i.e. throughout the Plan
phase and the methods and analysis milestones (these signal commitment
before the analysis has earned it): "striking", "massive", "central
finding", "biologically loaded", "biologically explosive", "reframes",
"rich", "hand-wavy" as praise. Reserve interpretive vocabulary for the
evaluation milestone.

**Describe before interpreting.** Write the numbers and direction
first ("5 markers show RNA log2FC < 0 and protein log2FC > 0 at
coculture days 31–89"). Tag interpretation `[interpretation]` and
list plausible alternatives.

**Verify before generalizing.** Words like "all", "every",
"systematically", "primarily", "no genes" require a query against
the data file, not a heatmap glance. If you write "all 5 are UP",
check all 5 in the data first.

**Proposals must cite specific data or friction.** When suggesting
a fix, framework, or methodology change, point to the data or
incident that motivates it. One occurrence is a note; process
change needs the same friction in two analyses. Don't enumerate
speculative proposals.

See [Anti-hallucination — 2.6 Emotive vocabulary and speculative proposals](references/anti-hallucination.md#26-emotive-vocabulary-and-speculative-proposals).

## References — read on demand, not all at once

- [Step protocol](references/step-protocol.md) — read at the start of every analysis execution; owns commit timing, decide-gate checklist, hard gates, redo path
- [Research notebook](references/research-notebook.md) — read when starting or resuming an analysis; owns notebook format, paper.md growth, gaps_and_friction.md, brainstorming override for the Plan phase
- [Artifacts guide](references/artifacts.md) — read at scaffold time or when unsure about directory structure, per-milestone folders, QC naming
- [Figures and reports](references/figures-and-reports.md) — read before making any figure or report page; owns the colour parameters, figure conventions, and report contents
- [Anti-hallucination](references/anti-hallucination.md) — read before presenting findings; covers tool-schema claims, publication attribution, field semantics, and the other anti-hallucination patterns
- [KG rules](references/kg-rules.md) — read when scoping a new analysis or uncertain about data sourcing vs literature
- [Gene identity](references/gene-identity.md) — read when working with gene names, paralogs, or orthologs
- [Python API guide](references/python-api-guide.md) — read before writing extraction or analysis scripts
- [Statistical rigor](references/statistical-rigor.md) — read when computing enrichment, comparing across studies, or reporting p-values
