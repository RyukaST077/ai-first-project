# 実装計画

## タスク形式テンプレート

作業の分解方法に応じて、いずれかのパターンを使用してください。

### 大タスクのみ
- [ ] {{NUMBER}}. {{TASK_DESCRIPTION}}{{PARALLEL_MARK}}
  - {{DETAIL_ITEM_1}} *(詳細が必要な場合のみ記載。タスクが単独で完結する場合は詳細項目を省略)*
  - _要件: {{REQUIREMENT_IDS}}_

### 大タスク + サブタスク構造
- [ ] {{MAJOR_NUMBER}}. {{MAJOR_TASK_SUMMARY}}
- [ ] {{MAJOR_NUMBER}}.{{SUB_NUMBER}} {{SUB_TASK_DESCRIPTION}}{{SUB_PARALLEL_MARK}}
  - {{DETAIL_ITEM_1}}
  - {{DETAIL_ITEM_2}}
  - _要件: {{REQUIREMENT_IDS}}_ *(IDのみを記載。説明文や括弧書きは追加しないこと)*

> **並列マーカー**: 並列実行可能なタスクにのみ ` (P)` を付けてください。`--sequential` モードで実行する場合は省略します。
>
> **任意のテストカバレッジ**: 受け入れ基準に紐づく延期可能なテスト作業の場合、チェックボックスを `- [ ]*` と記載し、詳細項目で参照する要件について説明してください。
