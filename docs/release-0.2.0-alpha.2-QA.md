# Release QA — template 0.2.0-alpha.2 (Spock)

**Date:** 2026-11-01 · **Branch tested:** `release/0.2.0-alpha.2` · **Tested in:**
the consumer clone `multiomics_analysis`, merged on a throwaway branch in a
separate worktree (Windows 11, Git Bash)

| | Version |
|---|---|
| Template | 0.2.0-alpha.2 |
| Explorer | v0.1.0-alpha.6 (`7ec6190`) |
| KG | 0.1.0-alpha.8, role `production` |
| Python / pandas | 3.12.11 / 3.0.3 |

**Verdict: green**, with the fixes below applied on the release branch.

## How it was tested

1. **Merge** the release into a clone with eleven finished analyses, on a
   throwaway branch in its own worktree, so the clone itself was untouched.
2. **`uv sync`**, then **`./scripts/preflight.sh`**.
3. **MCP server over stdio** (a `fastmcp` client, launched as Claude Code
   launches it): list tools, `kg_release_info`, `gene_overview`, list docs.
4. **Allow-list vs served tools.**
5. **Usage hook** fed sample events: object, array and non-JSON responses, a
   failure event, and `false` / `0` values.
6. **Scripts:** `build_report_index.py` and `build_paper.py` on a toy analysis
   (titled and untitled pages, an extra folder, PNG + SVG figures, a table, a
   missing figure).
7. **Existing analyses against the new stack:** both toy-test suites; every
   KG-querying script of the N-import coculture analysis, compared with the
   committed outputs.
8. **Platform packages:** every locked dependency checked for prebuilt
   packages on Windows, Intel Mac, Apple Silicon Mac and Linux.
9. **Skill integrity:** relative links and anchors; a cold read of the skills by
   a fresh agent walking three scenarios (Plan close, discovery methods
   milestone, evaluation decide).

## Results

| Check | Result |
|---|---|
| Merge into a consumer clone | **Conflict → documented.** `pyproject.toml` / `uv.lock` conflict when the clone added a package (here `plotly`). Resolution: keep both dependency lists, regenerate the lock. The recipe is now in the README |
| `uv sync`, preflight | **Green**: version triple printed, contract ok, API smoke matched 2 known loci |
| MCP server | Pass: 42 tools, `kg_release_info` verdict `ok`, `gene_overview` returns data, 117 docs resources |
| Allow-list vs served tools | Pass: 42 = 42, nothing missing or stale |
| Usage hook | **Fail → fixed.** `truncated: false` was logged as `null`; an array response crashed the hook; Windows `jq` wrote CRLF |
| Preflight under alpha.6 | **Fail → fixed.** `kg_release_info(conn)` → `kg_release_info(conn=conn)` (keyword-only) |
| Report index / paper builders | Pass |
| Platform packages | **Fail → fixed.** biopython 1.88 has no Intel-Mac package (capped `<1.87`); Python pinned to 3.12 so every package has a prebuilt build |
| `upsetplot` | **Dropped.** It crashes on its first plot under pandas 3 |
| Toy tests | Pass: 254 (+4 skipped, archive data absent) and 27 |
| `pytest` in the venv | **Fail → fixed.** It was not a dependency, so `python -m pytest` failed in a fresh clone |
| Re-run of N-import coculture scripts | Methods scripts stop on explorer API changes (below); later scripts then lack their gitignored inputs. No encoding or pandas 3 errors |
| Skill links / cold read | Pass after fixing the 7 inconsistencies the cold read found |

## Explorer alpha.6 changes that break older analysis scripts

Added to the changelog's upgrade notes. All of them are analysis-side, not
template problems:

| Script | Error | Cause |
|---|---|---|
| `p2b_pfam_roles` | `KeyError: 'evidence_score'` | TCDB edge columns removed |
| `p3_group_systems` | `ValueError: window must be <= 100 (got 250)` | `gene_neighbors` window cap |
| `p4_neighbours` | new "Stereo forms hold more rows …" warning, rejected by the analysis's warning whitelist | new metabolite-tool warnings |
| `p5_substrates` | "No direct TCDB system call … pass `include_tcdb_family_substrates=True`" | TCDB family substrates now opt-in; the script also reads removed columns |

KG content changes, with no error raised:
- The MED4 transporter universe went from 365 to 225 genes. The TCDB calls
  went from 356 to 203; BRITE, Pfam and Cyanorak counts are unchanged.
- The axenic anchor RNA experiment went from 3,698 to 1,849 rows.
- The Tolonen experiments lost 1–6 rows each.

## Passed on

- **To the explorer:** the alpha.6 "Breaking" section omits the `gene_neighbors`
  window cap (listed under Fixed), the opt-in for TCDB family substrates, and
  the new warnings, all of which break existing scripts. Worth listing under
  Breaking next time.
- **To the analysis (N-import coculture):** its regenerated pipeline outputs
  are gitignored, so when one methods script breaks, every downstream script
  fails too, even the plotting-only ones.
