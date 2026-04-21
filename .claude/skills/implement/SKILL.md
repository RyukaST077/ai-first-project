---
name: implement
description: Use this skill to implement commit tasks listed in a task list one at a time in numeric order. Starting from `tasks.md` or `task_list.md`, review the referenced design documents, check progress, investigate the existing implementation, compare against the design, make the smallest necessary changes, validate the result, perform an independent review, and update the task list. When appropriate, use subagents to split investigation, design comparison, and validation work, while keeping final judgment and integration under the parent agent.
argument-hint: Please specify the path to the task list, for example: `tasks.md` or `task_list.md`

---

# Implement

## Core Rules

1. Process commit tasks one at a time in numeric order. Do not skip any task.
2. Only one commit task may be considered in progress for completion at a time. Do not implement multiple `C-XXX` tasks in parallel.
3. However, **within a single commit task**, you may delegate investigation, design comparison, impact analysis, validation planning, and independent review to subagents.
4. Do not redo commit tasks that are already complete.
5. Before starting, always check progress and resume from the smallest incomplete `C-XXX`.
6. Before implementation, always review the referenced design document(s) for that commit task.
7. As a rule, keep changes limited to the smallest scope necessary for the target task.
8. Prioritize requirements explicitly written in the referenced design document(s). If they differ from the existing implementation, identify and handle the gap explicitly.
9. Read the style of the existing code first, then follow it.
10. Even if there are uncertainties, do not stop. Make the smallest necessary assumptions and continue.
11. Group changes into units that can pass build and test.
12. After completing a task, update the completion check in `$ARGUMENTS` according to its existing notation.
13. Implement IDs and constants from the design documents exactly as written, including case and symbols.
14. Treat subagent output as reference material. **The parent agent is responsible for adoption decisions, implementation integration, completion judgment, and updating `$ARGUMENTS`.**
15. If subagent results conflict, resolve them using this priority order: **design documents > actual implementation > task list wording > inference**.
16. Use subagents to improve quality and speed, but do not let delegation increase scope, duplicate effort, or weaken accountability.

## Subagent Policy

### Purpose

- The parent agent owns responsibility for completing the target commit task.
- Subagents help divide investigation, comparison, and validation work inside a single commit task.
- The processing order of commit tasks must not be changed.

### Work that may be delegated to subagents

- Extracting requirements from referenced design documents
- Exploring the existing implementation
- Identifying impact scope
- Investigating existing coding patterns
- Checking mismatches and inconsistencies
- Listing test perspectives
- Performing independent post-implementation review
- Organizing viewpoints around logs, exceptions, DB, ORM, APIs, and config differences

### Work that must not be delegated to subagents

- Deciding which `C-XXX` to start
- Running multiple commit tasks in parallel
- Making the final implementation decision
- Final integration of code changes
- Updating `$ARGUMENTS`
- Judging task completion
- Adopting implementation decisions that conflict with the design documents

### When subagents should be used

Use subagents where appropriate if any of the following apply:

- There are multiple referenced design documents
- Investigation of existing implementation patterns is needed
- The impact spans multiple directories or layers
- Differences between design and implementation need to be checked
- There are many test perspectives or regression risks
- It is safer to separate pre-implementation review and post-implementation review

You do not need to force subagent use for small changes such as:

- A clear change within a single file
- A constant change that requires no investigation
- A simple extension of an existing pattern

### Subagent orchestration rules

- Use at most **2 to 3 subagents** for a single commit task unless the scope is clearly large.
- Assign **non-overlapping roles** to subagents whenever possible.
- Recommended role split:
  - **Design reviewer**: extracts requirements, constraints, and acceptance criteria from the design documents
  - **Code investigator**: inspects existing implementation patterns, related files, and impact scope
  - **Validation reviewer**: checks test coverage, regression risk, and acceptance-criteria alignment after implementation
- Do not assign multiple subagents to perform the same investigation unless there is a clear reason.
- Before moving from **Step 2 to Step 3**, the parent agent must consolidate subagent findings and fix the implementation scope.
- Before moving from **Step 5 to Step 6**, the parent agent must consolidate validation findings and resolve conflicts.
- Do not use subagents for trivial single-file edits or obvious pattern-copy changes.
- If delegation creates more coordination cost than implementation benefit, the parent agent should continue without subagents.

### Request format for subagents

At minimum, provide the following to each subagent:

- Target task ID
- Task objective
- Referenced design document(s)
- Files or directories to inspect
- Expected deliverable
- Prohibited actions
- How evidence should be shown

Example requests:

- `Extract requirements, constraints, and acceptance criteria from the design documents for C-012`
- `Investigate existing implementation patterns related to C-012 by controller / usecase / repository`
- `Review the implementation diff for C-012 independently against the acceptance criteria`

### Return format for subagents

#### Investigation-oriented

- Investigation target
- Files reviewed
- Confirmed facts
- Inferences
- Unconfirmed points
- Recommended actions

#### Design-comparison-oriented

- Requirement list
- Constraint list
- Acceptance criteria
- Gaps from the existing implementation
- Implementation cautions

#### Validation-oriented

- Expected tests
- Boundary cases
- Failure cases
- Regression risks
- Missing checks

### How to handle subagent results

- Separate facts from inferences
- Do not adopt weakly supported conclusions
- If results conflict, the parent agent must re-check the design documents and code to resolve them
- Even if uncertainty remains, the parent agent should proceed using the smallest reasonable assumption
- The parent agent must summarize the adopted conclusions before implementation and before completion judgment

## Startup Procedure

### 1. Progress Check

At the start, always do the following:

