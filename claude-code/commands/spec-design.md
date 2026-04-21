---
description: 仕様に対する包括的な技術設計を作成する
allowed-tools: Bash, Glob, Grep, LS, Read, Write, Edit, MultiEdit, Update, WebSearch, WebFetch
argument-hint: <feature-name> [-y]
---

# 技術設計ジェネレーター

<background_information>
- **ミッション**: 要件（WHAT）をアーキテクチャ設計（HOW）へ落とし込む、包括的な技術設計ドキュメントを生成する
- **成功条件**:
  - すべての要件が、明確なインターフェースを持つ技術コンポーネントへ対応付けられている
  - 適切なアーキテクチャ調査・リサーチが実施されている
  - 設計がステアリング文脈および既存パターンと整合している
  - 複雑なアーキテクチャには図が含まれている
</background_information>

<instructions>
## 主タスク
承認済み要件を基に、機能 **$1** の技術設計ドキュメントを生成する。

## 実行手順

### ステップ1: コンテキスト読込

**必要なコンテキストをすべて読み込む**:
- `{{KIRO_DIR}}/specs/$1/spec.json`, `requirements.md`, `design.md`（存在する場合）
- **`{{KIRO_DIR}}/.memory-bank/steering/` ディレクトリ全体**（完全なプロジェクト記憶として）
- `{{KIRO_DIR}}/settings/templates/specs/design.md`（文書構造）
- `{{KIRO_DIR}}/settings/rules/design-principles.md`（設計原則）
- `{{KIRO_DIR}}/settings/templates/specs/research.md`（調査ログ構造）

**要件承認を検証**:
- `-y` フラグが指定された場合（$2 == "-y"）: spec.json 内の要件を自動承認
- それ以外: 承認状態を確認（未承認なら停止。Safety & Fallback 参照）

### ステップ2: 調査と分析

**重要: このフェーズは、設計を完全かつ正確な情報に基づかせるためのもの。**

1. **機能タイプを分類**:
   - **新規機能**（グリーンフィールド）→ フル調査が必要
   - **拡張**（既存システム）→ 統合中心の調査
   - **単純追加**（CRUD/UI）→ 最小限または調査不要
   - **複雑統合** → 包括的分析が必要

2. **適切な調査プロセスを実行**:

   **複雑機能／新規機能の場合**:
   - `{{KIRO_DIR}}/settings/rules/design-discovery-full.md` を読み、実行
   - WebSearch/WebFetch で徹底調査:
     - 最新のアーキテクチャパターンとベストプラクティス
     - 外部依存の検証（API、ライブラリ、バージョン、互換性）
     - 公式ドキュメント、移行ガイド、既知問題
     - パフォーマンス指標とセキュリティ考慮

   **拡張の場合**:
   - `{{KIRO_DIR}}/settings/rules/design-discovery-light.md` を読み、実行
   - 統合ポイント、既存パターン、互換性に集中
   - Grep を使って既存コードベースのパターンを分析

   **単純追加の場合**:
   - 形式的な調査はスキップし、簡易パターン確認のみ

3. **Step 3 のために調査結果を保持**:
- 外部 API 契約と制約
- 根拠付きの技術選定
- 踏襲または拡張すべき既存パターン
- 統合ポイントと依存関係
- 特定リスクと緩和策
- 想定アーキテクチャパターンと境界候補（詳細は `research.md` へ）
- 将来タスクの並列化に関する考慮（依存関係を `research.md` に記録）

4. **調査結果を Research Log に永続化**:
- 共有テンプレートを使って `{{KIRO_DIR}}/specs/$1/research.md` を作成または更新
- 調査範囲と主要発見を Summary に記載
- Research Log の各トピックに、情報源と示唆を記録
- テンプレートの各節で、アーキテクチャ評価・設計判断・リスクを記録
- `research.md` の記述言語は spec.json 指定に従う

### ステップ3: 設計ドキュメント生成

1. **設計テンプレートとルールを読み込む**:
- `{{KIRO_DIR}}/settings/templates/specs/design.md`（構造）
- `{{KIRO_DIR}}/settings/rules/design-principles.md`（原則）

2. **設計ドキュメントを生成**:
- **specs/design.md の構造と生成指示を厳密に遵守**
- **すべての調査結果を統合**: 収集した情報（API、パターン、技術）を、コンポーネント定義、設計判断、統合ポイント全体に反映
- Step 1 で既存の design.md が見つかった場合は参照文脈（マージモード）として利用
- 設計ルール（型安全性、視覚的コミュニケーション、フォーマルトーン）を適用
- 記述言語は spec.json 指定に従う
- 章見出し（"Architecture Pattern & Boundary Map", "Technology Stack & Alignment", "Components & Interface Contracts"）の更新を反映し、`research.md` の裏付け詳細を参照

