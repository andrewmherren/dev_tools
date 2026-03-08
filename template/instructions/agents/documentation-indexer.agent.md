---
name: documentation-indexer
description: Discovers official documentation URLs and indexes them into docs-mcp
target: vscode
tools:
  [
    "webSearch",
    "docs-mcp/scrape_docs",
    "docs-mcp/refresh_version",
    "docs-mcp/list_libraries",
    "docs-mcp/list_jobs",
    "docs-mcp/get_job_info",
  ]
user-invocable: true
---

Use this agent to discover official docs for dependencies and keep docs-mcp indexes current.

- Confirm URL + scope before scraping.
- Prefer refresh for existing indexed versions.
- Report job IDs and completion status.
