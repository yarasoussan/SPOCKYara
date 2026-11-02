# Methodology test brief — round 2 (testing the revised arc)

**Purpose.** Round 1 dogfooded the Plan→Run arc on one real analysis
(`analyses/2026-07-06-alteromonas_coculture_carbon_sources`) and answered its six
original questions — see [`methodology-review-2026-08.md`](methodology-review-2026-08.md).
Four changes came out of it and are now in the skill. **Round 2 tests those four
changes and settles the four findings that only occurred once.** Run the next real
analysis through the arc and record the answers as you go.

Round 1's questions are answered; don't re-run them. What's still open is below.

**Before you start (in the new chat):**

- The arc lives on `main` — no special branch. *(Round 1 ran on
  `methodology/plan-run-arc`, since merged; ignore that instruction if you see it
  in an old note.)*
- Open with the research question. The `research-methodology` skill loads
  automatically and should walk the arc: **Plan phase** (one grounded
  `superpowers:brainstorming` conversation → `proposal.md`, closing on self-review
  → proposal critic → your approval), then **Run phase** (`methods/` → `analysis/`
  → `evaluation/`, each advancing co-define → do → show → explore → decide, one
  commit each, execution delegated to a coding subagent).

---

## Watch-list A — do the four applied changes work?

These are new skill text with one incident behind each. Watch for both failure
directions: the change not firing when it should, and the change firing as
ceremony when there's nothing to catch.

1. **Automatic methods critic (when the milestone emits a data artifact).** Did it
   fire? Did it find anything a later pass wouldn't have — or did it burn a
   dispatch on a milestone with nothing to bite? If this analysis's methods
   milestone emits *no* data file, say so: the conditional is the part under test.
2. **The delta pass after exploration.** Exploration happens after the critic by
   construction. Did the delta pass actually get dispatched at the analysis
   milestone, and did scoping it to the delta (prior files as trusted inputs) keep
   it cheap?
3. **Fixture realism + spot-run on a real row.** Did writing fixtures in the real
   serialization form catch anything, or feel like overhead? Did the main-thread
   spot-run surface a bug the suite missed (round 1's `bool("False")` case)?
4. **Friction logged during the late milestones.** Round 1's log went quiet three
   days before the analysis and evaluation milestones ran. Does
   `gaps_and_friction.md` now carry entries dated *through* the end of the run —
   or did the decide-gate check just get ticked?

## Watch-list B — the four findings that need a second occurrence

Each of these happened once in round 1. One occurrence is a note; a second makes
it a skill change. Record what happens either way — a clean run is also evidence.

5. **Does the Plan phase reach a natural stop?** Round 1 took six commits and six
   critic passes, two of them *after* the commit labelled "approved," and the
   proposal reached 778 lines. Does this plan converge, or keep re-opening? Is
   "one commit for the Plan phase" ever true?
6. **Does the framing need a cross-experiment comparability statement?** Round 1's
   conclusion rested on agreement across experiments while the metric's
   comparability across them (FDR families of 46 vs 3–5 modules) was never stated
   — caught post hoc by the critic. If this analysis compares across experiments,
   did the framing floor's five items leave the same hole?
7. **Does the falsifiability check / expected-negative earn its place?** Round 1's
   sharpest instrument was a gene set that should *not* come up (the aromatic
   prong); it recurred in the re-run and is now a required framing item (the fifth
   floor item). Did naming it up front change the plan or the read of a null — or
   was it ceremony?
8. **Is "the methods milestone stays minimal" true?** Round 1's was a discovery
   milestone: 8 scripts, a genome-inventory reveal that inverted the proposal's
   counting unit, and a decision that superseded a locked proposal decision. Does
   that recur when the method includes constructing the entity set?

## Also worth noticing

- **Delegation cost.** Round 1 lost one subagent dispatch to context overflow on a
  large enumeration (fix: script results to disk via the Python API). Does the
  re-invoke loop stay clean at scale?
- **Anything that creaks that isn't on this list.** The list is what we predicted;
  the useful finding is usually what we didn't.

---

**Where to log:**

- **Friction** → `analyses/<slug>/gaps_and_friction.md` (as the methodology
  prescribes — and now checked at each decide gate).
- **Wins** (where the structure actively helped) → a short scratch note for this
  run; `gaps_and_friction.md` is a problem log and won't hold positive signal.
- **Watch-list answers** → answer them inline as they resolve, so the evidence is
  written while it's fresh rather than reconstructed at the end.

**After the run:** bring the friction notes, the wins note, and the watch-list
answers back to the methodology chat for a round-2 review, in the same shape as
[`methodology-review-2026-08.md`](methodology-review-2026-08.md). Findings that
now have two occurrences become skill changes; the rest stay notes.
