---
name: tasks
description: Create or update `_tasks/$ARGUMENTS.md` by decomposing a task in `docs/implements_plan.md` into an atomic-commit work task list. Use this when the user asks to break down an implementation-plan task into commit-sized steps for parallel development.
disable-model-invocation: true
---

# Task List Atomic

Use this skill to turn a task from `docs/implements_plan.md` into an implementation-ready task file at `_tasks/$ARGUMENTS.md`.

## Bundled Reference

- Read `references/task_template.md` first and follow it exactly.
- Output is limited to `_tasks/$ARGUMENTS.md`.

## Core Rules

- Prioritize the implementation plan and design documents. If information is missing, record it as `TBD`. Do not fill gaps by guessing.
- Do not proceed to implementation-ready planning while any `TBD` remains unresolved. Drafting is allowed, finalization is not.
- Keep `1 commit = 1 purpose`. Do not mix feature work, refactoring, test cleanup, documentation cleanup, or infra changes in the same commit unless the extra work is the minimum required to make that commit valid.
- Make every acceptance criterion terminal-verifiable using a command plus expected exit code or output. Do not use visual checks, browser checks, or subjective criteria.
- Every commit must be a buildable and testable unit.
- Use Conventional Commits: `<type>(<scope>): [$ARGUMENTS] <description>`.
- For each commit section, include the referenced design documents that justify that commit.
- Enforce the task fence strictly. Do not implement other tasks, adjacent screens, unrelated APIs, speculative work, or scope-external refactors.
- Do not write any file other than `_tasks/$ARGUMENTS.md` unless the user explicitly asks to resolve `TBD` values in design documents.

## Response Format

Every substantive response in this workflow should include:

1. current phase
2. gate result
3. scope boundary summary
4. main content
5. referenced design documents
6. `TBD` list
7. questions for unresolved `TBD` items when applicable
8. next action

## Workflow

1. Search `docs/implements_plan.md` for `$ARGUMENTS`.
2. If the task does not exist, stop and report that `$ARGUMENTS` was not found. Do not create `_tasks/$ARGUMENTS.md`.
3. Extract the task summary, priority, targets, dependencies, downstream tasks, and planning hints from `docs/implements_plan.md`.
4. Identify relevant design evidence in `docs/design/basic_design.md` and related files under `docs/design/`.
5. Define scope boundaries by listing `IN SCOPE`, `OUT OF SCOPE`, and `BOUNDARY` resources, including adjacent tasks and ownership where possible.
6. If scope boundaries are not defined, stop before commit planning.
7. Collect the detailed design constraints, interfaces, IDs, and data structures from the design documents.
8. Record every missing or ambiguous item as `TBD`.
9. If `TBD` remains, ask focused questions and stop before finalizing the task file. Only continue after those `TBD` values are resolved.
10. Determine `task_type` and `split_strategy` from the plan and design evidence. Use one of: `new_feature`, `change`, `bugfix`, `refactor`, `infra`, `migration`, `quality`, `security`, `release`, `other`.
11. Design the commit sequence in the order `foundation -> core -> integration -> finish`, with a maximum of 20 commits. Merge commits if the list would exceed 20.
12. For each commit, list the design documents or sections referenced by that commit.
13. Mark which commits are strictly sequential and which can be handled in parallel.
14. Write `_tasks/$ARGUMENTS.md` using `references/task_template.md` exactly, with no omitted sections.

## Gate Checks

### Gate 0

- `$ARGUMENTS` exists in `docs/implements_plan.md`
- dependency information is present or explicitly marked as none
- the split strategy can be justified from documented evidence

Suggested verification:

- `grep -n "$ARGUMENTS" docs/implements_plan.md`

### Gate 0.5

- `IN SCOPE` has at least one item
- `OUT OF SCOPE` has at least one item with owner task information when available
- `BOUNDARY` identifies shared resources and permissions
- no overlap exists with adjacent tasks for feature IDs, screen IDs, or API IDs

Do not proceed to commit design if scope boundaries are undefined.

### Gate 1

- relevant design files exist under `docs/`
- referenced IDs or sections can be found in those documents
- missing information is recorded in the `TBD` section

Suggested verification:

- `ls docs/`
- `grep "<ID>" <design_doc_path>`

### Gate 1.5

- all `TBD` items are resolved or explicitly marked as resolved
- if the user asked to resolve `TBD` in the source documents, those updates are reflected in `docs/`

Suggested verification:

- inspect the `TBD` section in `_tasks/$ARGUMENTS.md`
- `git diff docs/`

Do not proceed to commit design while any unresolved `TBD` remains.

### Gate 2

- `split_strategy` is one of the allowed enum values
- each commit has a single purpose
- commit count is 20 or fewer
- every acceptance criterion is terminal-verifiable
- every commit stays within `IN SCOPE`
- no boundary permission is violated

Suggested verification:

- `grep -c "^## C-" _tasks/$ARGUMENTS.md`

### Gate 3

- all template sections are filled
- acceptance criteria use terminal commands only
- scope boundary sections are complete

## Writing Rules

- When evidence is absent, write `TBD` rather than inventing details.
- If design documents conflict, preserve the conflict as `TBD` with cited sources.
- In each commit section, populate `参照設計書` with concrete document paths or sections. If the exact evidence is unknown, mark it as `TBD`.
- Use the current date in `YYYYMMDD` format and start the version at `1.0.0`.
- Keep acceptance criteria in `command -> expected result` form.
- Use only terminal-verifiable checks such as build, test, lint, typecheck, file existence, API status, or database status commands.
- Do not omit any section from the bundled template.

## Output

- Primary output: `_tasks/$ARGUMENTS.md`
- Expected outcome: an atomic-commit task file with explicit scope boundaries, evidence-backed decomposition, and terminal-verifiable acceptance criteria
