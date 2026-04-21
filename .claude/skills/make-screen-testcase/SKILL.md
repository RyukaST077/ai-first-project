---
name: make-screen-testcase
description: 指定された画面名について、`docs/` 配下の設計資料とテストテンプレートをもとに画面テスト計画書を作成する。画面単位のテスト観点整理、対象機能と対象外の明確化、テスト項目一覧、テストデータ、注意事項、リスク整理を行い、`docs/test/screen/screen_test_<画面名>.md` を出力するときに使う。
argument-hint: 画面設計書を指定してください。例: `screen1.md` や `screen2.md`

---

# Make Screen Testcase

Use this skill to create a screen test plan document for a specified screen.

## Required Inputs

- target screen name from the user request
- bundled reference: `references/single_test_plan_template.md`
- project-local template: `templates/single_test_plan_template.md` if it exists
- repository documents under `docs/**/*.md`
- design documents under `docs/design/**/*.md`
- fallback converted design documents under `convert2md_scripts/converted_md_design/**/*.md` when the needed information is not present in `docs/design/**/*.md`

## Bundled Reference

- Read `references/single_test_plan_template.md` first to understand the required output structure.
- If the repository has `templates/single_test_plan_template.md`, compare it with the bundled reference and follow the project-local template when they differ.

## Workflow

1. Read `references/single_test_plan_template.md` and identify the required sections and tables.
2. If `templates/single_test_plan_template.md` exists, compare it with the bundled reference and follow the project-local template when they differ.
3. Search `docs/**/*.md` and `docs/design/**/*.md` for the target screen name, screen ID, related business flow, validation rules, permissions, and external dependencies.
4. If the required information is still missing, search `convert2md_scripts/converted_md_design/**/*.md` and use only the minimum necessary facts from there.
5. Identify the screen purpose, main functions, in-scope features, out-of-scope features, environment assumptions, and test viewpoints from the gathered evidence.
6. Draft the test categories and test cases for the target screen. Remove unused template sections and add new categories only when the screen needs them.
7. Draft the test data, caution points, and risks based on the actual screen behavior, validation rules, permissions, and integrations described in the documents.
8. Save the finished document to `docs/test/screen/screen_test_<画面名>.md`.

## Writing Rules

- Replace every `{{ }}` placeholder with project-specific content. Do not leave unresolved placeholders in the final file unless the information is genuinely unavailable.
- If evidence is unavailable, write `要確認` instead of guessing.
- If multiple documents conflict, do not resolve the conflict by assumption. Record the item as `要確認` and cite the source file names.
- Remove unnecessary chapters, sections, categories, rows, and example text from the template.
- Add categories, test cases, and viewpoints when the target screen requires them.
- Adjust test item numbering to the project's numbering convention when such a convention is present in the documents.
- Keep the test plan focused on the specified screen. Do not broaden it into a system-wide or feature-wide plan unless the documents show that the screen cannot be tested independently.
- At the end of each major chapter, list the document file names used as evidence when practical.

## Output

- Primary output: `docs/test/screen/screen_test_<画面名>.md`
- Expected outcome: a screen-specific test plan aligned with the template and supported by repository documents
