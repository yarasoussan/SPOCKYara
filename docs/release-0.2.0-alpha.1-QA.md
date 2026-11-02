# Release QA — template 0.2.0-alpha.1

**Date:** 2026-09-23 · **Branch tested:** `release/0.2.0-alpha.1` (at `eca761e`)
· **Tested in:** the consumer clone `multiomics_analysis` (Windows 11, Git Bash)

| | Version |
|---|---|
| Template | 0.2.0-alpha.1 |
| Explorer | v0.1.0-alpha.5 (`2f7a138`) |
| KG | 0.1.0-alpha.7, built 2026-09-22, role `production`, 127,035 genes / 209 experiments / 49 papers / 48 organisms |

**Verdict: green**, with the two fixes below applied on the release branch.

## How it was tested

The release branch was merged into a working consumer clone on a throwaway
branch (`test/release-0.2.0-alpha.1`), so the check covers the real upgrade path
— a researcher with finished analyses pulling the new template — not only a
fresh clone.

1. **Merge.** The release was compared to the clone's own methodology edits, then
   merged. The release contains every one of them (including the falsifiability
   check); conflicts were all "both sides edited", resolved to the release
   version. The clone's own analyses, dashboard and docs were untouched.
2. **`uv sync`** to explorer v0.1.0-alpha.5.
3. **`./scripts/preflight.sh`**.
4. **MCP server, driven directly over stdio** (a `fastmcp` client, outside
   Claude Code): list tools, compare to the allow-list, call a few tools, list
   docs resources. Then again from inside a Claude Code session after
   reconnecting the server.
5. **Skill and doc integrity:** every relative link and `#anchor` in
   `.claude/skills/**`, `CLAUDE.md`, `README.md`, `analyses/README.md` and
   `docs/` resolved; searched for leftover version strings and old step names.
6. **Usage hook:** fed a sample PostToolUse event to `hooks/log-mcp-usage.sh`.
7. **Existing analysis against the new KG:** on a scratch copy of the
   carbon-sources analysis (the dogfood behind this release), ran its toy-test
   suite and re-ran all 12 scripts that query the KG, with deprecation warnings
   on, then compared every output CSV with the committed one.

## Results

| Check | Result |
|---|---|
| Merge into a consumer clone | Pass |
| `uv sync` | Pass (see note on Windows file locks) |
| Preflight | **Green** — version triple printed, contract ok, API smoke matched 2 known loci |
| MCP server | Pass — 42 tools, `kg_release_info` verdict `ok` (17/17 schema asserts), 116 docs resources, `gene_overview` and the new `ontology_term_details` return data |
| Allow-list vs served tools | **Fail → fixed:** `ontology_term_details` was not pre-approved |
| Skill / doc links and anchors | Pass — 0 broken |
| Usage hook | Pass where `jq` is installed; skips silently without it (by design) |
| Toy tests (27) | Pass |
| KG scripts re-run (12) | 11 ran, 1 crashed; many outputs differ from the committed ones — all traced to KG content changes, none to the template or explorer API (next section) |
| Deprecation warnings from the Python API renames | None hit by the existing scripts |

## Findings

### Fixed in this release

1. **`ontology_term_details` missing from the pre-approved tools.** The explorer
   adds this tool; `.claude/settings.json` did not list it, so every call would
   raise a permission prompt — contradicting the template's promise that all
   read-only KG tools are pre-approved. Added to the allow-list.

2. **Re-running an older analysis silently gives different numbers.** Nothing in
   the changelog warned about this. Re-running the carbon-sources scripts on KG
   0.1.0-alpha.7 found three changes, all KG content, none raising an error
   except where a downstream step got an empty list:

   | Change | Evidence | What to do |
   |---|---|---|
   | TCDB now includes weak homology calls | Default `genes_by_ontology(ontology="tcdb")` for HOT1A3: **427 → 1,139 genes**. Added calls are low identity (median 32%, min 20.6%; 767 genes at tier 3) and include LysR regulators, sensor kinases, rhodanese. The transporter parts list grew 694 → 1,270. | Use a trust filter: `max_tier=2` → 435 genes; `min_evidence_score=0.6` → 389 |
   | TCDB attachment level and naming changed | Genes that used to report `term_name` = `3.A.1.10` now report "The Ferric Iron Uptake Transporter (FeT) Family". A script matching TC numbers in `term_name` found 0 seed genes and crashed (`locus_tags must not be empty`). | Read the TC number from `term_id` |
   | An experiment gained timepoints under the same ID | `…_coculture_prochlorococcus_med4_hot1a3_rnaseq` now has days 11, 18, 31 (was day 11 only). Day-11 values are identical (3,947 genes, max log2FC difference 3e-9). A script without a `timepoint` filter pulled 11,841 rows instead of 3,947. | Filter on `timepoint` explicitly |

   Added to the 0.2.0-alpha.1 changelog entry as a "re-running an older analysis"
   note.

### Not template issues — passed on

**To the KG:**
- `tcdb:3.A.1` (the ABC Superfamily) has `superfamily` = "ArsA ATPase (ArsA)
  Superfamily" — looks like a mapping error.
- `tcdb:3.A.1.129` has no descriptive name (name = `3.A.1.129`) while its
  siblings do.
- `kg_release_info` returns an empty `release_notes_url` and null
  `release_highlights` / `breaking_changes`. The three data changes above are
  exactly what those fields are for; with them empty, a researcher cannot find
  out why a re-run changed.

**To the environment / setup docs:**
- **Usage logging is silently off without `jq`.** The tester machine had no `jq`
  on the Git Bash PATH; the hook exits 0 and logs nothing, and nothing had been
  logged since 2026-07-26. Suggest preflight warn when `jq` is missing, since
  usage logs are a stated goal of the template.
- **`uv sync` fails on Windows while the MCP server is running** (`failed to
  remove … multiomics-kg-mcp.exe … used by another process`). Stop the server
  (or close Claude Code) before syncing, then reconnect with `/mcp`. Worth a line
  in the README's update instructions.

## Reproduce

```bash
# in a consumer clone with the template as `upstream`
git fetch upstream
git checkout -b test/release-0.2.0-alpha.1
git merge upstream/release/0.2.0-alpha.1
uv sync                     # stop the MCP server first on Windows
./scripts/preflight.sh
```

For the re-run comparison, copy an analysis folder to a scratch directory,
export the KG credentials from `.env` (scripts run outside the repo root do not
find it), run each KG script from its own folder, and `cmp` each `data/*.csv`
against the committed copy.
