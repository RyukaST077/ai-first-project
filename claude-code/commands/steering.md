---
description: {{KIRO_DIR}}/.memory-bank/steering/ を永続的なプロジェクト知識として管理する
allowed-tools: Bash, Read, Write, Edit, MultiEdit, Glob, Grep, LS
---

# Kiro Steering 管理

<background_information>
**役割**: `{{KIRO_DIR}}/.memory-bank/steering/` を永続的なプロジェクト記憶として維持する。

**ミッション**:
- Bootstrap: コードベースからコア steering を生成（初回）
- Sync: steering とコードベースの整合を維持（保守）
- Preserve: ユーザーカスタマイズを尊重し、更新は追加的に行う

**成功条件**:
- steering が網羅リストではなくパターンと原則を捉えている
- コードとのドリフトを検出して報告できる
- `{{KIRO_DIR}}/.memory-bank/steering/*.md` をコア/カスタム問わず同等に扱う
</background_information>

<instructions>
## シナリオ判定

`{{KIRO_DIR}}/.memory-bank/steering/` の状態を確認:

**Bootstrap モード**: 空、またはコアファイル（product.md, tech.md, structure.md）が不足  
**Sync モード**: すべてのコアファイルが存在

---

## Bootstrap フロー

1. `{{KIRO_DIR}}/settings/templates/steering/` からテンプレートを読み込む
2. コードベースを分析（JIT）:
   - ソースファイルを `glob_file_search` で探索
   - README, package.json などを `read_file` で確認
   - `grep` でパターン抽出
3. パターンを抽出（列挙ではない）:
   - プロダクト: 目的、価値、コア機能
   - 技術: フレームワーク、意思決定、規約
   - 構造: 構成、命名、インポート
4. steering ファイルを生成（テンプレート準拠）
5. `{{KIRO_DIR}}/settings/rules/steering-principles.md` の原則を読み込む
6. レビュー用サマリーを提示

**焦点**: ファイル/依存のカタログではなく、意思決定を導くパターン。

---

## Sync フロー

1. 既存 steering（`{{KIRO_DIR}}/.memory-bank/steering/*.md`）をすべて読み込む
2. コードベースの変更を分析（JIT）
3. ドリフトを検出:
   - **Steering → コード**: 欠落要素 → 警告
   - **コード → Steering**: 新規パターン → 更新候補
   - **カスタムファイル**: 関連性を確認
4. 更新案を提示（追加的更新、既存ユーザー内容を保持）
5. 報告: 更新内容、警告、推奨事項

**更新方針**: 置換ではなく追加。ユーザー記述を保持する。

---

## 粒度原則

`{{KIRO_DIR}}/settings/rules/steering-principles.md` より:

> 「新しいコードが既存パターンに従うなら、steering の更新は不要であるべき」

網羅リストではなく、パターンと原則を文書化する。

**悪い例**: ディレクトリツリーの全ファイル列挙  
**良い例**: 具体例付きで構成パターンを説明

</instructions>

## ツールガイダンス

- `glob_file_search`: ソース/設定ファイル探索
- `read_file`: steering、ドキュメント、設定を読む
- `grep`: パターン検索
- `list_dir`: 構造分析

**JIT 戦略**: 必要なタイミングで取得し、先読みし過ぎない。

## 出力仕様

チャット要約のみ（ファイル更新は直接実施）。

### Bootstrap:
```
✅ Steering を作成しました

## 生成ファイル:
- product.md: [簡潔な説明]
- tech.md: [主要スタック]
- structure.md: [構成]

信頼できる情報源として確認・承認してください。
```

### Sync:
```
✅ Steering を更新しました

## 変更内容:
- tech.md: React 18 → 19
- structure.md: API パターンを追加

## コードドリフト:
- インポート規約に従っていないコンポーネント

## 推奨事項:
- api-standards.md の追加を検討
```

## 例

### Bootstrap
**入力**: 空の steering、React TypeScript プロジェクト  
**出力**: 「Feature-first」「TypeScript strict」「React 19」などのパターンを含む3ファイル

### Sync
**入力**: 既存 steering と新しい `/api` ディレクトリ  
**出力**: structure.md を更新、規約逸脱を警告、api-standards.md を提案

## 安全性とフォールバック

- **セキュリティ**: キー/パスワード/秘密情報は記載しない（原則参照）
- **不確実性**: 両方の可能性を報告し、ユーザー確認を取る
- **保全性**: 迷ったら置換せず追加更新

## 注記

- `{{KIRO_DIR}}/.memory-bank/steering/*.md` はすべてプロジェクト記憶として読み込まれる
- テンプレートと原則は外部カスタマイズ可能
- 焦点はカタログ化ではなくパターン化
- 「黄金律」: 既存パターンに沿う新規コードなら steering 更新は不要
- エージェント固有ツールディレクトリ（例: `.cursor/`, `.gemini/`, `.claude/`）は文書化しない
- `{{KIRO_DIR}}/settings/` は steering に記録しない（設定はメタデータであり、プロジェクト知識ではない）
- `{{KIRO_DIR}}/specs/` と `{{KIRO_DIR}}/.memory-bank/steering/` の軽い参照は可。他の `.kiro/` ディレクトリへの言及は避ける
