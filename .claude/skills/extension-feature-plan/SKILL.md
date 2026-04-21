---
name: extension-feature-plan
description: 既存コードに追加機能を導入するため、`templates/extension_feature_plan.md` と `docs/` をもとに `docs/implements_plan.md` を作成・更新する。既存実装調査、影響範囲、依存関係、モック方針、フェーズ別計画、リスク、変更履歴の整理に使う。

---

# Extension Feature Plan

Use this skill to create or update `docs/implements_plan.md` for an extension feature on top of an existing codebase.

## Required Inputs

- bundled reference: `references/extension_feature_plan_template.md`
- project-local template: `templates/extension_feature_plan.md` if it exists
- design and specification files under `docs/`
- existing `docs/implements_plan.md` if it already exists
- current repository structure and relevant source code

## Bundled Reference

- Read `references/extension_feature_plan_template.md` first to understand the required output structure.
- If the repository also has `templates/extension_feature_plan.md`, compare it with the bundled reference and follow the project-local version when they differ.
- If the feature also has requirements/design docs such as `docs/design/extensin_feature/extension_feature_requirements.md`, use them as evidence when drafting the plan.

## Workflow

1. Read `references/extension_feature_plan_template.md` and identify the required sections and structure.
2. If `templates/extension_feature_plan.md` exists in the repository, compare it with the bundled reference and follow the project-local version when they differ.
3. Inspect the files under `docs/` and identify which documents can be used as evidence.
4. Inspect the existing source code to identify architecture patterns, dependencies, tests, database schema, and API surfaces relevant to the feature.
5. If `docs/implements_plan.md` already exists, review the current content and compare before overwriting it.
6. Draft or update `1. 概要` from the design documents and existing implementation evidence.
7. Draft or update `2. 開発の進め方（チーム戦略）` from the design documents and existing implementation evidence.
8. Draft or update `3. 影響範囲と依存関係` from the design documents and existing implementation evidence.
9. Draft or update `4. モック方針` from the design documents and existing implementation evidence.
10. Draft or update `5. フェーズ別 実装計画` from the design documents and existing implementation evidence.
11. Draft or update `6. リスクと対策` from the design documents and existing implementation evidence.
12. Record the current creation or update timestamp in the change history and complete `7. 変更履歴`.
13. Save the finished plan to `docs/implements_plan.md`.

## Writing Rules

- Do not write from guesswork. If the evidence is not present in `docs/` or the source code, mark it as `要確認`.
- If the documents conflict, do not resolve the conflict by assumption. Add the issue to `要確認` and cite the source file names.
- At the end of each chapter, list the design document file names and source code file names used for that chapter.
- Keep the plan grounded in the existing documents and the repository's actual implementation patterns.
- Give highest priority to identifying regression risk and the scope of existing behavior that could be affected.
- Distinguish new functionality from modifications to existing functionality.
- Treat destructive database changes or impacts to existing data with caution.
- Verify existing tests and document the regression coverage expectation.

## Output

- Primary output: `docs/implements_plan.md`
- Expected outcome: a project-wide implementation plan aligned with the template and supported by the documents and codebase
