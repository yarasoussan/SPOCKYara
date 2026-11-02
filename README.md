# Spock — multi-omics research template (alpha)

A ready-to-use starting point for doing computational research on the lab's
multi-omics **knowledge graph** — without writing database queries or analysis
code yourself. The knowledge graph is the lab's integrated database for the
marine cyanobacterium *Prochlorococcus* and the heterotrophic bacterium
*Alteromonas*: their genes, gene expression measured across many experiments,
ortholog relationships, metabolites, and how these connect. You ask research
questions in plain English inside **Claude
Code** (an AI assistant that runs in the VS Code editor); it queries the
knowledge graph, runs the statistics, makes the figures, and writes up the
results following a rigorous, reproducible methodology built into this repo.

**Who this is for:** lab biologists. **No prior experience with VS Code, git,
GitHub, or the command line is assumed** — this guide walks you through the
one-time setup step by step. When something doesn't work, the lab operator (the
person who set up the knowledge graph) is your first port of call.

## What you'll actually do

1. Make your own copy of this template (a **fork**) and download it to your
   computer (a **clone**).
2. Point it at the lab's knowledge-graph database (one-time credentials).
3. Open it in VS Code and chat with Claude in plain English, e.g.
   *"What genes respond when MED4 is starved of nitrogen?"*
4. Claude does the querying, analysis, and write-up — saving everything into
   your copy as files you can revisit, share, and publish from.

You direct the research; Claude is the analyst. The methodology built into this
repo keeps the science honest: every claim is traced to the data, gene
identities aren't guessed, and statistics are done properly.

### A few terms you'll see

| Term | What it means here |
|---|---|
| **Knowledge graph (KG)** | The lab's multi-omics database — *Prochlorococcus* & *Alteromonas* genes, expression, orthologs, metabolites, and more. |
| **Claude Code** | Anthropic's AI coding assistant; runs inside VS Code. |
| **MCP server** | The bridge that lets Claude query the KG. This repo wires it up for you — you never configure it by hand. |
| **Repository ("repo")** | A project folder tracked by **git** (which records the history of your changes). This template is one. |
| **Fork / clone** | A *fork* is your own copy of the template on GitHub. A *clone* is that copy downloaded onto your laptop. |
| **`uv`** | A tool that sets up Python and installs the analysis software in one step. |

> **⚠ Your fork is public.** This is an open-science alpha: the template, all
> forks, your analyses, **and** your usage logs are public and indexable —
> including in-progress, unpublished work. Know this before you start. If a
> specific analysis must stay private, gitignore its directory locally; the
> default is public.

---

## One-time setup

### Install these first

You need all of the following, installed once. None is optional: preflight
checks for them and goes red if one is missing.

