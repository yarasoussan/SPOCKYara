# usage/

MCP tool-usage logs, written **into the repo** (un-ignored in `.gitignore`).

- `multiomics-kg-usage.jsonl` — one line per `multiomics-kg` MCP call, appended
  by `hooks/log-mcp-usage.sh`. Each line stamps the template version, the tool
  name + inputs, and response metadata.
- `preflight.jsonl` — one line per `./scripts/preflight.sh` run, recording the
  full **version triple** (template / explorer / KG) and the connection verdict.

**Commit these alongside your analysis commits.** They feed the alpha's
usage-logging purpose — showing how the KG tools get used so they can be
improved. Attribution is by fork owner (these logs are public; see the README).
