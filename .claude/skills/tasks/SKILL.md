---
name: tasks
description: Create or update `_tasks/$ARGUMENTS.md` by decomposing a task in `docs/implements_plan.md` into an atomic-commit work task list. Use this when the user asks to break down an implementation-plan task into commit-sized steps for parallel development.
---

# Task List Atomic

Use this skill to turn a task from `docs/implements_plan.md` into an implementation-ready task file at `_tasks/$ARGUMENTS.md`.

## Bundled Reference

- Read `references/task_template.md` first and follow it exactly.
- Output is limited to `_tasks/$ARGUMENTS.md`.

## Operating Model

This skill is **retrieval-first** and **non-blocking by default**.

When information is incomplete, do **not** stop immediately and do **not** emit `TBD` as the default outcome. Investigate missing facts first. If evidence is still incomplete, continue safely by separating repository-backed facts from AI-added mitigations.

Use the following labels consistently:

- `[EVIDENCE]` = grounded in repository documents, code, tests, configs, scripts, existing task files, or other verified references
- `[AI-PROPOSAL]` = a mitigation, workaround, fallback, or decomposition decision proposed by the AI
- `[ASSUMPTION]` = a reversible, low-risk placeholder used so planning can continue safely
- `[BLOCKED]` = an unresolved item that makes correct, safe, or scope-compliant continuation impossible

Never present `[AI-PROPOSAL]` or `[ASSUMPTION]` as if they were documented facts.

## Core Rules

- Prioritize repository evidence first. Search documentation, code, tests, configs, scripts, existing `_tasks/`, and related artifacts before concluding that information is missing.
- Do not guess missing facts.
- Do not use `TBD` in the output task file.
- If evidence is unavailable, the AI may add a mitigation, workaround, fallback, or reversible planning decision, but it must be labeled as `[AI-PROPOSAL]` or `[ASSUMPTION]`.
- Do not stop merely because information is incomplete. Stop only when a critical `[BLOCKED]` item remains after investigation.
- Every `[AI-PROPOSAL]` must include:
  1. why it is needed
  2. what evidence gap triggered it
  3. risk level
  4. whether it is reversible
- Prefer repository-local evidence over external references.
- If repository-local evidence is insufficient and approved external references are available, use them only to clarify standards, library behavior, framework constraints, or commands needed for terminal-verifiable acceptance criteria.
- Keep `1 commit = 1 purpose`. Do not mix feature work, refactoring, test cleanup, documentation cleanup, or infra changes in the same commit unless the extra work is the minimum required to make that commit valid.
- Make every acceptance criterion terminal-verifiable using a command plus expected exit code or output. Do not use visual checks, browser checks, or subjective criteria.
- Every commit must be a buildable and testable unit.
- Use Conventional Commits: `<type>(<scope>): [$ARGUMENTS] <description>`.
- For each commit section, include the referenced design documents or evidence sources that justify that commit.
- Enforce the task fence strictly. Do not implement other tasks, adjacent screens, unrelated APIs, speculative work, or scope-external refactors.
- Do not write any file other than `_tasks/$ARGUMENTS.md` unless the user explicitly asks to update repository source documents.
- Do not stop at the first plausible plan. Check for missing constraints, adjacent ownership boundaries, second-order impacts, and safer reversible mitigations before finalizing.

## Response Format

Every substantive response in this workflow should include:

1. current phase
2. gate result
3. scope boundary summary
4. evidence gathered
5. AI-proposed mitigations
6. assumptions used
7. blocked items
8. main content
9. referenced design documents
10. next action

### Response Formatting Rules

- `evidence gathered` must contain only `[EVIDENCE]` items.
- `AI-proposed mitigations` must contain only `[AI-PROPOSAL]` items.
- `assumptions used` must contain only `[ASSUMPTION]` items.
- `blocked items` must contain only `[BLOCKED]` items.
- Do not mix evidence and AI proposals in the same bullet.
- If there are no items for `AI-proposed mitigations`, `assumptions used`, or `blocked items`, write `none`.
- The final `_tasks/$ARGUMENTS.md` must not contain `TBD`.
- If the plan proceeds using `[AI-PROPOSAL]` or `[ASSUMPTION]`, make that traceable in the relevant commit section or notes.

## Investigation Order

When a needed fact is missing or ambiguous, investigate in this order before considering `[BLOCKED]`:

