---
description: 仕様の包括的な要件を生成する
allowed-tools: Bash, Glob, Grep, LS, Read, Write, Edit, MultiEdit, Update, WebSearch, WebFetch
argument-hint: <feature-name>
---

# 要件生成

<background_information>
- **ミッション**: spec 初期化時のプロジェクト説明を基に、EARS 形式で網羅的かつテスト可能な要件を生成する
- **成功条件**:
  - ステアリング文脈と整合した完全な要件文書を作成
  - すべての受け入れ基準で、プロジェクトの EARS パターンと制約に従う
  - 実装詳細を含めず、コア機能に集中
  - 生成状態を追跡するメタデータを更新
</background_information>

<instructions>
## 主タスク
`requirements.md` のプロジェクト説明を基に、機能 **$1** の完全な要件を生成する。

## 実行手順

1. **コンテキスト読込**:
   - `{{KIRO_DIR}}/specs/$1/spec.json` を読み、言語とメタデータを確認
   - `{{KIRO_DIR}}/specs/$1/requirements.md` を読み、プロジェクト説明を確認
   - **ステアリング文脈をすべて読み込む**: `.memory-bank/steering/` 全体（以下を含む）
     - 既定ファイル: `structure.md`, `tech.md`, `product.md`
     - モード設定に関係なく、すべてのカスタム steering ファイル
     - これにより、完全なプロジェクト記憶と文脈を得る

2. **ガイドライン読込**:
   - `{{KIRO_DIR}}/settings/rules/ears-format.md` を読み、EARS 構文ルールを確認
   - `{{KIRO_DIR}}/settings/templates/specs/requirements.md` を読み、文書構造を確認

3. **要件生成**:
   - プロジェクト説明から初期要件を作成
   - 関連機能を論理的な要件領域にグルーピング
   - すべての受け入れ基準に EARS 形式を適用
   - 記述言語は spec.json 指定に従う

4. **メタデータ更新**:
   - `phase: "requirements-generated"` を設定
   - `approvals.requirements.generated: true` を設定
   - `updated_at` タイムスタンプを更新

## 重要な制約
- HOW ではなく WHAT に集中（実装詳細を含めない）
- 要件はテスト可能・検証可能であること
- EARS 文の主語は適切に選択（ソフトウェアでは system/service 名）
- まず初版を生成し、その後ユーザーフィードバックで反復（最初に連続質問しない）
- requirements.md の要件見出しは、先頭に数値 ID を必ず含める（例: "Requirement 1", "1.", "2 Feature ..."）。"Requirement A" のような英字 ID は不可。
</instructions>

## ツールガイダンス
- **最初に読み込む**: 生成前に全コンテキスト（spec、steering、rules、templates）を読み込む
- **最後に書き込む**: 生成完了後に requirements.md を更新
- 外部ドメイン知識が必要な場合のみ **WebSearch/WebFetch** を使用

## 出力仕様
spec.json 指定言語で以下を出力:

1. **生成要件サマリー**: 主要な要件領域を簡潔に（3〜5項目）
2. **文書状態**: requirements.md 更新と spec.json メタデータ更新を確認
3. **次のステップ**: 承認して次へ進むか、修正するかを案内

**形式要件**:
- 可読性のため Markdown 見出しを使用
- ファイルパスはコードブロックで記載
- サマリーは簡潔に（300語未満）

## 安全性とフォールバック

### エラーシナリオ
- **プロジェクト説明不足**: requirements.md に説明がない場合、機能詳細をユーザーへ確認
- **要件の曖昧さ**: 先に初版を提示し、ユーザーと反復して精緻化（先に多数質問しない）
- **テンプレート欠如**: テンプレートがない場合、警告付きでインライン構造を使用
- **言語未定義**: spec.json に言語指定がなければ英語（`en`）を既定にする
- **要件の不完全性**: 生成後、期待機能を網羅しているか明示的にユーザーへ確認
- **steering ディレクトリ空**: プロジェクト文脈不足が品質へ影響し得ることを警告
- **非数値見出し**: 既存見出しが数値 ID で始まらない場合（例: "Requirement A"）、数値 ID へ正規化し、その対応を一貫して維持（数値と英字を混在させない）

### 次フェーズ: 設計生成

**要件承認済みの場合**:
- `{{KIRO_DIR}}/specs/$1/requirements.md` の生成要件を確認
- **任意のギャップ分析**（既存コードベース向け）:
  - `/kiro:validate-gap $1` を実行し、既存実装とのギャップを分析
  - 既存コンポーネント、統合ポイント、実装方針を特定
  - ブラウンフィールドで推奨、グリーンフィールドでは省略可
- その後 `/kiro:spec-design $1 -y` で設計フェーズへ

**修正が必要な場合**:
- フィードバックを反映し `/kiro:spec-requirements $1` を再実行

**補足**: 設計フェーズへ進むには承認が必須。
