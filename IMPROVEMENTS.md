# IMPROVEMENTS.md

You are the coordinator agent for this repository. Your job is to implement all improvements below by delegating work to subagents in parallel, then integrating and validating all outputs.

## Mission

Implement incremental, low-risk improvements to make agent-driven verification reliable and repeatable, with emphasis on executable test/spec adherence workflows.

## Critical Constraints

- Use only local repository context and `docs-mcp` indexed docs for knowledge.
- Subagents must not rely on web search.
- Before any implementation subtask starts, run the documentation indexing preparation tasks below.
- Preserve existing repository conventions and merge behavior.
- Do not remove existing functionality.
- Keep changes incremental and focused.
- Prefer updating existing files over adding many new files.
- Keep secrets out of source-controlled files.
- Use ASCII-only edits unless a file already requires Unicode.
- Validate changes with available checks/tasks and report gaps explicitly.

## Repository Facts (Ground Truth)

- Template task scaffold currently lacks real test/lint/verify execution entrypoints:
  - `template/.vscode/tasks.json.jinja`
- Language conventions mention quality goals but not canonical runnable test command contracts:
  - `template/instructions/languages/python-conventions.md`
  - `template/instructions/languages/nodejs-conventions.md`
  - `template/instructions/languages/rust-conventions.md`
  - `template/instructions/languages/cpp-conventions.md`
  - `template/instructions/languages/godot-conventions.md`
  - `template/instructions/languages/unreal-conventions.md`
- Shared template MCP defaults currently include `docs-mcp` and `filesystem`, with Sonar disabled:
  - `template/fragments/shared/mcp.json`
  - `template/instructions/common/mcp-policy.md`
- Existing infra already includes SonarQube and Trivy services:
  - `docker-compose.yml`
- Existing docs already describe Sonar setup flow:
  - `homepage/PROJECT_SETUP.md`

## High-Level Deliverables

1. Canonical test/verify task framework in template-generated VS Code tasks.
2. Clear agent verification contract in instructions/docs.
3. Better testing extension recommendations per language.
4. Optional security/quality validation tasks (Sonar and Trivy), implemented safely and opt-in where needed.
5. Final validation report with what was changed, what was verified, and residual risks.

---

## Phase 0: Documentation Index Preparation (Required First)

Assign all tasks in this phase to `documentation-indexer` subagents.  
Goal: ensure downstream subagents can query authoritative docs from local `docs-mcp` without web search.

### D0.1: Index VS Code Tasks docs

- Agent: `documentation-indexer`
- Target source:
  - `https://code.visualstudio.com/docs/editor/tasks`
- Action:
  - Index/update docs in `docs-mcp`.
  - Record job ID and completion status.
- Output:
  - Confirm indexed library/resource name and retrievable status.

### D0.2: Index VS Code Testing docs

- Agent: `documentation-indexer`
- Target source:
  - `https://code.visualstudio.com/docs/debugtest/testing`
- Action:
  - Index/update docs in `docs-mcp`.
  - Record job ID and completion status.
- Output:
  - Confirm indexed library/resource name and retrievable status.

### D0.3: Index SonarScanner CLI docs

- Agent: `documentation-indexer`
- Target source:
  - `https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/scanners/sonarscanner`
- Action:
  - Index/update docs in `docs-mcp`.
  - Record job ID and completion status.
- Output:
  - Confirm indexed library/resource name and retrievable status.

### D0.4: Index Trivy client/server docs

- Agent: `documentation-indexer`
- Target source:
  - `https://trivy.dev/latest/docs/references/modes/client-server/`
- Action:
  - Index/update docs in `docs-mcp`.
  - Record job ID and completion status.
- Output:
  - Confirm indexed library/resource name and retrievable status.

### D0 acceptance criteria

- All four sources are indexed and queryable via `docs-mcp`.
- Coordinator posts a short “docs readiness” checkpoint before Phase 1 starts.

---

## Phase 1: Parallel Implementation Tasks

Run T1-T4 in parallel after D0 completes.

### T1: Canonical Test and Verify Tasks

- Agent: `subagent-tasking-core`
- Primary files:
  - `template/.vscode/tasks.json.jinja`
  - `template/README.md`
  - `template/README.md.jinja`
- Required work:
  1. Add real `test` task defaults by language/execution mode where feasible.
  2. Mark test task with `group.kind: "test"` and default where appropriate.
  3. Add `lint` and `typecheck` task stubs or concrete commands where safe defaults are known.
  4. Add `verify` compound task (`dependsOn`) that runs at least `test` + `lint` (and `typecheck` when available).
  5. Keep behavior safe for projects before full toolchain install (clear fallback messaging where needed).
