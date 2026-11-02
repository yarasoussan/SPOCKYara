# Methodology review — Plan→Run arc, first full dogfood

**Date:** 2026-08-06
**Subject analysis:** `analyses/2026-07-06-alteromonas_coculture_carbon_sources`
*(The subject analysis lives in the consumer clone where the dogfood ran, not in this template.)*
(Plan phase + all three Run milestones, closed 2026-07-26)
**Skill under review:** `.claude/skills/research-methodology` (+ `.claude/skills/critical-review`)
**Brief this answers:** [`docs/methodology-test-brief.md`](methodology-test-brief.md)

Evidence read: `proposal.md` (778 lines), `proposal_notebook.md`,
`proposal_critical_review.md`, the three milestone `notebook.md` files, all four
`critical_review.md` files, `gaps_and_friction.md`, `methodology_wins.md`,
`paper.md`, and the analysis's commit history — checked against the skill text
(`SKILL.md`, `references/step-protocol.md`, `references/research-notebook.md`,
`critical-review/SKILL.md`).

---

## 1. Watch-list verdicts

### 1. Did the enumerated `proposal.md` let you poke holes before anything ran? — **Yes, decisively**

Being forced to name a concrete approach, a statistics decision, and a named
validation set surfaced problems with no code written: the dual C+N ambiguity
(amino-acid/peptide uptake is also the nitrogen story), TCDB's ABC superfamily
lump (`3.A.1` carries no substrate signal), and the counting-unit trap
(transporter subunits co-move, so raw genes aren't independent).

The sharpest case is the `rank_up` catch (`gaps_and_friction.md`, 2026-07-07).
The scoring premise assumed `rank_up` was a genome-wide directional rank; a
`run_cypher` check showed it is populated on significant genes only (111 of 3947
edges in the primary experiment), and that the MCP tool renames the genome-wide
field `rank_by_effect` to `rank`. A genome-wide null over `rank_up` is not even
constructible. **The critic could falsify the stats plan against a live KG field
only because the plan named the field and the operation** — the single clearest
argument for enumeration.

### 2. Did the proposal critic catch what a vague plan would hide? — **Yes, and more than the skill anticipates**

Six passes across six Plan commits. Pass 2 found two Blockers (the `rank_up`
population above, plus an inverted extremum — "best (max) `rank_up`" selects the
*least*-up system, since rank 1 is most up). Pass 3 caught a degradation rung
that could fire on direction-blind metabolic potential. Pass 4 found a Blocker
**in machinery a previous critic pass had introduced** — a system-boundary rule
that fragmented ABC importers with two permeases, KG-verified against the
proposal's own worked example.

The dogfood's own lesson, recorded in `methodology_wins.md`, is that **each
material revision earns its own cold re-review** — and that later passes catch
what earlier passes' fixes introduced.

### 3. Coherent or cramped? — **Coherent**

Each researcher refinement built on a fact grounded earlier in the same thread.
Viability checks ("can we reconstruct transport systems?", "is TCDB specific
enough?") were two queries mid-conversation because grounding was already open.
KG grounding inside the Plan conversation also corrected the researcher's own
recollection of the dataset (one experiment → ten; proteomics is a starvation
time course, not a presence contrast) *at plan time* rather than mid-run.

### 4. Did delegation keep the main thread clean? — **Mostly yes; one failure**

The first subagent dispatch overflowed its context on a large enumeration result
and died without writing artifacts (`methods/notebook.md`, Context section); a
second dispatch that scripted results to disk via the package Python API
succeeded. After that the division held: the notebooks consistently distinguish
subagent output from main-thread verification ("verified against the KG
directly, not just the subagent CSV").

### 5. Did the main thread catch anomalies rather than trust summaries? — **Caught twice, missed once**

**Caught (methods):** the scorer's `assign_reference_class` used
`bool(row["in_candidate"])`; the real CSV stores that field as the string
`"False"`, and `bool("False")` is truthy — on real data every system would have
collapsed to `"candidate"`, destroying the reference-class structure the whole
null comparison depends on. All 27 unit tests passed, because the fixture used
Python booleans. Main-thread show-step verification re-ran the helper on a real
CSV string row and caught it.

**Missed (analysis):** the Fig F caveat cited L-lactate's coculture protein
percentile as 0.03; 0.03 is cation/acetate, and L-lactate's protein (0.58–0.89)
*agrees* with its RNA. The wrong number carried a wrong framing — "RNA and
protein disagree" instead of the true "proteomics is underpowered" (protein
median 0.82 ≥ RNA 0.76; 0 modules reach q<0.10). The **delta-critic** caught it,
not the main thread (`analysis/critical_review.md`, Delta review).

### 6. Any redo caused by a plan that looked fine but wasn't? — **No milestone redo**

Two proposal assumptions died on contact with data and were absorbed without a
reopen: `livKHMGF` — decision 7's worked example — is not annotated in HOT1A3 at
all (livH/M/G/F KOs absent), and single-gene systems turned out to be the *norm*
for HOT1A3 organic carbon (36 SBPs against 11 import permeases; 85 secondary
carriers), inverting the proposal's multi-subunit emphasis. Both were handled as
in-milestone re-anchoring plus a focus note added to the proposal's known
confounders. The methods milestone did rebuild its pipeline once (build → curate
→ classified v2 build), but inside the milestone and before its single commit, so
the no-mid-milestone-commits rule held.

---

## 2. Findings — where the skill text does not match what worked

Each finding is graded against Rule 9's own bar: one occurrence is a note,
process change needs the same friction twice.

### A. The methods critic should be automatic when the milestone emits data — **change now**

`step-protocol.md` GATE C makes the methods critic on-demand, on the premise that
computed results first appear at the analysis milestone. That premise is false
for KG work where the "method" includes constructing the entity set. The methods
milestone here emitted `parts_list_v2.csv` — substrate labels, confident/inferred
flags, reference classes — which every downstream score consumes.

Run on demand anyway, the critic found:
- a **Blocker**: `crr` / EIIA<sup>Glc</sup> (`ACZ81_07475`, `EZ55_01570`), a soluble
  cytoplasmic phosphocarrier, sat in the candidate set as a *confident* MFS-sugar
  importer — it would have scored as a confident sugar module;
- a `[KG]`-tagged count of **111** secondary carriers that is reproducibly **85**,
  already propagated into `paper.md`;
- three further label/confidence errors (`rpfN` porin mislabelled MFS-sugar,
  `peptide/nickel` at `confident`, the TonB reference-class narrative
  contradicting the scorer's own output).

*Bar:* cleared within this analysis (a Blocker **and** a propagated bad number in
the paper).

### C. The delta pass is the normal path, not an edge case — **change now**

`critical-review/SKILL.md` covers re-review on expansion in one paragraph. In
practice the expansion is routine: the analysis critic came back clean on data
integrity, then researcher-requested exploration (compound-class aggregation,
control scoring, figures D–H and E2) added new scripts and new claims during
decide. The delta pass over *only* that delta returned **1 Blocker, 2 Concerns,
2 Notes** — including the Fig F inversion in §1.5.

Since the explore phase runs *after* the critic by construction, a milestone that
explores should expect a delta pass.

*Bar:* cleared (two critic rounds in one milestone, the second finding a Blocker).

### F. TDD guidance needs a fixture-realism clause — **change now**

The `bool("False")` bug in §1.5 is not a one-off mistake but a class: a fixture
whose input *type* does not match the real artifact's serialization hides every
bug in the parsing layer, and a green suite reads as evidence of correctness. The
skill currently says to toy-test reusable utilities; it says nothing about the
fixture matching the real data's form, and nothing about spot-running on a real
row.

*Bar:* cleared (one bug, but it would have silently destroyed the analysis's
control structure, and the failure mode is generic).

### G. Friction logging decayed exactly when the run got heavy — **change now**

`gaps_and_friction.md` holds six entries, none dated later than 2026-07-23 —
nothing from the analysis or evaluation milestones. Yet the analysis milestone
produced a textbook methodology gap the framing didn't anticipate: EZ55's BH
family is only 3–5 modules, so its q<0.10 is a far weaker bar than HOT1A3's
46-module family (fucose p=0.017 clears q<0.10 in EZ55 but would give q≈0.7 in
HOT1A3). That was recorded as a critic disposition, never as friction.

Separately, `methods/notebook.md` cites `../gaps_and_friction.md` for the
subagent context-overflow death — **that entry was never written.** So a real
tooling friction is unlogged and the cross-reference dangles.

*Bar:* cleared (two instances: an unlogged methodology gap and an unlogged
tooling failure with a dangling pointer).

### B. "One commit for the Plan phase" is not what happens — **note, confirm next analysis**

Six Plan commits, six critic passes, and two of them landed *after* the commit
labelled "Plan phase APPROVED — Run phase open". The skill prescribes one commit
and implies one critic pass; neither survived contact. What the run actually
converged on is: the Plan phase closes when a cold pass comes back clean on the
current text, and each revision round may commit.

Related open question the skill does not answer: **when is the plan enough?**
`proposal.md` reached 778 lines and 13 locked decisions. The enumeration paid for
itself, but there is no stopping rule, and the two post-approval passes suggest
the phase can keep re-opening itself.

### D. Cross-experiment comparability belongs in the enumerated framing floor — **note, confirm next analysis**

The proposal met all four floor items and still locked "one FDR family per
(experiment × timepoint)" plus "no pooling; agreement by count across separate
results" without ever stating **how q's from families of different size compare**.
The entire conclusion rested on cross-experiment agreement. The gap was repaired
post hoc — by the analysis critic (Concern 2) and by the researcher-requested
compound-class aggregation, which is family-size-independent and became the lead
read. Candidate floor addition: *if the claim rests on agreement across
experiments, state what makes the metric comparable across them.*

### E. The validation set should include an expected-negative — **applied 2026-08-11** (a second occurrence in the re-run settled it)

The floor asks for genes whose behavior is known *if the method works*. The
sharpest instrument in this analysis was the opposite: the aromatic
expected-negative, something that should **not** come up. Its partial hit (benE,
the #2 module in the primary experiment at q=0.090) forced the honest reading —
aromatics appear in both strains but never as a coherent transporter+catabolism
unit, so "a partial complication, not cleanly falsified". That check exists
because the proposal happened to be good, not because the skill asks for it.

### H. "The methods milestone stays minimal" mischaracterizes KG work — **note**

`research-notebook.md` describes methods as an ad-hoc module implementing the
committed approach. Here it was a discovery milestone: 8 scripts, a 486-line
notebook, a genome-inventory reveal that inverted the proposal's counting unit,
and a logged decision that **supersedes proposal decision 7** (component role from
Pfam domains primary, KO confirming). This is the root cause of finding A — when
methods builds the entity set, it produces claims, not just code.

---

## 3. What held and should not be touched

- **The Plan→Run split and the enumerated framing.** Findings 1 and 2 are the
  strongest signal in the dogfood.
- **The critic chain.** Three Blockers across the arc (proposal pass 2, methods,
  analysis delta), none of which the author would plausibly have caught alone —
  the analysis critic explicitly verified the data-integrity half clean, so the
  Blockers were real and separable from noise.
- **Rule 9, plain language.** A grep of the banned interpretive vocabulary across
  `proposal.md`, `proposal_notebook.md`, `methods/notebook.md`, and
  `analysis/notebook.md` returns **zero hits** before the evaluation milestone.
- **GATE D, results tabled not paraphrased.** Every milestone notebook shows real
  markdown tables with real numbers.
- **Main thread owns `notebook.md`.** The judgment record stayed coherent and the
  interpretive corrections all landed in one place.
- **The "artifacts back, not conclusions" delegation rule.** It is what made the
  `bool("False")` catch possible.

---

## 4. Disposition

Applied to the skill on 2026-08-06: **A, C, F, G**; **E** followed on 2026-08-11 after
the re-run reproduced it (falsifiability check + pre-registered expected-negative
are now part of the framing floor).
Carried as watch items for the next analysis: **B, D, H** — re-check whether
each recurs before changing the skill text.