1. `docs/implements_plan.md`
2. `docs/design/basic_design.md`
3. related files under `docs/design/`
4. existing `_tasks/`
5. related code under application and library directories
6. related tests
7. configs, scripts, CI definitions, linters, typecheck configs, migration files
8. neighboring tasks, screen IDs, feature IDs, API IDs, schema definitions
9. git history or blame when useful and available
10. approved external references for framework/library/standard clarification only

If one search is empty or too narrow, retry with a different strategy:
- alternate query wording
- broader path scope
- related identifiers
- neighboring task names
- interface names
- test names
- config keys

Use at least 2 distinct retrieval attempts before marking an item `[BLOCKED]`, unless the task itself is missing from `docs/implements_plan.md`.

## Workflow

1. Search `docs/implements_plan.md` for `$ARGUMENTS`.
2. If the task does not exist, stop and report that `$ARGUMENTS` was not found. Do not create `_tasks/$ARGUMENTS.md`.
3. Extract the task summary, priority, targets, dependencies, downstream tasks, and planning hints from `docs/implements_plan.md`.
4. Identify relevant design evidence in `docs/design/basic_design.md` and related files under `docs/design/`.
5. Define scope boundaries by listing `IN SCOPE`, `OUT OF SCOPE`, and `BOUNDARY` resources, including adjacent tasks and ownership where possible.
6. If scope boundaries are still undefined after investigation, determine whether safe continuation is possible:
   - use `[ASSUMPTION]` if the boundary can be narrowed safely and reversibly
   - use `[AI-PROPOSAL]` if the AI can propose a concrete containment strategy
   - use `[BLOCKED]` only if scope cannot be made safe
7. Collect detailed design constraints, interfaces, IDs, data structures, commands, file paths, validation methods, and dependency edges from repository evidence.
8. Record missing or ambiguous items as `candidate_gaps` internally and investigate them using the `Investigation Order`.
9. For each unresolved `candidate_gap`, classify it as one of:
   - `[ASSUMPTION]` if continuation is safe and reversible
   - `[AI-PROPOSAL]` if the AI can provide a concrete workaround, adapter, staged rollout, validation shortcut, or decomposition strategy
   - `[BLOCKED]` only if the unresolved item is critical and proceeding would likely cause incorrect, unsafe, or scope-violating output
10. Continue planning as far as safely possible even when non-critical gaps remain.
11. Determine `task_type` and `split_strategy` from the plan and evidence. Use one of: `new_feature`, `change`, `bugfix`, `refactor`, `infra`, `migration`, `quality`, `security`, `release`, `other`.
12. Design the commit sequence in the order `foundation -> core -> integration -> finish`, with a maximum of 20 commits. Merge commits if the list would exceed 20.
13. For each commit:
   - keep a single purpose
   - identify referenced design documents and evidence sources
   - list terminal-verifiable acceptance criteria
   - mark whether the commit is sequential or parallelizable
   - separate evidence-backed requirements from `[AI-PROPOSAL]` or `[ASSUMPTION]`
14. If `[AI-PROPOSAL]` is used in a commit, include:
   - trigger
   - proposal
   - rationale
   - risk
   - reversible yes/no
   - validation command
15. Write `_tasks/$ARGUMENTS.md` using `references/task_template.md` exactly, with no omitted sections.
16. Before finalizing, verify that:
   - no `TBD` remains
   - no undocumented fact is presented as evidence
   - every non-evidence item is labeled as `[AI-PROPOSAL]`, `[ASSUMPTION]`, or `[BLOCKED]`
   - no critical `[BLOCKED]` item remains if the file is finalized

## Gate Checks

### Gate 0

- `$ARGUMENTS` exists in `docs/implements_plan.md`
- dependency information is present, inferable from repository evidence, or explicitly marked as none
- the split strategy can be justified from documented evidence or a clearly labeled `[AI-PROPOSAL]`

Suggested verification:

- `grep -n "$ARGUMENTS" docs/implements_plan.md`

### Gate 0.5

- `IN SCOPE` has at least one item
- `OUT OF SCOPE` has at least one item with owner task information when available
- `BOUNDARY` identifies shared resources and permissions
- no overlap exists with adjacent tasks for feature IDs, screen IDs, or API IDs, or any overlap is explicitly contained by `[ASSUMPTION]` or `[AI-PROPOSAL]`
- no critical boundary ambiguity remains unresolved

Do not proceed to commit design only if a critical `[BLOCKED]` boundary issue remains.

### Gate 1

- relevant design files or repository evidence exist
- referenced IDs, sections, interfaces, commands, or data structures can be found or reasonably triangulated from evidence
- missing information is either resolved, converted into `[ASSUMPTION]`, converted into `[AI-PROPOSAL]`, or marked `[BLOCKED]`

