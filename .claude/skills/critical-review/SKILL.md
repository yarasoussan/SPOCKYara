---
name: critical-review
description: Use before the researcher sees a claim-bearing artifact of a research analysis — the proposal at the close of the Plan phase (and again after the design review changes it), the analysis and evaluation milestones at their decide phase, the methods milestone when it emits a data artifact, and any milestone whose claims expanded after its earlier pass — plus on demand at any point. Dispatches a fresh-context critic that re-checks the artifact's own claims against its own files. The proposal gets interpretation only; the analysis and data-emitting methods milestones get data-integrity + interpretation; the evaluation milestone gets interpretation only. The critic reviews only that artifact's files; earlier phases are trusted inputs, not re-audited.
---

# Critical review

Dispatch a fresh-context critic to challenge a research milestone **before** it is
presented at the decide gate. The critic never sees your session history — it
reads the milestone's artifacts cold, so it cannot inherit the narrative you
anchored on while doing the work. That detachment is the point: the failure modes
the methodology keeps hitting (a heatmap narrated "all 5 are UP" when the data
file says otherwise; a difference-of-trajectories narrated as "coculture vs
axenic" when each arm is starvation-vs-its-own-baseline) survive precisely because
the author is committed to the story. A reviewer reading only the data files is
not.

This does not replace the researcher's decide-gate approval — it sharpens it.
The critic's findings, where any exist, become part of the state you present.

## Keep it light — three rules that bound the cost

1. **Match the lens to what the milestone produces.** Don't run every dimension on
   every milestone.
2. **Review only this milestone's own files.** The proposal and earlier milestones
   already passed their own review — treat their outputs as trusted inputs, not as
   things to re-audit.
3. **Write an artifact only when there are findings.** A clean milestone gets one
   line in `notebook.md`, not a file.

## When it runs, and with which lens

**Proposal (automatic; interpretation only).** The proposal is the
highest-leverage artifact — a flaw in the framing propagates through all three
Run milestones and is the most expensive to unwind — so it is reviewed before the
Run phase begins. Its lens is **interpretation only**: there is no data yet, so
there is nothing to integrity-check; the critic weighs the framing's testability,
controls, confounders, and whether the statistics decision, validation set, and
falsifiability check / expected-negative fit the question. Invoke it especially when the framing rests on a judgment call that
is not self-evidently sound: a **non-obvious combining key** (e.g. mapping
disjoint strains onto shared ortholog groups), a **derived or constructed
comparison**, or **controls whose validity is not obvious** (is the positive
control really independent? is the negative control the contrast it is labelled
as?). The proposal review sits alongside the author's own self-review and the
researcher's approval of `proposal.md` — see [step-protocol.md — The Plan phase](../research-methodology/references/step-protocol.md).

**Analysis milestone (automatic; the one heavy gate).** This is where computed
results first appear, so it gets the full pass: **data-integrity + interpretation**.
The data-integrity half is what pays off here — it opens the CSVs and checks the
signs, counts, truncation, and conflation that the narrative glosses.

**Methods milestone (automatic when it emits a data artifact; otherwise on
demand).** A methods milestone whose only output is a toy-tested function can
wait for the analysis pass. But when the method includes **constructing the
entity set** — a parts list, a curated candidate set, a classification table —
that file carries claims (substrate labels, confidence flags, class assignments)
and every downstream score inherits them. Then it gets the full
**data-integrity + interpretation** lens, on the same footing as the analysis
milestone. Do not skip it because the milestone is labelled "methods": the errors
this catches are exactly the ones no later pass will, because later milestones
read the parts list as a *trusted input*.

**Delta pass (expected, not exceptional).** A critic pass is point-in-time, and
the **explore** phase runs *after* it by construction — the researcher asks for
follow-on analyses, and new scripts, figures and conclusions land during decide.
**If a milestone's claims materially expand after its pass, re-run the critic
over the delta before closing.** **The proposal gets delta passes too:** the Plan
phase closes on a design review with the researcher, which usually changes the
framing after the proposal critic ran — re-run it over the changed sections, with
the earlier proposal as a trusted input. *(N-import coculture: two Plan-phase
delta passes, about 70k tokens each, found one Blocker and five Concerns in the
additions.)* Tell the re-dispatch which prior files are
already-reviewed (list them as trusted inputs) so it reviews only the new work,
not the whole milestone again. Treat a milestone that explored after its pass and
closed without a delta pass as having closed unreviewed work — the clean first
verdict does not cover what came after it.

**Evaluation milestone (automatic; light).** Evaluation produces conclusions, not
new computation, so a data-integrity sweep has little to bite. Run **interpretation
only**: is each conclusion earned by the analysis milestone's results? are caveats
honest? is anything over-claimed, causal-from-correlational, or compared across
platforms? Evaluation reads the analysis milestone's outputs as **trusted
evidence** — it judges whether the conclusions follow from them; it does not
re-open those files hunting for new data defects (the analysis review already did
that).

**Any point, on demand.** A methods milestone that emits no data but rests on a
non-obvious choice, or a redo you want re-checked, can be reviewed at will.

**Not run by a subagent:** routine **methodology compliance** (locus tags present,
computations in scripts, results tabled not paraphrased, decide-gate checklist
populated). These are mechanical self-checks — they belong in the author's
decide-gate checklist ([step-protocol.md](../research-methodology/references/step-protocol.md)),
not a fresh-context dispatch.

## How to dispatch

**1. Identify the folder under review and the analysis root** (e.g.
`analyses/<name>/analysis/` under `analyses/<name>/`; for a framing review, the
proposal files at the analysis root).

**2. Dispatch the `critic` agent** (`.claude/agents/critic.md` — it cannot edit
files; fall back to a `general-purpose` subagent if it isn't available), filling
the template at [critical-reviewer.md](critical-reviewer.md). Dispatch a fresh
critic for every pass, delta passes included — never continue an earlier one; a
critic that remembers the last pass is no longer reading cold.

Placeholders:
- `{ANALYSIS_ROOT}` — path to the analysis directory
- `{REVIEW_FOLDER}` — path to the folder under review (the **only** files in review
  scope); for a framing review, `proposal.md` at the analysis root
- `{REVIEW_NAME}` — what is under review (e.g. "the analysis milestone")
- `{REVIEW_INTENT}` — one or two plain-language sentences on what this milestone set
  out to do and the main judgment calls it made (the co-define agreement, or the
  proposal's framing)
- `{REVIEW_LENS}` — which dimensions to apply: `interpretation only` for the
  proposal and the evaluation milestone; `data-integrity + interpretation` for the
  analysis milestone and for a methods milestone that emitted a data artifact; for
  other on-demand runs, choose by what was produced (data files → include
  data-integrity; conclusions only → interpretation only)
- `{TRUSTED_INPUTS}` — prior output files this artifact builds on, which the critic
  reads as evidence but does **not** re-audit (e.g. the analysis milestone's data/
  for an evaluation review; the methods milestone's data artifact for an analysis
  review). Empty for the proposal, and for an analysis milestone whose methods
  milestone emitted no data file.

**3. Handle the result by what it found:**
- **Findings exist** → write the critic's findings verbatim to a
  `critical_review.md` in the review folder (for the proposal, whose files sit at
  the analysis root, use `proposal_critical_review.md`), each with your
  **disposition**: fixed (what changed), disputed (why the critic is wrong, with
  the file-and-number that proves it), or deferred (why it can wait). Commit it
  with the phase.
- **Clean** → no file. Add one line to the milestone's `notebook.md` (or
  `proposal_notebook.md` for the proposal):
  `Critical review: clean (data-integrity + interpretation)` or `(interpretation)`
  — so the clean verdict sits with the decide-gate checklist, not floating elsewhere.

**4. Act before presenting:**
- **Blocker** — must be resolved (fixed or disputed with a specific data
  citation, not "I'm confident") before the milestone closes.
- **Concern** — address or explicitly defer with a reason.
- **Note** — record; fix if cheap.
- **Push back when the critic is wrong.** It read the artifacts cold and may have
  missed context — but disputing requires a file-and-number, not confidence.

**5. Present to the researcher** alongside the decide-gate state: the
`critical_review.md` with your dispositions (or the one-line clean note).

## What the critic is told NOT to do

- **Not to review anything outside `{REVIEW_FOLDER}`.** Trusted inputs are read for
  evidence, never re-audited.
- **Not to redo the analysis.** It spot-checks the milestone's claims against the
  milestone's files; it does not re-run the method.
- **Not to manufacture findings.** Every finding cites a specific file, the
  literal column name, and the number. "Unverified — check X" beats a confident
  guess. A clean dimension is a valid verdict.
- **Not to rewrite anything.** It reports; the author dispositions.

## Red flags

**Never:**
- Skip the proposal review because "the plan is obvious," the analysis-milestone
  review because "the result is obvious," or a data-emitting methods review
  because "methods is only code."
- Close a milestone that grew after its critic pass without a delta pass over the
  new work.
- Start the Run phase, or close a milestone, with an unresolved Blocker.
- Re-audit an already-reviewed proposal or earlier milestone as part of a later
  milestone's review.
- Let the critic's confidence substitute for the data — a refutation without a
  file-and-number citation is itself a finding to dispute.

See the template at [critical-reviewer.md](critical-reviewer.md).
