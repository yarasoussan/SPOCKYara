# analyses/

Your research output lives here — **one directory per analysis**. This folder
ships empty (just this README); each analysis is scaffolded by the
`research-methodology` skill when you start it.

The skill's `references/step-protocol.md` and `references/artifacts.md` own the
authoritative structure. In brief, an analysis directory looks like:

```
analyses/YYYY-MM-DD-short_slug/
  paper.md                 # the running synthesis (grows across the arc)
  gaps_and_friction.md     # friction + tool gaps surfaced during the work
  .gitignore               # per-analysis ignores (created at scaffold)
  proposal.md              # question + KG entries + enumerated framing (the plan)
  proposal_notebook.md     # brainstorming record: grounding queries, rejected alternatives
  methods/
    notebook.md            # lab notebook + decide-gate checklist (main-thread owned)
    <module_name>.py       # ad-hoc methods module
    scripts/ data/ figures/    # (qc_* prefix for QC artifacts)
  analysis/  evaluation/
    ...
```

The arc is two phases: a **Plan** phase (one `superpowers:brainstorming`
conversation converging on `proposal.md`, one commit) and a **Run** phase (three
milestones — methods → analysis → evaluation — each advancing **co-define → do →
show → explore → decide**, one commit per milestone at the decide gate). Don't
hand-scaffold this — let the skill drive it so the gates and manifests stay
consistent.

Commit the repo-root `usage/` logs alongside your analysis commits.