- Notes:
  - Keep existing build tasks intact.
  - Avoid over-prescriptive commands that will fail universally across all projects.
  - Prioritize deterministic, low-friction defaults.

### T2: Testing Extension Recommendations

- Agent: `subagent-extensions`
- Primary files:
  - `template/fragments/languages/python-extensions.json`
  - `template/fragments/languages/nodejs-extensions.json`
  - `template/fragments/languages/rust-extensions.json`
  - `template/fragments/languages/cpp-extensions.json`
  - `template/fragments/languages/godot-extensions.json`
  - `template/fragments/languages/unreal-extensions.json`
- Required work:
  1. Add/testing-focused extension recommendations where high-confidence and low-risk.
  2. Keep extension lists lean and relevant.
  3. Beware of security risks and only propose extensions from extensions that are highly trusted.
  4. Do not remove currently recommended core language tooling unless clearly obsolete.
- Notes:
  - Validate extension IDs.
  - Avoid adding niche extensions that are likely to create maintenance overhead.

### T3: Agent Verification Contract and Guidance

- Agent: `subagent-instructions`
- Primary files:
  - `template/instructions/common/mcp-policy.md`
  - `template/instructions/common/git-safety.md`
  - `template/instructions/languages/*.md` (as needed)
  - Optionally add one new common instruction file if needed
- Required work:
  1. Define a lightweight “Agent Verification Contract”:
     - After code edits, run `test` or `verify`.
     - Report exact commands run, pass/fail status, and uncovered risk areas.
  2. Clarify expected fallback behavior when tasks/tools are unavailable.
  3. Ensure guidance remains compatible with current security/secret handling rules.
- Notes:
  - Keep policy concise and actionable.
  - Avoid duplicating existing docs excessively.

### T4: Optional Sonar and Trivy Task Integration

- Agent: `subagent-quality-security`
- Primary files:
  - `template/.vscode/tasks.json.jinja`
  - `homepage/PROJECT_SETUP.md` (if updates needed)
  - `docs/mcp-policy.md` or template equivalents (if updates needed)
- Required work:
  1. Add optional Sonar scan task that works when token/env is present.
  2. Add optional Trivy task aligned with client/server mode where practical.
  3. Make both tasks clearly optional and non-blocking by default.
- Notes:
  - Do not hardcode secrets.
  - Respect existing env-var based secret policy.

---

## Phase 2: Integration and Consistency Pass

- Agent: `subagent-integrator`
- Required work:
  1. Merge outputs from T1-T4.
  2. Resolve conflicts while preserving existing repository conventions.
  3. Ensure template semantics remain coherent across language/mode combinations.
  4. Ensure docs and tasks do not contradict each other.

---

## Validation Requirements

Coordinator must execute and report:

1. Template integrity checks:

- Ensure modified template files render correctly (no broken Jinja syntax).
- Ensure no malformed JSON fragments.

2. Behavioral checks:

- Confirm generated task model now exposes:
  - runnable `test`
  - runnable/defined `verify`
  - task grouping for test where appropriate

3. Policy checks:

- Confirm no secrets were introduced.
- Confirm new instruction text is concise and non-contradictory.

4. Reporting:

- For each changed file:
  - what changed
  - why
  - any compatibility caveat
- Explicitly list anything not validated and why.

---

## Task Prioritization

Use this order if resource constrained:

1. T1 Canonical test/verify tasks
2. T3 Agent verification contract
3. T2 Testing extension recommendations
4. T4 Optional Sonar/Trivy tasks
5. Integration and validation

---

## Definition of Done

- D0 indexing tasks completed and confirmed queryable in `docs-mcp`.
- Template has concrete, reusable test/verify task workflow.
- Instructions clearly require post-edit verification and transparent reporting.
- Language extension recommendations better support testing workflows.
- Optional Sonar/Trivy task paths exist without introducing secret risk.
- Coordinator submits final report with:
  - completed tasks
  - file-level diff summary
  - validation outcomes
  - residual risks/gaps

---

## Final Output Format (Coordinator)

Return sections in this exact order:

1. `Completed Work`
2. `Changed Files`
3. `Validation Performed`
4. `Open Risks / Not Validated`
5. `Suggested Next Increment (Optional)`

Keep output concise, factual, and implementation-focused.
