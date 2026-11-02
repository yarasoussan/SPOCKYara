# Phase protocol

An analysis is two phases: a **Plan** phase that converges on `proposal.md`, and a **Run** phase that executes it across three milestones (`methods/` → `analysis/` → `evaluation/`). Each Run milestone advances through the rhythm **co-define → do → show → explore → decide** (phase content defined in [research-notebook.md](research-notebook.md)). This document owns **when things happen and what gates enforce them**.

The **just-in-time formalization** principle applies throughout: terms, metrics, stability checks, decisions, and caveats enter the analysis only when the data demands them. *Enumeration* is its partner — within what the plan does commit to, be concrete, because a vague-but-approved plan is what forces redos. See [research-notebook.md](research-notebook.md) for both principles and their application to the Plan phase framing.

## Commit structure

**Commit every iteration; mark approval with its own commit.** Work changes many times inside a phase — proposal revisions after each design-review round, each round of do / explore, each critic pass and its dispositions, each rebuild of the reports. Each of those is committed, so git holds every version the researcher saw, not only the approved one. Reports and notebooks are rebuilt or overwritten in place; the commits are what keep their history.

Two kinds of commit, told apart by the message:

| Commit | When | Message |
|---|---|---|
| **Iteration** | after every round that changed files — before presenting it to the researcher | `<slug> <phase>: iteration — <what changed, one line>` |
| **Approval** | at decide, only after the researcher's explicit approval (GATE E) | `<slug> <phase>: approved — <advance rationale>` |

`<phase>` is `plan`, `methods`, `analysis` or `evaluation`. Example: `2026-11-03-n_release methods: iteration — tier rule v3, bin samples for Medium`.

- **The main thread commits**, never the coding subagent — it has just read the files and owns what the round means.
- **Commit everything the round produced**, including `usage/` logs, rebuilt `reports/`, `index.html` and `paper.html`. Leave nothing modified across a researcher hand-off.
- **Never amend or squash** an iteration commit; a wrong turn stays in history as the record of what was tried.
- **Iteration commits are not approval.** Only an `approved` commit closes a phase; GATE B and GATE E are about that commit.

The **approval commit** of each phase must leave the tree holding everything the phase produced:

**Plan approval commit:**
- `proposal.md` (question + KG entries + enumerated framing)
- `proposal_notebook.md` (the brainstorming record: KG-grounding queries, counts, rejected alternatives)
- `proposal_critical_review.md` where the proposal critic found something
- the scaffold (analysis folder, `paper.md` skeleton, `gaps_and_friction.md` header) — see [artifacts.md](artifacts.md)
- `paper.md` Question + Background sections populated