3. **spec.json のメタデータ更新**:
- `phase: "design-generated"` を設定
- `approvals.design.generated: true, approved: false` を設定
- `approvals.requirements.approved: true` を設定
- `updated_at` タイムスタンプを更新

## 重要制約
 - **Type Safety**:
   - プロジェクト技術スタックに沿った強い型付けを徹底する。
   - 静的型付け言語では、明示的な型/インターフェースを定義し、危険なキャストを避ける。
   - TypeScript では `any` を絶対に使わず、正確な型とジェネリクスを優先する。
   - 動的型付け言語では、利用可能な型ヒント/アノテーション（例: Python type hints）を付与し、境界で入力検証を行う。
   - 公開インターフェースと契約を明確に文書化し、コンポーネント横断の型安全性を確保する。
- **最新情報**: 外部依存・ベストプラクティスには WebSearch/WebFetch を利用
- **ステアリング整合**: ステアリング文脈の既存アーキテクチャパターンを尊重
- **テンプレート準拠**: specs/design.md の構造と生成指示を厳密に遵守
- **設計に集中**: アーキテクチャとインターフェースのみ（実装コードは書かない）
- **要件トレーサビリティ ID**: requirements.md で定義された数値 ID（例: "1.1", "1.2", "3.1", "3.3"）のみを正確に使用。新規 ID の創作や英字ラベルの使用は禁止。
</instructions>

## ツールガイダンス
- **Read first**: 実行前に全コンテキスト（spec、steering、templates、rules）を読み込む
- **Research when uncertain**: 外部依存、API、最新ベストプラクティスの不確実性は WebSearch/WebFetch で解消
- **Analyze existing code**: Grep でコードベースのパターンと統合ポイントを調査
- **Write last**: 調査・分析完了後に design.md を生成

## 出力仕様

**コマンド実行出力**（design.md 本文とは別）:

spec.json 指定言語で簡潔に以下を提示:

1. **Status**: `{{KIRO_DIR}}/specs/$1/design.md` に設計文書を生成したことを確認
2. **Discovery Type**: 実行した調査プロセス（full/light/minimal）
3. **Key Findings**: 設計に影響した `research.md` の重要知見を2〜3点
4. **Next Action**: 承認ワークフローの案内（Safety & Fallback 参照）
5. **Research Log**: `research.md` を最新判断で更新したことを確認

**形式**: 簡潔な Markdown（200語未満）。これはコマンド出力であり、設計ドキュメント本文ではない。

**補足**: 実際の設計ドキュメントは `{{KIRO_DIR}}/settings/templates/specs/design.md` 構造に従う。

## 安全性とフォールバック

### エラーシナリオ

**要件未承認**:
- **実行停止**: 承認済み要件なしでは続行不可
- **ユーザーメッセージ**: "Requirements not yet approved. Approval required before design generation."
- **推奨アクション**: "Run `/kiro:spec-design $1 -y` to auto-approve requirements and proceed"

**要件ファイル不足**:
- **実行停止**: 要件ドキュメントが必須
- **ユーザーメッセージ**: "No requirements.md found at `{{KIRO_DIR}}/specs/$1/requirements.md`"
- **推奨アクション**: "Run `/kiro:spec-requirements $1` to generate requirements first"

**Template Missing**:
- **ユーザーメッセージ**: "Template file missing at `{{KIRO_DIR}}/settings/templates/specs/design.md`"
- **推奨アクション**: "Check repository setup or restore template file"
- **Fallback**: 警告付きで基本的なインライン構造を使用

**Steering Context Missing**:
- **警告**: "Steering directory empty or missing - design may not align with project standards"
- **続行**: 生成は続行するが、出力に制約として明記

**Discovery Complexity Unclear**:
- **デフォルト**: フル調査プロセス（`{{KIRO_DIR}}/settings/rules/design-discovery-full.md`）を使用
- **理由**: 重要文脈の取りこぼしより、過剰調査を優先
- **Invalid Requirement IDs**:
  - **実行停止**: requirements.md に数値 ID がない、または非数値見出し（例: "Requirement A"）を使用している場合は停止し、修正を依頼する。

### 次フェーズ: タスク生成

**設計承認済みの場合**:
- 生成物 `{{KIRO_DIR}}/specs/$1/design.md` を確認
- **任意**: `/kiro:validate-design $1` で対話型品質レビューを実施
- その後 `/kiro:spec-tasks $1 -y` で実装タスクを生成

**修正が必要な場合**:
- フィードバックを反映し `/kiro:spec-design $1` を再実行
- 既存 design.md は参照文脈（マージモード）として利用

**補足**: タスク生成へ進む前に、設計承認は必須。