- **[VS Code](https://code.visualstudio.com/)** — the editor everything runs in
- **[Claude Code](https://claude.com/claude-code)** — the AI assistant (added to VS Code), plus a **Claude account** with Claude Code access to sign in with. Keep it current (`claude update`): the `dataviz` skill the figures rely on ships with Claude Code itself
- **[git](https://git-scm.com/downloads)** — tracks your work. **On Windows this must be Git for Windows**, which also installs **Git Bash**: the preflight check and the usage logger are bash scripts, so run them from a Git Bash terminal
- **[uv](https://docs.astral.sh/uv/)** — installs Python (3.12, pinned by the repo) and the analysis tools for you
- **[jq](https://jqlang.github.io/jq/)** — used by the usage logger; without it no usage is recorded
- A free **[GitHub account](https://github.com/signup)** — to fork the template, and **signed in on this computer** so you can push your work at the end of an analysis. On Windows and Mac, git asks you to sign in through the browser the first time you push

Quickest way to install the command-line tools (then install Claude Code from its link above):

| OS | Command |
|---|---|
| **Windows** (PowerShell) | `winget install Microsoft.VisualStudioCode Git.Git astral-sh.uv jqlang.jq --accept-source-agreements --accept-package-agreements` — one command for all four. If an older winget rejects several names, run `winget install <name>` once per package |
| **macOS** ([Homebrew](https://brew.sh)) | `brew install git uv jq` and `brew install --cask visual-studio-code` |
| **Linux** (Debian/Ubuntu) | `sudo apt install git jq`, then `curl -LsSf https://astral.sh/uv/install.sh \| sh` |

Close and reopen VS Code (and any terminal) afterwards, so the new tools are on your PATH.
On Windows, set VS Code's terminal to Git Bash: **Terminal → New Terminal**, then the
**˅** next to **+** → **Git Bash** (or *Select Default Profile* → **Git Bash** to make it stick).

> **New to the command line?** The steps below are commands you paste into a
> terminal. VS Code has one built in: **View → Terminal**. Open this folder in
> VS Code first, then paste each command into that terminal and press Enter.

You also need **lab-subnet (or VPN) access** to the KG box. Network details and
credentials come from the lab operator — ask them for the **KG connection
guide** (canonically `multiomics_biocypher_kg/docs/kg_mcp_guide.md`).

### 1. Fork, clone & install

Fork [TheSherLab/spock](https://github.com/TheSherLab/spock) on GitHub first
(the **Fork** button, top-right of the repo page). Then, in a terminal:

```bash
# Replace <your-fork-url> with the URL of YOUR fork (green "Code" button on your fork):
git clone <your-fork-url>
cd spock                      # the folder git clone just made — matches your fork's name if you renamed it
git remote add upstream https://github.com/TheSherLab/spock.git   # lets you pull updates later
uv sync                       # installs the explorer tools + analysis libraries
```

### 2. Set KG credentials

Credentials come from the lab operator (see the **KG connection guide**).
**Never commit them** — the steps below keep them out of git automatically.

**Recommended — all platforms: a gitignored `.env` file in the repo root.**

```bash
cp .env.example .env     # makes your own .env; then open .env in VS Code and fill in:
#   NEO4J_URI=bolt://HOST:PORT      # exact value from the KG connection guide
#   NEO4J_USERNAME=explorer
#   NEO4J_PASSWORD=…
```

Claude reads `.env` automatically (the MCP server runs from this folder). This
works identically on Linux, Windows 11, and Remote-SSH.

<details>
<summary><b>Alternative — shell / OS environment</b> (if you'd rather not keep a creds file)</summary>

- **Linux:** `export NEO4J_*` in `~/.bashrc`, then launch VS Code from that
  terminal (`code .`) — a VS Code opened from the desktop icon won't inherit them.
- **Windows 11:** set them as User Environment Variables (PowerShell:
  `[Environment]::SetEnvironmentVariable("NEO4J_URI","…","User")`), then restart VS Code.
- **Windows 11 + Remote-SSH:** set them on the **remote** host (where the MCP
  runs), not on Windows — or just use the `.env` method, which is simplest here.

</details>

### 3. Open in Claude Code & trust the workspace

Open this folder in VS Code. When prompted, **trust the workspace** — this lets
the research skills load, the MCP server start, and the required **`superpowers`**
plugin install (the methodology's Plan-phase brainstorming depends on it; it's declared
in `.claude/settings.json` and pulled from the official Anthropic marketplace on
trust). Confirm the `multiomics-kg` server shows as connected by running `/mcp` in
a Claude chat.

> If preflight later reports the plugin missing (some setups don't auto-install on
> trust), install it once by hand:
> ```bash
> claude plugin install superpowers@claude-plugins-official
> ```

### 4. Preflight (the "is everything wired up?" check)

```bash
./scripts/preflight.sh        # checks versions + KG connection + a real query → green/red
```

**Green** = you're clear to start. **Red** = it tells you exactly what's wrong,
with a specific hint for the three common problems: credentials not set, not on
the lab subnet, or a version mismatch. Fix it before starting a research chat.

### 5. Start an analysis

Open a new Claude chat and ask your research question. The `research-methodology`
skill loads automatically and guides the work through a two-phase arc: a **Plan**
phase (question → KG entries → enumerated framing, converged into `proposal.md`)
and a **Run** phase (methods → analysis → evaluation). Everything Claude produces
is saved under `analyses/` in **your** copy. Claude commits every iteration as it
goes (with the `usage/` logs, which help improve the tools), marks each step you
approve with an *approved* commit, and asks you to **push** when the analysis is
done. Say no if the work must stay private for now; your fork is public.

What you get back at each step:
- **`index.html`** at the analysis root — open it in a browser: it links every
  report (figures you can hover over, tables you can sort and filter) and the
  paper draft. Bookmark it; it is the one page to open.
- **`paper.md`** at the analysis root — written as paper text you can drop into a
  manuscript's Methods, Results and Discussion. **`paper.html`** is the same text
  with figures and tables in place; Print → Save as PDF from your browser for a PDF.
- **`gaps_and_friction.md`** — what went wrong and what worked. Please keep it
  honest: it is the evidence for improving the method.

> **Fewer permission prompts (optional).** Claude Code's *auto* permission mode
> lets it run routine commands without asking each time. It is set per user, not
> per repo: check your mode with `/status`, and see the Claude Code docs on
> permission modes before turning it on.

---

## Keeping up to date

```bash
git pull upstream main && uv sync     # preflight warns you when you're behind
```

The pull brings new skills and a possibly-updated explorer version; `uv sync`
installs it. Preflight verifies the two match.

**If the pull stops with a conflict in `pyproject.toml` / `uv.lock`** (it will if
you added a package yourself, e.g. with `uv add`): in `pyproject.toml`, keep
**both** lists of dependencies (delete only the `<<<<<<<`, `=======` and
`>>>>>>>` marker lines), then regenerate the lock file instead of merging it:

```bash
git checkout --theirs uv.lock && uv lock && uv sync
git add pyproject.toml uv.lock && git commit --no-edit
```

---

**Connection specifics** — the lab Bolt URI, firewall/subnet checks, and
shared-credential handling — live in the **KG connection guide**, not here. This
README links to it rather than copying it, so the instructions never drift.
