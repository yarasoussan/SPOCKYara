# Anti-hallucination patterns

Concrete failure modes observed in LLM-driven omics analysis and
how to prevent them. Each pattern includes a real or realistic
example from this KG.

## Contents

1. [Gene identity errors](#category-1-gene-identity-errors) — paralog conflation, ortholog conflation, inventing functions
2. [Narrative fabrication](#category-2-narrative-fabrication) — causal claims, cherry-picking, selective reporting, language strength, cross-experiment aggregation, emotive vocabulary, speculative proposals
3. [Data handling errors](#category-3-data-handling-errors) — counting from truncated lists, cross-study p-values, fabricating statistics, direction-sign absent
4. [Knowledge boundary violations](#category-4-knowledge-boundary-violations) — asserting absence, assuming completeness, unsupported literature claims, measurement failure vs biological absence
5. [Source-of-truth verification failures](#category-5-source-of-truth-verification-failures) — tool capabilities from memory, publication attribution from memory, field semantics from memory
6. [Quick self-check](#quick-self-check) — 8-question checklist before presenting findings

---

## Category 1: Gene identity errors

These are the most dangerous because they produce plausible but
wrong biological conclusions.

### 1.1 Paralog conflation

**What happens:** Multiple locus tags share a gene name. The LLM
groups them as "the same gene" and merges their expression data
into a single narrative.

**Real example (catalase analysis):** "katA is downregulated by
starvation (log2FC -7.8) then partially recovers at day 89
(log2FC +1.8)." Wrong — the downregulation is ACZ81_02025, the
"recovery" is ACZ81_11985. Different genes, opposite behaviors,
same name.

**Prevention:** See [Gene identity — Paralog handling](gene-identity.md#paralog-handling).

### 1.2 Ortholog cluster conflation

**What happens:** Genes in the same ortholog cluster are treated
as interchangeable. "katB" in one strain is reported using data
from "katE" in another strain because they share a cluster.

**Real example:** MIT1002_02513 (katE) and MIT1002_03530 (katB)
are both in cluster 4644E. The analysis reported katE expression
values as "katB" because the cluster matched.

**Prevention:** See [Gene identity — Ortholog cluster rules](gene-identity.md#ortholog-cluster-rules).

### 1.3 Inventing gene functions

**What happens:** The LLM knows from training data that "gene X
is involved in pathway Y" and states this without querying the KG.
The KG may have different or no annotation for that gene.

**Prevention:**
- Gene function claims must come from `gene_overview`,
  `gene_ontology_terms`, or `genes_by_function` output
- Prefix intrinsic knowledge with: "Based on general knowledge
  (not from this KG)..."
- If the KG annotation disagrees with intrinsic knowledge, report
  the KG annotation and note the discrepancy

---

## Category 2: Narrative fabrication

The LLM constructs a coherent biological story that goes beyond
what the data supports.

### 2.1 Causal claims from correlational data

**What happens:** Expression data shows co-regulation. The LLM
writes "gene X regulates gene Y" or "condition A causes pathway B
to activate."

**Prevention:**
- Differential expression shows *association*, not causation
- Use language: "co-regulated", "correlated", "respond similarly"
- Reserve causal language for claims backed by specific evidence
  (which this KG does not contain — no ChIP-seq, no knockouts)

### 2.2 Cherry-picking from truncated results

**What happens:** MCP returns 50 rows (limit). The LLM reports
"the top 5 genes are..." without noting that 750 other genes
were not examined. Or worse: "gene X is NOT differentially
expressed" when it was simply outside the returned rows.

**Prevention:**
- Always check `truncated` and `total_matching` in MCP output
- Never infer absence from a truncated result set
- When summarizing: "Of {total_matching} significant genes, the
  top {n} by |log2FC| are..."
- For absence claims: must use a non-truncated result or a
  specific query for that gene

### 2.3 Selective reporting of duplicate entries

**What happens:** The KG has two entries for the same gene in the
same condition (different contrasts from the original DESeq2
analysis). The LLM reports only the significant one.

**Real example:** katG (ACZ81_16125) at day 89 in coculture has
two entries: +1.26 (padj 3e-4) and -1.16 (padj 0.29). Only the
significant one was reported.

**Prevention:**
- When multiple entries exist for the same gene/condition, report
  all of them
- Note that they likely represent different statistical contrasts
- If you cannot determine which contrast is relevant, flag the
  ambiguity rather than choosing one

### 2.4 Strength of language vs strength of evidence

**What happens:** The LLM uses confident language for weak evidence.
"katB is significantly downregulated" when padj = 0.050.
"Consistent with ROS detoxification" when there are no p-values.

**Prevention:** See [Statistical rigor — Strength of language](statistical-rigor.md#strength-of-language-vs-strength-of-evidence). Match language to evidence level; never use confident language for weak or absent statistics.

### 2.5 Cross-experiment aggregation without caveats

**What happens:** Expression data from different platforms
(microarray, RNA-seq) or different statistical tests (Goldenspike,
Rockhopper, DESeq2) are compared as if they are directly
comparable. "Gene X has log2FC 3.2 in study A and 1.1 in study B,
so the response is stronger in A."

**Real example (nitrogen stress analysis):** Tolonen 2006
(microarray, Goldenspike) and Read 2017 (RNA-seq, Rockhopper)
fold changes for the same genes were compared. Different platforms
have different dynamic ranges — a log2FC of 3 on microarray is
not the same as log2FC 3 on RNA-seq.

**Prevention:** See [Statistical rigor — Cross-experiment comparison](statistical-rigor.md#cross-experiment-comparison-caveats). Compare direction and rank, not magnitude, across platforms.

### 2.6 Emotive vocabulary and speculative proposals

Two related failure modes. Both reach for elaborate language or
elaborate fixes when the data hasn't earned them yet.

**(a) Emotive vocabulary before the evaluation milestone.** Describing a data observation
with words like "striking", "massive", "biologically loaded",
"biologically explosive", "central finding", "reframes the analysis"
before the formal analysis has run. The vocabulary commits to a
conclusion the analysis hasn't tested.

**Real example (discordance analysis, step 2 close):** Before any
discordance metric had been computed, the step-2 narrative described
a 5-marker heatmap as "biologically loaded", "massive finding",
"biologically explosive", and claimed the data "reframes the
analysis with a strongly motivated default hypothesis." The arc
puts hypothesis testing at the analysis milestone and caveat
harvesting at the evaluation milestone — enthusiasm while still
enumerating the KG entries biases later analysis.

**(b) Anchor-on-loud-cells then narrate wrong.** Reading a heatmap
or summary table by eye, fixating on the strongest-color cells,
and writing a generalization ("all", "systematically", "primarily")
without checking the underlying data file.

**Real example (stress-axis analysis, step 3):** Step 3 control
heatmap was described as "All 5 N-stress positives are clearly UP
across both omics in both conditions." The data file showed
coculture-RNA values systematically negative (log2FC −1 to −2.6)
at all 4 timepoints. The narrative anchored on the strongest cells
(axenic-protein death-phase) and missed the muted pattern. Caught
at step 5 by a quantitative score, not at step 3.

**(c) Speculative proposals.** Listing methodology improvements,
KG-side fixes, or process changes that aren't anchored to specific
data or recurring friction. The proposals sound systematic but are
extrapolations from a single nudge or single incident.

**Real example (stress-axis analysis, retrospective):** A retrospective
listed 7 methodology improvements after one analysis, including
process changes ("adopt `uv run` as default", "add a retrospective
sub-protocol") that came from a single nudge or a single occurrence
— not a pattern. Process change needs the same friction across two
analyses; one occurrence is a note, not a directive.

**Prevention:**
- Before the evaluation milestone, write factual statements: numbers,
  directions, conditions. Drop vocabulary like "massive", "striking", "explosive",
  "central", "reframes", "rich", "hand-wavy" used as praise.
- Interpretation, where present, goes inline with `[interpretation]`,
  and lists competing alternatives.
- Words like "all", "every", "no", "systematically", "primarily"
  require a query against the data file, not a heatmap glance. If
  you write "all 5 are UP", check all 5 in the data first.
- For methodology / KG / tooling proposals: point to the specific
  friction (date, location, what failed). One occurrence is a note;
  process change needs the same friction in two analyses.
- Reserve interpretive vocabulary and bold proposals for the evaluation milestone,
  where the framing has been tested.

---

## Category 3: Data handling errors

### 3.1 Counting from truncated lists

**What happens:** `len(results)` used instead of `total_matching`.
"There are 50 genes responding to nitrogen stress" when there are
actually 823.

**Prevention:**
- Counts come from summary fields (`total_matching`,
  `total_entries`), never from `len(results)`
- If you need to count subcategories not in summary fields,
  extract full data first

### 3.2 Cross-study p-value comparison

**What happens:** "katA is more significantly affected by
starvation (padj 2e-11) than by coculture (padj 0.015)."
These p-values come from different studies with different designs,
sample sizes, and statistical power. They are not comparable.

**Prevention:**
- P-values are within-study measures — never compare across studies
- Compare effect sizes (log2FC) across studies if needed, but note
  the caveat
- For cross-study claims, use direction and rough magnitude, not
  precise p-value ranking

### 3.3 Fabricating summary statistics

**What happens:** The LLM computes a mean or percentage from
incomplete data in context and presents it as a finding.
"On average, catalase genes are downregulated 6.2-fold under
starvation" — computed from whatever rows were visible.

**Prevention:**
- Summary statistics must be computed in scripts over complete
  data, not eyeballed from MCP output
- If you report a summary statistic, cite the script that
  computed it
- For quick estimates in chat, explicitly say "rough estimate
  from the top N results" and never present as a finding

### 3.4 Direction claims from a table whose sign may be absent

**What happens:** An experiment is compared or summarized by direction
(up/down) without checking that the underlying `log2_fold_change` sign is
actually present. Some experiments report only one direction — or have the
sign stripped at ingestion (stored as `|log2FC|`) — so every gene reads "up."
A direction claim built on such a table is an artefact, not biology, and
`table_scope` does not protect you: a table tagged `all_detected_genes` can
still be all-positive.

**Real example (Alteromonas coculture analysis):** four experiments from two
2016 papers showed `significant_down = 0` with `table_scope =
all_detected_genes`. Counting the sign of `log2_fold_change` over *all* stored
edges (significant and not) found **0% negative across 740–2295 genes** — the
sign was gone. An earlier pass had claimed "motility direction flips by
partner" partly from these; the flip was unreadable from the corrupted data.
(The real, partner-specific direction difference only showed up later, between
*sign-verified* contrasts.)

**Prevention:**
- Before trusting or comparing **direction**, check the log2FC **sign
  distribution over all genes**, not the rollup counts. `0% negative across
  many genes (incl. non-significant)` = sign lost → unusable for direction.
- `significant_down = 0` alone is not the tell — a real experiment can have no
  significant down genes while its log2FC values still carry both signs (e.g.
  sparse proteomics). The diagnostic is the **all-gene sign distribution**.
- A genuine all-genes DE table is roughly symmetric (~40–55% negative). Far from
  that across thousands of genes is a data-integrity flag — report it (and the
  experiment) rather than building on it.

---

## Category 4: Knowledge boundary violations

### 4.1 Asserting absence

**What happens:** "Prochlorococcus does not have catalase genes."
True in this KG, but the LLM may state it as a universal fact
when it's a property of the KG's gene set.

**Prevention:**
- "No catalase genes are annotated in the KG for Prochlorococcus"
- Not: "Prochlorococcus lacks catalase"
- The KG reflects what was annotated and loaded — absence in the
  KG does not prove biological absence (though in this case the
  biological absence is well-established, that knowledge comes
  from training data, not the KG)

See also [4.4 Measurement failure vs biological absence](#44-measurement-failure-vs-biological-absence) for the related case of missing measurements (vs missing annotations).

### 4.2 Assuming KG completeness

**What happens:** "All nitrogen-responsive genes in MED4 are..."
when the KG only contains results from specific experiments under
specific conditions.

**Prevention:**
- Qualify scope: "In experiment X, N genes were differentially
  expressed under nitrogen limitation"
- Not: "MED4 has N nitrogen-responsive genes"
- Always anchor claims to specific experiments and conditions

### 4.3 Literature claims without KG support

**What happens:** The LLM knows from training data that "gene X
has been shown to [function] in [organism] (Smith et al. 2020)"
but this publication is not in the KG and the claim cannot be
verified from the data.

**Prevention:**
- Clearly separate KG-derived findings from literature context
- Use a distinct format: "**From the KG:** ... **From the
  literature (not verified in this KG):** ..."
- If the user needs literature support, say so — this system is
  a KG explorer, not a literature review tool
- Never cite a specific paper from intrinsic knowledge as if
  it were a KG reference

### 4.4 Measurement failure vs biological absence

Related to [4.1 Asserting absence](#41-asserting-absence) — that one is about KG annotation; this one is about missing measurements.

**What happens:** Data is missing for one omics layer (or condition,
or timepoint) and present for another. The LLM treats the missing
data as evidence of *biological* absence — "mRNA is gone", "the
protein is not expressed", "the gene is silenced" — when the
absence is technical, not biological.

**Real example (discordance analysis, step 1):** Sketched a
sub-question "protein persists while mRNA is gone" for MED4 axenic
d31 / d89 proteome-only data. The missing RNA-seq was an extraction
failure (cell death, RNA degradation, biomass below extraction
threshold) — not biological absence of mRNA. Treating it as "mRNA
gone" would have produced a false post-transcriptional-persistence
claim.

**Common reasons data is missing without being biologically zero:**
- Extraction failure (RNA degradation, low biomass, technical)
- Detection limit (dynamic range of the assay)
- Sample loss or processing error
- Sequencing or MS depth insufficient for low-abundance species
- Multi-mapper filtering (genome-redundant paralogs dropped)
- Different platforms cover different gene sets by design

**Prevention:**
- Before claiming biological absence from missing data, ask: was
  this gene / sample / timepoint actually measured? Check the
  experiment design and the upstream pipeline.
- Treat missing data as missing data — no information — not as
  zero or "below biological detection."
- If you must use the data despite the gap, explicitly handle it
  as missing-not-at-random and flag the assumption.
- Language: "no protein detected" (not "protein absent"), "no
  RNA-seq data" (not "mRNA gone"), "below detection limit" (not
  "not expressed").

---

## Category 5: Source-of-truth verification failures

Claims made from training knowledge or prior-session memory without re-reading the current schema, API, or metadata. These are the hardest to catch because the claim *feels* confident — it's based on something real that existed somewhere — but the specific detail may be wrong for this KG, this tool version, or this field's semantics.

### 5.1 MCP tool capability from memory

**What happens:** Asserting what parameters an MCP tool accepts, what it returns, or what filters it supports, based on a remembered tool signature. Tool schemas evolve; memory of "what the tool could do" drifts.

**Real example (N-limitation analysis):** "`pathway_enrichment` accepts only `ontology` + `level`, no `term_ids` filter." The current schema supports `term_ids` for DAG ontologies. The false claim blocked a whole line of analysis that would have worked.

**Prevention:**
- Before asserting what any MCP tool accepts or returns, re-load the current schema: run `ToolSearch select:<tool_name>`, or read the authoritative per-tool doc the MCP serves at `docs://tools/{tool_name}`
- For cross-tool semantics — `not_found` vs `not_matched`, `truncated`/`total_matching`, `not_known`/tested-absent rows, exclude-wins-on-overlap — consult `docs://guide/conventions` rather than reasoning from a field name
- Do not rely on memory of tool signatures from earlier in the session or orientation — schemas change and memory drifts
- If a tool call fails, check the schema before concluding the capability is missing

### 5.2 Publication attribution from training knowledge

**What happens:** Naming authors or papers from intrinsic knowledge — recognizing that "this experiment sounds like X's work" — without calling the KG publications API. The attribution may be confidently wrong.

**Real example (N-limitation analysis):** NC1 was attributed to "Hennon" (a real coculture researcher) based on how the experiment was described. The actual paper was Aharonovich & Sher 2016 — different group, different strain, different biology.

**Prevention:**
- Before naming an author, title, or citation associated with an experiment, run `list_publications` (with the relevant `experiment_id` or filter)
- Cite by KG-resolved DOI or experiment ID; use author-year labels only for what `list_publications` returned
- If two experiments "sound similar," that's a signal to verify, not to infer

### 5.3 Field semantics from memory — cumulative vs per-timepoint counts

**What happens:** Using a top-level summary field as if it were per-timepoint or per-condition because the field name sounds unambiguous. Example: `list_experiments` returns a top-level `gene_count` that is cumulative across timepoints (= sum of per-TP row counts); per-TP counts live in `timepoints[].gene_count`, and the distinct-gene denominator is the top-level `distinct_gene_count`. Using cumulative `gene_count` as if it were either distorts detection-power expectations and pathway background sizes.

**Real example (N-limitation analysis):** Tolonen 2006 was reported as having "10,182 genes" — ~6× the actual MED4 ORFome. The number was cumulative across timepoints, not per-TP.

**Prevention:**
- For per-TP detection power use `timepoints[].gene_count`; for pathway background size or cluster Fisher 2×2 dimensions use the top-level `distinct_gene_count` (distinct genes measured across the experiment). Never use cumulative top-level `gene_count` for either.
- When pulling a numeric field from any tool response, check the field's docstring or schema description before using it in a summary
- For anything that sounds "obvious" (counts, totals, sizes), verify the unit and scope against the schema

---

## Quick self-check

Before presenting any finding, ask:

1. **Where did this number come from?** → Must name a tool call
   or script output
2. **Am I using a gene name or a locus tag?** → Must be locus tag
3. **Is this from complete data or truncated?** → Check `truncated`
4. **Am I comparing across studies?** → Compare direction and rank; compare
   magnitude only within one platform and study; never p-values
4b. **Am I claiming a direction (up/down)?** → Confirm the log2FC sign is
   present — check the all-gene sign distribution, not just rollup counts
5. **Am I claiming absence?** → Qualify with "in the KG" / "in
   this experiment"
6. **Is this KG data or my training knowledge?** → Label which is
   which
7. **Would a different paralog assignment change this conclusion?**
   → If yes, verify the assignment
8. **Am I claiming tool capabilities, citations, or field semantics
   from memory?** → Verify against current schema (`ToolSearch`),
   `list_publications`, or field descriptions before asserting
