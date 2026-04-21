# AI-DLC と仕様駆動開発

AI-DLC（AI Development Life Cycle）上での Kiro 形式 Spec Driven Development 実装。

## プロジェクト文脈

### パス
- Steering: `.memory-bank/steering/`
- Specs: `{{KIRO_DIR}}/specs/`

### Steering と仕様

**Steering** (`.memory-bank/steering/`) - プロジェクト横断のルールと文脈で AI をガイド
**Specs** (`{{KIRO_DIR}}/specs/`) - 個別機能の開発プロセスを形式化

### アクティブ仕様
- `{{KIRO_DIR}}/specs/` を確認してアクティブ仕様を把握
- `/kiro:spec-status [feature-name]` で進捗確認

## 開発ガイドライン
{{DEV_GUIDELINES}}

## 最小ワークフロー
- Phase 0（任意）: `/kiro:steering`, `/kiro:steering-custom`
- Phase 1（仕様）:
  - `/kiro:spec-init "description"`
  - `/kiro:spec-requirements {feature}`
  - `/kiro:validate-gap {feature}`（任意: 既存コードベース向け）
  - `/kiro:spec-design {feature} [-y]`
  - `/kiro:validate-design {feature}`（任意: 設計レビュー）
  - `/kiro:spec-tasks {feature} [-y]`
- Phase 2（実装）: `/kiro:spec-impl {feature} [tasks]`
  - `/kiro:validate-impl {feature}`（任意: 実装後）
- 進捗確認: `/kiro:spec-status {feature}`（いつでも実行可）

## 開発ルール
- 3段階承認フロー: Requirements → Design → Tasks → Implementation
- 各フェーズで人手レビュー必須。`-y` は意図的な高速化時のみ使用
- steering を最新に保ち、`/kiro:spec-status` で整合確認
- ユーザー指示に正確に従い、その範囲で自律的に行動する: 必要な文脈を収集し、この実行内で依頼作業を端から端まで完了する。必須情報が欠ける、または指示が重大に曖昧な場合にのみ質問する。

## Steering 設定
- `.memory-bank/steering/` 全体をプロジェクト記憶として読み込む
- 既定ファイル: `product.md`, `tech.md`, `structure.md`
- カスタムファイルをサポート（`/kiro:steering-custom` で管理）
