---
name: extension-feature-requirements
description: 既存ソースコードへの追加機能について、対話で要件を確定し、テンプレに沿った確定版指示書を作成する。追加機能の要件定義、曖昧点の解消、受け入れ条件とテスト観点の明確化を行うときに使う。
---

# Extension Feature Requirements

Use this skill to define requirements for an extension feature on top of an existing codebase and produce a finalized design document.

## Required Inputs

- existing source code and current behavior
- user intent for the extension feature
- bundled template: `references/extension_feature_requirements_template.md`
- optional project-local template: `templates/design/extensin_feature/extension_feature_requirements.md`

If repository context is missing, first ask for related modules, current specs, or relevant directory structure.

## Bundled Reference

- Read `references/extension_feature_requirements_template.md` first.
- If `templates/design/extensin_feature/extension_feature_requirements.md` exists, compare it with the bundled template and follow the project-local version when they differ.

## Core Principles

- Do not jump into implementation policy while requirements are still unclear.
- Do not overfill by assumption; ask and confirm.
- Detect ambiguity, contradiction, and unresolved terms, then ask follow-up questions.
- Make acceptance criteria and test viewpoints concrete and verifiable.

## Workflow

1. Start with information-gathering questions and wait for answers.
2. Summarize user responses and reflect only confirmed points into the template.
3. Identify unresolved points, contradictions, and vague wording, then ask focused follow-up questions.
4. Repeat until all required sections are completed.
5. Before finalizing, verify that acceptance criteria and test viewpoints are specific and testable.
6. Output the finalized document to `docs/design/extensin_feature/extension_feature_requirements.md`.

## Response Format Per Turn

In each turn, always include:

A. current understanding (short bullet points)
B. additional questions (priority order, up to 10; prefer yes/no or choice-style)
C. template reflection (delta only for newly confirmed sections)

## Initial Interview Questions

Use these at the first turn (up to 10 questions):

1. What is the extension feature name (tentative is fine), and what is its most important goal?
2. Who are the users or roles of this feature (for example, admin, end user, operator)?
3. What inputs does it receive, and what outputs are expected (UI, API response, file output, etc.)?
4. What trigger starts it (screen action, API call, scheduled timing, etc.)?
5. Which existing areas are affected (new addition, existing modification, or both)?
6. Describe one concrete happy-path example (for example, input A leads to result B).
7. What should happen on failures or exceptions (validation, messages, retry, rollback)?
8. What constraints exist (performance targets, security, permissions, environment, browser support, external integrations, deadline)?
9. What are 2 to 3 acceptance criteria that define done?
10. Can you share existing references (directories, key classes/functions, API specs, screen URLs, current operation steps)?

## Writing Rules

- Never write from guesswork. If evidence is missing in docs, mark it as `要確認`.
- If sources conflict, do not decide unilaterally. List it under `要確認` with source file names.
- At the end of each chapter, list the referenced design document file names.

## Output

- Primary output: `docs/design/extensin_feature/extension_feature_requirements.md`
- Expected outcome: a finalized requirement document with no major ambiguity and testable acceptance criteria