Suggested verification:

- `ls docs/`
- `grep "<ID>" <design_doc_path>`
- repository search commands as needed

### Gate 1.5

- all critical gaps are either resolved by evidence or explicitly marked `[BLOCKED]`
- all non-critical gaps are resolved, contained by `[ASSUMPTION]`, or handled by `[AI-PROPOSAL]`
- no item remains as unlabeled uncertainty
- if repository documents were updated by explicit user request, those updates are reflected in `docs/`

Suggested verification:

- inspect `_tasks/$ARGUMENTS.md` for unlabeled uncertainty
- `grep -n "TBD" _tasks/$ARGUMENTS.md` should return no matches
- `git diff docs/`

Do not proceed to commit design while any critical `[BLOCKED]` item remains.

### Gate 2

- `split_strategy` is one of the allowed enum values
- each commit has a single purpose
- commit count is 20 or fewer
- every acceptance criterion is terminal-verifiable
- every commit stays within `IN SCOPE`
- no boundary permission is violated
- every `[AI-PROPOSAL]` includes trigger, rationale, risk, reversibility, and validation

Suggested verification:

- `grep -c "^## C-" _tasks/$ARGUMENTS.md`
- `grep -n "AI-PROPOSAL" _tasks/$ARGUMENTS.md`

### Gate 3

- all template sections are filled
- acceptance criteria use terminal commands only
- scope boundary sections are complete
- no `TBD` remains
- facts, assumptions, proposals, and blocked items are clearly separated

Suggested verification:

- `grep -n "TBD" _tasks/$ARGUMENTS.md` returns no matches
- template headings match `references/task_template.md`

## AI-Proposal Format

When an AI-added mitigation is required, use the following structure in the relevant section:

```text
[AI-PROPOSAL] <short title>
- Trigger: <what evidence gap caused this>
- Proposal: <the AI-added mitigation or workaround>
- Rationale: <why this is a reasonable next step>
- Risk: low | medium | high
- Reversible: yes | no
- Validation: <terminal-verifiable command or check>
````

## Assumption Format

When a reversible low-risk assumption is required, use the following structure:

```text
[ASSUMPTION] <short title>
- Gap: <what is not fully documented>
- Assumption: <the reversible placeholder>
- Safety basis: <why continuing is still safe>
- Reversible: yes
- Validation: <terminal-verifiable command or follow-up check>
```

## Blocked Format

When continuation must stop, use the following structure:

```text
[BLOCKED] <short title>
- Missing: <critical missing item>
- Investigation performed: <searches or evidence attempted>
- Why blocked: <why safe continuation is not possible>
- Required resolution: <what must be clarified>
```

## Writing Rules

* When evidence is absent, do not invent facts.
* Prefer `[AI-PROPOSAL]` or `[ASSUMPTION]` over stopping when continuation is safe.
* If design documents conflict, preserve the conflict explicitly and classify it as:

  * `[EVIDENCE]` for each conflicting source
  * `[AI-PROPOSAL]` if the AI suggests a containment strategy
  * `[BLOCKED]` only if the conflict is critical
* In each commit section, populate `参照設計書` with concrete document paths, repository evidence, or sections. If exact evidence cannot be found, do not fabricate it; use a labeled `[AI-PROPOSAL]` or `[ASSUMPTION]` as appropriate.
* Use the current date in `YYYYMMDD` format and start the version at `1.0.0`.
* Keep acceptance criteria in `command -> expected result` form.
* Use only terminal-verifiable checks such as build, test, lint, typecheck, file existence, API status, or database status commands.
* Do not omit any section from the bundled template.
* Do not use vague wording such as `probably`, `maybe`, or `TBD` in the final task file. Classify the item explicitly instead.
* When AI-added content is used, make it easy for reviewers to distinguish it from documented requirements.

## Completion Standard

A finalized `_tasks/$ARGUMENTS.md` is acceptable only when all of the following are true:

* the target task exists in `docs/implements_plan.md`
* scope boundaries are defined and safe
* each commit is atomic and terminal-verifiable
* no `TBD` remains
* every unsupported fact has been removed or relabeled
* every AI-added mitigation is labeled `[AI-PROPOSAL]`
* every reversible placeholder is labeled `[ASSUMPTION]`
* no critical `[BLOCKED]` item remains

## Output

* Primary output: `_tasks/$ARGUMENTS.md`
* Expected outcome: an atomic-commit task file with explicit scope boundaries, evidence-backed decomposition, clearly labeled AI-added mitigations where needed, and terminal-verifiable acceptance criteria