**Run milestone approval commit:**
- `notebook.md` (narrative + decide-gate checklist)
- `scripts/`, `data/`, `figures/` (main + `qc_*` files)
- `reports/` (the milestone's HTML reports, rebuilt from `data/`), plus the regenerated `index.html` and `paper.html` at the analysis root
- updates to `paper.md` (the milestone's synthesis section)
- updates to `gaps_and_friction.md` (if the milestone encountered friction)
- `critical_review.md` where the critic found something (analysis + evaluation milestones; methods when it emits a data artifact; any delta pass)

The decide phase is still the milestone boundary: the approval commit is what the next milestone builds on.

**When the analysis is done, request a push.** After the evaluation milestone's approval commit, ask the researcher to push — don't push unasked, because forks are public (see the README). Show what will go: the branch, the commits not yet on the remote (`git log --oneline @{u}..` or, with no upstream yet, the whole branch), and a reminder that the analysis and its usage logs become public. Push only on a yes; if the researcher declines or wants to hold it back (unpublished work), say so in the evaluation `notebook.md`. The researcher may also ask to push after any approval commit — same request, same check.

## The Plan phase

The Plan phase is one grounded `superpowers:brainstorming` conversation (three overrides — see [research-notebook.md — Using brainstorming for the Plan phase](research-notebook.md)). The output is `proposal.md` plus its brainstorming record: committed after each design-review round, and closed by the Plan approval commit.

**Framing is enumerated.** The proposal's framing states, concretely: hypothesis; approach (how and why, not code); a deliberate statistics decision (the specific test and thresholds, or an explicit reasoned "none"); a named validation set (the genes/pathways whose behavior is already known, with the behavior expected if the method works); a falsifiability check (the result that would say the method found nothing real, plus a pre-registered expected-negative class that should *not* score); and design comparability (per experiment: its role, what each arm is compared against and that reference's physiological state, whether contrasts share samples or a fitted model, and what it can and cannot confirm — asking the researcher for culture states the KG doesn't hold). See [research-notebook.md](research-notebook.md#just-in-time-formalization) for the floor. The proposal also says what the result is for (standalone, or part of a paper) and whose hypothesis it is.

**Plan the methods milestone by what it produces.** If the method constructs the entity set (a parts list, candidate set, tiers, classes), say so in the proposal: it is a discovery milestone, with many decisions at its decide gate and the four verification layers in [research-notebook.md — Phase 1](research-notebook.md#phase-1--analysis-code-methodology-first).

**Close gate — review the proposal before execution.** The proposal is the highest-leverage artifact; a flaw in it propagates through all three Run milestones and is the most expensive to unwind. Before the Run phase begins, in order:

1. **Self-review** — read `proposal.md` with fresh eyes: is the framing enumerated (stats decision actually made, validation set named and checkable, falsifiability check + expected-negative named, a design-comparability row per experiment)? any vagueness, placeholder, or internal contradiction? Fix inline. This is the direct catch for the vague-plan-that-forces-a-redo failure.
2. **Critical review (automatic; interpretation only)** — dispatch the fresh-context critic via the `critical-review` skill over `proposal.md`. There is no data yet, so the lens is interpretation only (testability, controls, confounders, whether the statistics decision, validation set, and expected-negative fit the question). Findings + dispositions go to `proposal_critical_review.md`; a clean review is a one-line note in `proposal_notebook.md`. Resolve every Blocker before proceeding. See [GATE C](#gate-c-critical-review-before-a-claim-bearing-artifact-is-shown).
3. **Design review with the researcher** — this is where the researcher's design thinking happens, so expect changes rather than a sign-off. Present a **short list of the open design choices** (what is compared, how the set is defined, which controls, what is deferred), each with your recommendation and the critic's findings that bear on it; `proposal.md` and the `paper.md` Question + Background are there to read, not the thing presented. Fold in the researcher's changes.
4. **Delta critic pass after changes** — if the design review changed the framing (it usually does), re-dispatch the critic over what changed, with the already-reviewed proposal as a trusted input. Repeat 3–4 until the researcher approves with no further design change. Only then does the Plan approval commit land and the Run phase begin. *(N-import coculture: four approval prompts in a row were answered with design input, growing the proposal from 205 to 330 lines; two scoped delta passes caught one Blocker and five Concerns in the additions.)*

## Before starting a Run milestone

- The Plan approval commit exists, `proposal.md` is populated
- The previous milestone's commit exists (for analysis and evaluation)
- The previous milestone's `notebook.md` has the decide-gate checklist populated and its `paper.md` section written

If any of these is missing, close the previous phase first.

## Delegation (Run phase)

The KG queries and script iterations of *do* and *show* run in a coding subagent (`superpowers:subagent-driven-development`), keeping the researcher-facing thread clean. See [SKILL.md Rule 8 — Run](../SKILL.md) for the two guardrails. In gate terms:

- The subagent authors **scripts, data, figures, logs, and a factual run-manifest**. It does not conclude.
- The main thread authors **`notebook.md`, `paper.md`, `gaps_and_friction.md`, critical-review dispositions, and the decide-gate checklist** — pasting the subagent's run-manifest verbatim into the mechanical notebook sections and writing every interpretive section itself.
- Keep the **same subagent** alive across a milestone's invocations so the domain rules and analysis context persist.
- Use the template's **`kg-coder`** agent (`.claude/agents/kg-coder.md`) for this role: it preloads `research-methodology` and `dataviz`, so the rules ride along by configuration. Continue it with `SendMessage` (by name or the agent ID it returned) for each new exploration question rather than spawning a fresh one; spawn a new one only if it has lost the thread.

Where no subagents are available, the same work is done inline — same rules, same artifacts, same ownership.

## "co-define" phase (Run milestones)

Before doing any of the milestone's work, propose it to the researcher in plain language: what it should produce, the main judgment calls you expect, and why. Let the researcher adjust scope or approach. Begin only once you've agreed.

This is the front-end mirror of the decide gate: decide closes a milestone with researcher approval; co-define opens it with researcher agreement. No artifacts are produced here — it is a short conversation that sets scope. Default to co-defining every milestone; the researcher may wave through routine ones, but never skip co-define for a genuine judgment call (what to compare, how to define a gene set, which controls). Keep it in plain language — no internal codes or undefined jargon (see [SKILL.md Rule 9](../SKILL.md)).

## "do" phase (Run milestones)

The coding subagent does the milestone's work:

- **methods:** implement the approach the proposal committed to as an ad-hoc Python module; verify against hand-computed toy data (`superpowers:test-driven-development`), with fixtures in the **real artifact's serialization form** and a main-thread spot-run on one real row — a green suite over the wrong input type is not evidence. When the method **constructs the entity set**, the spot-run is replaced by four layers before scaling: real-serialization fixtures → a pilot against an independent MCP-only answer key → an API-usage review against the explorer's source and docs → a random sample of each bin before any tier or class rule is approved (see [research-notebook.md — Phase 1](research-notebook.md#phase-1--analysis-code-methodology-first))
- **analysis:** run the method; produce scored outputs, figures, tables
- **evaluation:** assess results against the framing; QC scripts for sensitivity/stability where a result triggers them

Every figure is made with the `dataviz` skill and the template's colour parameters, and every milestone produces HTML reports in `reports/` — a `summary.html` plus one page per aspect, rebuilt in place as the work iterates (see [figures-and-reports.md](figures-and-reports.md)).

Outputs land where they naturally belong: scripts in `scripts/`, their outputs in `data/` and `figures/`. QC artifacts use the `qc_` prefix (see [artifacts.md](artifacts.md)). No commit yet — outputs are uncommitted working-tree state until decide.

## "show" phase (Run milestones)

The main thread populates `notebook.md` from the subagent's returned artifacts and run-manifest. Recommended sections (see [research-notebook.md](research-notebook.md)):

- **Context** — what this milestone is for; what the proposal or prior milestone set up
- **What I did** — scripts run with command lines for non-trivial cases; KG queries issued (lifted from the subagent's run-manifest)
- **Results** — summary tables shown inline as markdown tables (not prose paraphrases); links to full tables in `data/` and figures in `figures/`; cited publications resolved via `list_publications` (never from memory — see [anti-hallucination.md — Category 5](anti-hallucination.md#category-5-source-of-truth-verification-failures))

Summary tables in **Results** are the same tables presented to the researcher in chat — the real numbers the subagent produced, copied as markdown, not paraphrased.

## "explore" phase (Run milestones)

Investigate anomalies, surprises, or gaps. Each exploration question is a new request to the same coding subagent (continued, not respawned), which returns the artifact that answers it; the main thread and researcher read it and interpret. Add `qc_*.py` checks; run sensitivity analyses; cross-validate against the validation set. Capture anomalies worth flagging as **Surprises** in `notebook.md`.

**Exploration is expected to exceed the plan.** Findings you did not plan for are welcome — that is discovery, not scope drift — provided they still pass through the decide gate before being committed. If a researcher question produces a data point or changes interpretation, both the prose and the data live in the notebook; the narrative IS the exploration record.

## "decide" phase (Run milestones)

1. **Finalize `notebook.md`** (main thread):
   - Ensure Context / What I did / Results / Surprises are populated as applicable
   - Add a **Decisions** section if any forks were taken (prose + date; see [research-notebook.md](research-notebook.md))
   - Write the **decide-gate checklist** at the end:
     - **Outputs produced** — filenames in `scripts/`, `data/`, `figures/`, with command lines for non-trivial scripts
     - **Results presented** — summary tables shown inline; links to full tables and figures
     - **QC gate** — what was checked → result (one line per check)
     - **Decisions made this milestone** — prose + date, if any; omit if none
     - **Advance rationale** — one line, why this milestone is ready to close

2. **Update `paper.md`:** write the synthesis for the section this milestone populates, as journal prose that drops into a manuscript as is — no internal vocabulary, file paths or process history; figures by number with captions; at evaluation, the Discussion opens with the findings table and numbered meanings. See [research-notebook.md — paper.md growth](research-notebook.md#papermd-growth-pattern).

   **Rebuild the reports, the index and the paper:** rebuild the milestone's `reports/` from `data/` (`scripts/build_reports.py`), then from the repo root `uv run python scripts/build_report_index.py analyses/<slug>` and `uv run python scripts/build_paper.py analyses/<slug>` (it fails on a figure `paper.md` references but that doesn't exist). Open `summary.html` and check its findings table against `notebook.md`. See [figures-and-reports.md](figures-and-reports.md#milestone-reports--milestonereports-and-the-analysis-indexhtml).

3. **Append to `gaps_and_friction.md`** if friction was encountered (KG issues, MCP schema mismatches, methodology gaps, anti-hallucination corrections). Two checks before moving on, both cheap:
   - **Every friction the notebook references has an entry.** If `notebook.md` says "see `gaps_and_friction.md`," the entry exists. A dangling pointer means the friction was noticed and lost.
   - **A critic finding that exposed a gap the framing didn't anticipate is friction, not just a disposition.** Dispositions record what you fixed in *this* analysis; friction is what the next analysis needs to know. Log both. Later milestones are where this slips — the log tends to go quiet exactly when the run gets heavy and the lessons get expensive. *(Alteromonas coculture: the friction log stopped three days before the analysis and evaluation milestones ran, so an FDR-family-size comparability trap that reshaped the whole cross-experiment read survives only as a critic disposition; separately, a subagent context-overflow death was cited from the notebook but never written up.)*

4. **Critical review (analysis and evaluation — automatic; methods automatic when it emits a data artifact):** before presenting to the researcher, dispatch the fresh-context critic via the `critical-review` skill. It reviews **only this milestone's own files** (the proposal and earlier milestones are trusted inputs) with a lens matched to the milestone: **analysis** gets data-integrity + interpretation (the heavy gate, where computed results first appear); **evaluation** gets interpretation only (it judges whether conclusions are earned by the already-vetted analysis results); **methods** gets data-integrity + interpretation whenever it emits a data file that later milestones consume, and is on demand otherwise. Methodology compliance is not the critic's job — it lives in your decide-gate checklist. If the critic finds anything, write its findings and your disposition for each to `{MILESTONE}/critical_review.md` and resolve every Blocker (fix, or dispute with a specific data citation) before the milestone closes; if it comes back clean, add a one-line `Critical review: clean (<lens>)` to `notebook.md` and write no file. If the milestone's claims expand after the pass (explore runs after the critic by construction), re-dispatch over the delta with the already-reviewed files as trusted inputs before closing. See [GATE C](#gate-c-critical-review-before-a-claim-bearing-artifact-is-shown).

5. **Present state to researcher:** point them at the analysis `index.html` first (it is how they look at the results), then show the `notebook.md` content, the `paper.md` diff, any `gaps_and_friction.md` additions, and — where the review produced findings — `critical_review.md` with your dispositions. Wait for explicit approval or redirect.

6. **On approval, make the approval commit** (`<slug> <milestone>: approved — …`), containing whatever the last iteration commit didn't. Changes after a redirect are iteration commits; only explicit approval earns the `approved` message.

7. **At the evaluation milestone, request the push** (see [Commit structure](#commit-structure)).

8. Begin the next milestone (create its folder as needed — see [artifacts.md](artifacts.md)).

## Redo path

When the researcher says "redo the analysis milestone with X" (or any milestone):

1. **do:** update script or approach; rerun; regenerate outputs. New artifacts overwrite old in the milestone folder.
2. **show / explore:** new tables, figures, Results; update Surprises if changed.
3. **decide:** new decide-gate checklist, new `paper.md` synthesis, new `gaps_and_friction.md` entry if the redo surfaced friction. **Iteration commits, then a new approval commit (never amend the previous).**

The previous commit remains in git history as the record of what was tried. The working-tree `notebook.md` is overwritten because it now describes what actually happened in the successful attempt — it is not a log of prior attempts.

If the redo invalidates downstream milestones, the redo's `notebook.md` must list the downstream milestones that consumed its outputs. The researcher decides whether to cascade. `gaps_and_friction.md` is append-only: redo friction entries accumulate.

## Reopen path (a data reveal reopens the locked proposal)

The redo path handles "redo milestone N and cascade downstream." A different case: while executing a Run milestone, the data itself contradicts an assumption baked into the **locked `proposal.md`** (the question or the framing). The lock is provisional until the data behind it has actually been pulled — "locked at end of the Plan phase" is not "frozen against what the data turns out to be." Grounding the Plan phase in live KG queries catches many such reveals during planning; the rest surface in the Run phase.

When this happens: **reopen the proposal, don't paper over it.** Edit `proposal.md` to record (a) the original lock, (b) the data reveal that triggered the reopening, and (c) the evolved question/framing — then re-lock and continue. Add a `gaps_and_friction.md` entry. This is distinct from the redo path (which cascades *forward*); here a downstream reveal edits an *upstream* lock.

**Real example (Alteromonas coculture analysis):** the question "does motility go up or down in coculture?" was reopened when enumerating the KG revealed that every usable coculture contrast runs in a medium with no added organic carbon — reframing it around a carbon-provision hypothesis. The original lock was edited (original + evolved question + a decision), not silently replaced.

## Hard gates

### GATE A: Co-define before doing

The first dogfood analysis executed an internal plan and surfaced finished work for review — the researcher reacted to results instead of shaping the milestone. **Do not start a Run milestone's work before proposing it in plain language and getting the researcher's agreement.** Co-define opens the milestone; decide closes it. (Routine milestones may be waved through, but genuine judgment calls never are.) The Plan phase's equivalent gate is brainstorming's present-design-and-approve step.

### GATE B: Milestone boundary

Early analyses partially wrote notebooks retroactively — exploration reasoning was lost and couldn't be verified against the actual data state at the time.

**Do not start milestone N+1 until milestone N's approval commit exists, including `notebook.md`, `paper.md` updates, and `gaps_and_friction.md` updates if applicable.** Likewise, do not start the Run phase until the Plan approval commit exists.

### GATE C: Critical review before a claim-bearing artifact is shown

Across analyses, wrong narratives survived because the author was anchored to them — a control heatmap narrated "all 5 are UP" while the data file showed them negative; a per-arm starvation contrast narrated as "coculture vs axenic"; a control row double-counting pooled and per-timepoint genes. The author who wrote the story cannot reliably see its holes; a fresh reader of the data files can.

**Do not present a claim-bearing artifact to the researcher until the `critical-review` critic has run with the artifact's lens and every Blocker it raised is resolved** — fixed, or disputed with a specific file-and-number citation (not "I'm confident"). Reviewed automatically: **the proposal** (before the Run phase begins) — interpretation only, no data yet; **the analysis milestone** — data-integrity + interpretation, the heavy gate; **the evaluation milestone** — interpretation only; and **the methods milestone whenever it emits a data artifact** that downstream milestones consume — data-integrity + interpretation. The critic reviews only that artifact's own files; earlier phases are trusted inputs. Where the critic finds anything, the findings and your dispositions are committed with the phase (`proposal_critical_review.md` for the proposal, `critical_review.md` in the milestone folder otherwise); a clean review is a one-line note in `proposal_notebook.md` or `notebook.md`. Keep it light — see the three bounding rules in the [critical-review skill](../../critical-review/SKILL.md).

**Methods is not exempt because "it's only code."** When the method includes *constructing the entity set* — a parts list, a curated candidate set, a classification table — that file carries claims (substrate labels, confidence flags, class assignments) and every downstream score inherits them. A methods milestone whose only output is a toy-tested function stays on demand; one that hands the analysis milestone a table does not. *(Alteromonas coculture: the on-demand methods critic found a soluble PTS phosphocarrier sitting in the candidate set as a confident sugar importer, plus a `[KG]`-tagged carrier count 30% high that had already reached `paper.md`.)*

**Re-review on expansion — expect it, don't treat it as an edge case.** The critic pass is point-in-time, and the **explore** phase runs *after* it by construction: researcher-requested follow-ons, new scripts, new figures and new conclusions routinely land during decide. If a milestone's claims **materially expand after its pass**, re-dispatch the critic over the delta before closing, listing the already-reviewed files as trusted inputs. A milestone that explores after its critic pass and closes without a delta pass is closing unreviewed work. **The same holds for the Plan phase:** the design review at its close routinely changes the framing after the proposal critic ran, so changes there get a scoped delta pass too. *(Alteromonas coculture: the analysis critic came back clean on data integrity; the delta pass over the exploration that followed returned a Blocker — a figure caveat citing the wrong module's number, which had inverted its interpretation.)*

### GATE D: Results presented, not paraphrased

Summary tables shown in chat must also appear as markdown tables in `notebook.md`. Prose paraphrases of numbers lose precision and are unreviewable. This matters more under delegation: the subagent produces the tables, but the main thread must surface the *real numbers*, not the subagent's summary of them.

**Do not close the milestone if the Results section in `notebook.md` is prose where a table belongs.**

### GATE E: Researcher approval

Scope drift (decisions added mid-execution) slips past when there is no atomic gate between "I finished some work" and "I'm advancing." The decide phase presents state to the researcher; the researcher approves, requests a redo, or redirects.

**Do not make a milestone's `approved` commit without explicit researcher approval of the decide-gate state.** Iteration commits need no approval — they record work, they don't close it.

## Git discipline

### Per-analysis .gitignore

Created during scaffolding (at the start of the Plan phase). Default:
```
# Large intermediate data reproducible from KG
# (list specific files here, not blanket patterns)
__pycache__/
```
Everything else tracked by default. Explicit entries with a comment explaining why.

### Scaffolding

Claude creates the scaffold at the start of the Plan phase, before the brainstorming dialogue begins (see [artifacts.md — Scaffold creation](artifacts.md)), and commits it as the first iteration commit (`<slug> plan: iteration — scaffold`).

### Redo commits

Redo produces new commits — iterations, then a new approval commit — never amendments. The failed attempt's commits stay in history. Within the working tree, the milestone's `notebook.md` is overwritten to reflect the successful attempt.
