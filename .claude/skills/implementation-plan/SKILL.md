---
name: implementation-plan
description: Create or update `docs/implements_plan.md` from `templates/implements_plan.md` and the project design documents in `docs/`. Use this when the user asks for a project-wide implementation plan, team development strategy, dependency ordering, mock policy, phased implementation plan, rough role split, risk analysis, or change history grounded in existing documentation.
---

# Implementation Plan

Use this skill to produce a project-wide implementation plan in `docs/implements_plan.md`.

## Required Inputs

- bundled template: `references/implements_plan_template.md`
- design and specification files under `docs/`
- existing `docs/implements_plan.md` if it already exists

## Bundled Reference

- Read `references/implements_plan_template.md` first to understand the required output structure.
- If the repository also has `templates/implements_plan.md`, treat it as the project-local source of truth and compare it with the bundled template before writing.

## Workflow

1. Read `references/implements_plan_template.md` and identify the required sections and structure.
2. If `templates/implements_plan.md` exists in the repository, compare it with the bundled template and follow the project-local version when they differ.
3. Inspect the files under `docs/` and identify which documents can be used as evidence.
4. If `docs/implements_plan.md` already exists, review the current content and compare before overwriting it.
5. Draft or update `1. 概要` from the design documents in `docs/`.
6. Draft or update `2. 開発の進め方（チーム戦略）` from the design documents in `docs/`.
7. Draft or update `3. 依存関係の整理（最重要）` from the design documents in `docs/`.
8. Draft or update `4. モック方針（遷移先がスコープ外/未実装の場合）` from the design documents in `docs/`.
9. Draft or update `5. フェーズ別 実装計画（セットアップ〜リリースまで）` from the design documents in `docs/`.
10. In `Phase 2: データベーススキーマ完成`, create the plan as `1 table = 1 task`. Expand the table to match the number of tables in scope.
11. Draft or update `6. 役割分担（ざっくり）` from the design documents in `docs/`.
12. Draft or update `7. リスクと対策` from the design documents in `docs/`.
13. Record the current creation or update timestamp in the change history and complete `8. 変更履歴`.
14. Save the finished plan to `docs/implements_plan.md`.

## Writing Rules

- Do not write from guesswork. If the evidence is not present in `docs/`, mark it as `要確認`.
- If the documents conflict, do not resolve the conflict by assumption. Add the issue to `要確認` and cite the source file names.
- At the end of each chapter, list the design document file names used for that chapter.
- Keep the plan grounded in the existing documents and template structure.
- In `Phase 2`, do not create broad cross-table tasks. Represent schema work at table granularity, with one task per table.

## Output

- Primary output: `docs/implements_plan.md`
- Expected outcome: a project-wide implementation plan aligned with the template and supported by the documents in `docs/`
