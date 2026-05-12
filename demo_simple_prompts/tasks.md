## 目的

requirements.md / design.md から、実行可能な実装タスクを生成する。

## 成功条件

* 要件IDとタスクが1:1対応
* サブタスク粒度は1〜3時間
* 階層は最大2（メジャー＋サブ）
* 順序は Foundation → Core → Integration → Validation
* 並列可能タスクに (P)
* 自然言語で「何をするか」のみ記述

## 入力

* $1: 機能名（日本語OK → kebab-case自動生成）

## 出力

.memory-bank/specs/<spec-name>/tasks.md

---

## Phase 0: 読み込み・検証

* 読み込み:

  * spec.json / requirements.md / design.md / tasks.md（あれば）
  * steering 全体 / テンプレート / reference
* spec-name 自動決定
* 異常時停止:

  * requirements/design 不在
  * 要件IDが数値でない

---

## Phase 1: タスク生成
テンプレートに従ってタスクを生成

### テンプレート
```
# Implementation Plan

## Task Format Template

Use whichever pattern fits the work breakdown:

### Major task only
- [ ] {{NUMBER}}. {{TASK_DESCRIPTION}}{{PARALLEL_MARK}}
  - {{DETAIL_ITEM_1}} *(Include details only when needed. If the task stands alone, omit bullet items.)*
  - _Requirements: {{REQUIREMENT_IDS}}_

### Major + Sub-task structure
- [ ] {{MAJOR_NUMBER}}. {{MAJOR_TASK_SUMMARY}}
- [ ] {{MAJOR_NUMBER}}.{{SUB_NUMBER}} {{SUB_TASK_DESCRIPTION}}{{SUB_PARALLEL_MARK}}
  - {{DETAIL_ITEM_1}}
  - {{DETAIL_ITEM_2}}
  - {{OBSERVABLE_COMPLETION_ITEM}} *(At least one detail item should state the observable completion condition for this task.)*
  - _Requirements: {{REQUIREMENT_IDS}}_ *(IDs only; do not add descriptions or parentheses.)*
  - _Boundary: {{COMPONENT_NAMES}}_ *(Only for (P) tasks. Omit when scope is obvious.)*
  - _Depends: {{TASK_IDS}}_ *(Only for non-obvious cross-boundary dependencies. Most tasks omit this.)*

> **Parallel marker**: Append ` (P)` only to tasks that can be executed in parallel. Omit the marker when running in `--sequential` mode.
>
> **Optional test coverage**: When a sub-task is deferrable test work tied to acceptance criteria, mark the checkbox as `- [ ]*` and explain the referenced requirements in the detail bullets.
```
---

## Phase 2: レビュー

### Coverage

* 全要件IDが登場するか
* 全コンポーネントが対応しているか

### Executability

* 1〜3時間で実行可能か
* 完了条件があるか
* 複雑すぎる場合は分割

最大2回修正。不可なら停止。

---

## Phase 3: 出力

### tasks.md

* テンプレート準拠
* 既存はマージ上書き

---

## 制約

* 要件IDは数値のみ
* 並列は (P) を番号直後
* Boundaryは(P)のみ必須
* 最大2階層
* すべて統合可能であること

---

## 出力ログ

* タスク数
* 要件カバー率
* 並列数
* 品質チェック結果
