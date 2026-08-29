# AGENTS.md — Genius-Verification

## Buildkite execution

Expected Buildkite pipeline slug: `genius-verification`.

When Buildkite tools are available, use Buildkite's official remote MCP server at `https://mcp.buildkite.com/mcp` and inspect live pipeline/build state before making CI claims.

Primary Buildkite lane:

- contract validation with Python 3.13;
- bytecode compilation of verification tooling as a syntax sanity check.

Useful commands:

```sh
bk pipeline validate --file .buildkite/pipeline.yml
bk pipeline view genius-verification --json
bk build view --pipeline genius-verification --summary
```

A repository pipeline definition is not execution evidence. Completion requires a live Buildkite build result.
