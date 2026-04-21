---
description: 仕様の実装タスクを生成する
allowed-tools: Read, Write, Edit, MultiEdit, Glob, Grep
argument-hint: <feature-name> [-y] [--sequential]
---

# 実装タスクジェネレーター

<background_information>
- **ミッション**: 技術設計を実行可能な作業項目へ変換する、詳細かつ実行可能な実装タスクを生成する
- **成功条件**:
  - すべての要件が具体的なタスクへ対応付けられている
  - タスク粒度が適切（各 1〜3 時間）
  - 階層と順序が明確なタスク進行
  - 実装能力に焦点を当てた自然言語記述
</background_information>

<instructions>
## 主タスク
承認済みの requirements と design を基に、機能 **$1** の実装タスクを生成する。

## 実行手順

### ステップ1: コンテキスト読込

**必要なコンテキストをすべて読み込む**:
- `{{KIRO_DIR}}/specs/$1/spec.json`, `requirements.md`, `design.md`
- `{{KIRO_DIR}}/specs/$1/tasks.md`（存在する場合、マージモードの参照）
- **`{{KIRO_DIR}}/.memory-bank/steering/` ディレクトリ全体**（完全なプロジェクト記憶として）

**承認を検証**:
- `-y` フラグ指定時（$2 == "-y"）: spec.json の requirements/design を自動承認
- それ以外: 両方承認済みか検証（未承認なら停止。Safety & Fallback 参照）
- `--sequential` の有無で sequential mode を判定

### ステップ2: 実装タスク生成

**生成ルールとテンプレートを読み込む**:
- `{{KIRO_DIR}}/settings/rules/tasks-generation.md`（原則）
- `sequential` が **false** の場合: `{{KIRO_DIR}}/settings/rules/tasks-parallel-analysis.md`（並列判断基準）
- `{{KIRO_DIR}}/settings/templates/specs/tasks.md`（`(P)` マーカー対応フォーマット）

**すべてのルールに従ってタスクリストを生成**:
- 記述言語は spec.json 指定に従う
- すべての要件をタスクへ対応付ける
- 要件カバレッジ記載時は、数値要件 ID のみをカンマ区切りで列挙（説明サフィックス、括弧、翻訳、自由ラベルは不可）
- 設計コンポーネントを漏れなく含める
- タスク進行が論理的かつ段階的であることを検証
- 単一サブタスク構造はメジャータスクへ昇格し、入れ物だけのメジャータスクに詳細を重複記載しない（テンプレートパターンに従う）
- 並列条件を満たすタスクに `(P)` マーカーを付与（sequential mode では省略）
- 任意のテストカバレッジサブタスクは、MVP 後に延期可能かつコア実装で受け入れ基準が満たされる場合のみ `- [ ]*` を使用
- 既存 tasks.md がある場合は新内容とマージ

### ステップ3: Finalize

**書き込みと更新**:
- `{{KIRO_DIR}}/specs/$1/tasks.md` を作成または更新
- spec.json のメタデータを更新:
  - `phase: "tasks-generated"`
  - `approvals.tasks.generated: true, approved: false`
  - `approvals.requirements.approved: true`
  - `approvals.design.approved: true`
  - `updated_at` タイムスタンプ更新

## 重要制約
- **ルール厳守**: tasks-generation.md の原則はすべて必須
- **自然言語**: コード構造ではなく「何をするか」を記述
- **完全網羅**: すべての要件をタスクへ対応付ける
- **最大 2 階層**: メジャータスクとサブタスクのみ（それ以上は不可）
- **連番維持**: メジャータスクは 1,2,3... と増分、重複不可
- **統合性**: すべてのタスクはシステムに接続される（孤立作業を作らない）
</instructions>

## ツールガイダンス
- **Read first**: 生成前にコンテキスト・ルール・テンプレートを読み込む
- **Write last**: 分析と検証完了後に tasks.md を生成

## 出力仕様

spec.json 指定言語で簡潔に報告:

1. **Status**: `{{KIRO_DIR}}/specs/$1/tasks.md` にタスクを生成したことを確認
2. **Task Summary**:
   - 合計: X 件のメジャータスク、Y 件のサブタスク
   - Z 件の要件をすべてカバー
   - サブタスク平均サイズ: 1〜3 時間
3. **Quality Validation**:
   - ✅ すべての要件がタスクに対応
   - ✅ タスク依存関係を検証
   - ✅ テストタスクを含む
4. **Next Action**: タスク確認後の次ステップを案内

**形式**: 簡潔（200語未満）

## 安全性とフォールバック

### エラーシナリオ

**要件または設計が未承認**:
- **実行停止**: requirements と design が承認済みでなければ続行不可
- **ユーザーメッセージ**: "Requirements and design must be approved before task generation"
- **推奨アクション**: "Run `/kiro:spec-tasks $1 -y` to auto-approve both and proceed"

**要件または設計ファイル不足**:
- **実行停止**: 両ドキュメントが必須
- **ユーザーメッセージ**: "Missing requirements.md or design.md at `{{KIRO_DIR}}/specs/$1/`"
- **推奨アクション**: "Complete requirements and design phases first"

**要件カバレッジ不足**:
- **警告**: "Not all requirements mapped to tasks. Review coverage."
- **ユーザー対応**: 意図的なギャップか確認、または再生成

**Template/Rules Missing**:
- **ユーザーメッセージ**: "Template or rules files missing in `{{KIRO_DIR}}/settings/`"
- **Fallback**: 警告付きで基本的なインライン構造を使用
- **推奨アクション**: "Check repository setup or restore template files"
- **Missing Numeric Requirement IDs**:
  - **実行停止**: requirements.md の全要件に数値 ID が必要。欠落があれば生成を停止し、修正を依頼する。

### 次フェーズ: 実装

**実装開始前**:
- **重要**: `/kiro:spec-impl` 実行前に会話履歴をクリアし、コンテキストを解放する
- 初回タスク開始時・タスク切り替え時のいずれも適用
- 新鮮なコンテキストにより、クリーンな状態と適切なタスク集中を確保

**タスク承認済みの場合**:
- 特定タスク実行: `/kiro:spec-impl $1 1.1`（推奨: タスクごとに文脈クリア）
- 複数タスク実行: `/kiro:spec-impl $1 1.1,1.2`（慎重に使用。間で文脈クリア）
- 引数なし: `/kiro:spec-impl $1`（未完了全実行。文脈肥大化のため非推奨）

**修正が必要な場合**:
- フィードバックを反映し `/kiro:spec-tasks $1` を再実行
- 既存 tasks は参照文脈（マージモード）として利用

**補足**: 実装フェーズでは、適切な文脈と検証でタスク実行をガイドする。