- Read `$ARGUMENTS` and classify each `C-XXX` as `Complete / Incomplete / Unknown`
- Review the referenced design document(s) for each `C-XXX` and summarize the objective, constraints, and acceptance criteria
- Check the branch, diff, related files, and test status to detect inconsistencies between `$ARGUMENTS` and the actual implementation state
- If inconsistencies exist, resolve them with the minimum necessary evidence such as file presence or diffs

Rules for choosing the starting commit task:

- As a rule, start from the smallest incomplete `C-XXX`
- If implementation is already done but not checked off, update the check first with evidence, then move on
- If any task has unknown status, start there to determine its state
- Do not break numeric order

### 2. `$ARGUMENTS` Correction

- If an unchecked item is clearly complete, mark it complete with evidence
- If an item is checked but incomplete, keep the check as-is, leave a note about the inconsistency, and start from that task

### 3. Initial Delegation Planning

After selecting the target `C-XXX`, do the following if needed:

- Delegate requirement extraction from the design documents to a subagent
- Delegate investigation of existing implementation patterns to a subagent
- Delegate impact analysis to a subagent
- Delegate validation planning to a subagent if regression risk is non-trivial
- The parent agent must then integrate the results and determine the final implementation scope

## How to Process Each Commit Task

As a rule, process each task in the following order.

### Step 1. Review the Referenced Design Documents

- Before implementation, always read the design document(s) linked to the commit task
- Extract the scope, requirements, constraints, acceptance criteria, and any IDs or constants first
- If there is a gap between the existing implementation and the design, organize it as an explicit issue at this stage
- If needed, you may delegate the following to subagents:
  - Requirement extraction
  - Constraint extraction
  - Gap identification against the existing implementation
  - Acceptance criteria organization
- The parent agent must integrate the extracted results and determine the conditions that must be satisfied in this task

### Step 2. Pre-Implementation Check

- Summarize the task objective and success condition in 1 to 3 lines
- Summarize the relevant design document sections and the requirements that this implementation must satisfy
- State the evidence that the task is incomplete, or the evidence that it is already complete and can be skipped
- If it is already complete, only update `$ARGUMENTS` and move to the next task
- Investigate and organize the following:
  - Package structure
  - Naming rules
  - Exception design
  - Logging policy
  - DB and ORM policy
  - Test policy
- List the implementation points and impact scope related to the design documents
- If needed, you may delegate the following to subagents:
  - Investigation of existing implementation style
  - Identification of related files
  - Listing of impact scope
  - Confirmation of incompleteness evidence
- Before proceeding to Step 3, the parent agent must consolidate the findings and lock the target scope for this task

### Step 3. Implementation Plan

- Summarize design decisions in bullet points
  - Mapping to the referenced design documents
  - Data model, interfaces, and domain design
  - Exceptions, validation, and transactions
  - Consistency with existing APIs and DB
- If there are decision points, write alternatives and the reason for the chosen option
- If there are major risks, write mitigations
- The parent agent must make the final implementation decision
- If needed, only the comparison of alternatives may be delegated to a subagent, but the adoption decision must not be delegated

### Step 4. Changes

- Show changes in a way that makes the diff clear for each modified file
- Show full contents for new files
- Keep configuration and SQL aligned with the existing environment-difference policy
- Add the following only when necessary and only in the minimum scope:
  - Migrations or DDL
  - Dependencies
  - Exceptions or error responses
  - README or API specifications
- If the implementation is large, you may ask subagents to help with file-level investigation or diff review
- However, final integration of the changes must be done by the parent agent
- Do not expand the scope beyond what was fixed in Step 2 and Step 3 unless a blocking issue is found

### Step 5. Validation Procedure

- Write commands for local build, test, run, lint, format, and similar checks
- Write the expected result and what to observe
- When necessary, also check boundary values, failure cases, performance, concurrency, and compatibility
- If needed, you may delegate the following to subagents:
  - Identifying missing test perspectives
  - Organizing checks against acceptance criteria
  - Reviewing regression risks
- Before proceeding to Step 6, the parent agent must consolidate validation findings and resolve open conflicts

### Step 6. Self-Check Against Acceptance Criteria

- For each acceptance criterion, mark `✅ / ❌`
- Briefly state the basis for the judgment
- If possible, add an independent review by a subagent that did not perform the implementation
- In the independent review, check the following:
  - Missed acceptance criteria
  - Overlooked design-document mismatches
  - Missing impact scope
  - Insufficient testing
- The final judgment must be made by the parent agent

## When a Task Is Complete

Include the following when necessary:

- Summary of the commit task
- Notes for reviewers
- Handover memo for the next task
- `$ARGUMENTS` update result
- Summary integrating subagent results
- Assumptions made in this task and why they were reasonable

## Exit Conditions

- All commit tasks are complete and `$ARGUMENTS` has been updated
- Or there are no incomplete tasks and consistency of `$ARGUMENTS` has been confirmed

## Startup Instructions for Claude Code

When this skill is used, proceed in the following order:

1. First, perform the progress check and declare which `C-XXX` should be started
2. Read the referenced design document(s) for that task before implementation
3. If needed, delegate requirement extraction, existing implementation investigation, impact analysis, and validation planning to subagents
4. The parent agent integrates the subagent results and finalizes the implementation plan for that task
5. Complete the following for that task: `Step 1. Review the Referenced Design Documents → Step 2. Pre-Implementation Check → Step 3. Implementation Plan → Step 4. Changes → Step 5. Validation Procedure → Step 6. Self-Check`
6. After completion, update `$ARGUMENTS` and move to the next `C-XXX`
7. If all tasks are complete, finish with the consistency check result