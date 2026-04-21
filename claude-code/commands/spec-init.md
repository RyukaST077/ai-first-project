---
description: 詳細なプロジェクト説明から新しい仕様を初期化する
allowed-tools: Bash, Read, Write, Glob
argument-hint: <project-description>
---

# 仕様初期化

<background_information>
- **ミッション**: 新しい仕様のディレクトリ構造とメタデータを作成し、仕様駆動開発の最初のフェーズを初期化する
- **成功条件**:
  - プロジェクト説明から適切な feature 名を生成
  - 競合しない一意な spec 構造を作成
  - 次フェーズ（要件生成）への明確な導線を提示
</background_information>

<instructions>
## 主タスク
プロジェクト説明（$ARGUMENTS）から一意な feature 名を生成し、仕様構造を初期化する。

## 実行手順
1. **一意性確認**: `{{KIRO_DIR}}/specs/` の命名衝突を確認（必要なら数値サフィックスを付与）
2. **ディレクトリ作成**: `{{KIRO_DIR}}/specs/[feature-name]/`
3. **テンプレートから初期ファイル作成**:
   - `{{KIRO_DIR}}/settings/templates/specs/init.json` を読む
   - `{{KIRO_DIR}}/settings/templates/specs/requirements-init.md` を読む
   - プレースホルダーを置換:
     - `{{FEATURE_NAME}}` → 生成した feature 名
     - `{{TIMESTAMP}}` → 現在の ISO 8601 タイムスタンプ
     - `{{PROJECT_DESCRIPTION}}` → $ARGUMENTS
   - spec ディレクトリへ `spec.json` と `requirements.md` を書き込む

## 重要な制約
- この段階で requirements/design/tasks は生成しない
- フェーズごとの開発原則を遵守
- フェーズ分離を厳密に維持
- 本フェーズでは初期化のみ実行
</instructions>

## ツールガイダンス
- **Glob** で既存 spec ディレクトリを確認し、命名の一意性を担保
- **Read** でテンプレート `init.json` と `requirements-init.md` を取得
- **Write** で置換後の `spec.json` と `requirements.md` を作成
- いかなる書き込み前にも検証を実施

## 出力仕様
`spec.json` 指定言語で、次の構成で出力する:

1. **生成した Feature 名**: `feature-name` 形式と、1〜2文の根拠
2. **プロジェクト要約**: 1文で簡潔に
3. **作成ファイル**: フルパスの箇条書き
4. **次のステップ**: `/kiro:spec-requirements <feature-name>` をコードブロックで表示
5. **補足**: 初期化のみ実施した理由（フェーズ分離）を2〜3文で説明

**形式要件**:
- Markdown 見出し（##, ###）を使用
- コマンドはコードブロックにする
- 全体を簡潔に（250語未満）
- `spec.json.language` に従った明確でプロフェッショナルな文体

## 安全性とフォールバック
- **曖昧な Feature 名**: 生成が難しい場合は2〜3案を提示し、ユーザーに選択してもらう
- **テンプレート欠如**: `{{KIRO_DIR}}/settings/templates/specs/` の不足ファイルを明示し、リポジトリ設定確認を促す
- **ディレクトリ競合**: 既存名と重複時は `feature-name-2` のように数値サフィックスを付与し、自動解決を通知
- **書き込み失敗**: 失敗パスを示し、権限またはディスク容量を確認するよう案内
