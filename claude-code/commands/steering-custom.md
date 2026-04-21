---
description: 専門領域向けのカスタム steering ドキュメントを作成する
allowed-tools: Bash, Read, Write, Edit, MultiEdit, Glob, Grep, LS
---

# Kiro カスタム Steering 作成

<background_information>
**役割**: コアファイル（product, tech, structure）以外の専門 steering ドキュメントを作成する。

**ミッション**: 特定領域向けのプロジェクト記憶を、ユーザーが作成できるよう支援する。

**成功条件**:
- カスタム steering が専門パターンを適切に保持する
- コア steering と同じ粒度原則に従う
- 特定ドメインに対する明確な価値を提供する
</background_information>

<instructions>
## ワークフロー

1. **ユーザーに確認**:
   - 対象ドメイン/トピック（例: "API standards", "testing approach"）
   - 文書化したい具体要件・パターン

2. **テンプレートの有無確認**:
   - `{{KIRO_DIR}}/settings/templates/steering-custom/{name}.md` があれば読み込む
   - 出発点として使い、プロジェクトに合わせて調整

3. **コードベースを分析（JIT 戦略）**:
   - 関連ファイルを **Glob** で探索
   - 既存実装を **Read** で確認
   - 特定パターンを **Grep** で抽出

4. **カスタム steering を生成**:
   - テンプレートがあればその構造に従う
   - `{{KIRO_DIR}}/settings/rules/steering-principles.md` の原則を適用
   - 網羅リストではなくパターン中心
   - 100〜200行（2〜3分で読める量）を目安

5. **ファイル作成**:
   - `{{KIRO_DIR}}/.memory-bank/steering/{name}.md` に作成

## 利用可能テンプレート

`{{KIRO_DIR}}/settings/templates/steering-custom/` にあるテンプレート:

1. **api-standards.md** - REST/GraphQL 規約、エラーハンドリング
2. **testing.md** - テスト構成、モック、カバレッジ
3. **security.md** - 認証パターン、入力検証、シークレット管理
4. **database.md** - スキーマ設計、マイグレーション、クエリパターン
5. **error-handling.md** - エラー種別、ログ、リトライ戦略
6. **authentication.md** - 認証フロー、権限、セッション管理
7. **deployment.md** - CI/CD、環境、ロールバック手順

必要時にテンプレートを読み、プロジェクト向けに調整する。

## Steering 原則

`{{KIRO_DIR}}/settings/rules/steering-principles.md` より:

- **列挙よりパターン**: すべてを列挙せず、パターンを文書化
- **単一ドメイン**: 1ファイル1トピック
- **具体例重視**: コード例でパターンを示す
- **保守可能なサイズ**: 目安は100〜200行
- **セキュリティ最優先**: 秘密情報・機微データは記載しない

</instructions>

## ツールガイダンス

- **Read**: テンプレート読込、既存コード分析
- **Glob**: パターン分析向け関連ファイル探索
- **Grep**: 特定パターン検索
- **LS**: 関連構造の把握

**JIT 戦略**: 必要なタイプの steering を作る時だけテンプレートを読む。

## 出力仕様

チャット要約のみ（ファイルは直接作成）。

```
✅ カスタム Steering を作成しました

## 作成ファイル:
- {{KIRO_DIR}}/.memory-bank/steering/api-standards.md

## 参照元:
- テンプレート: api-standards.md
- 分析対象: src/api/ ディレクトリのパターン
- 抽出内容: REST 規約、エラー形式

## 内容:
- エンドポイント命名パターン
- リクエスト/レスポンス形式
- エラーハンドリング規約
- 認証アプローチ

必要に応じて確認・カスタマイズしてください。
```

## 例

### 成功例: API 標準
**入力**: 「API 標準の steering を作成して」  
**アクション**: テンプレート読込、src/api/ を分析、パターン抽出  
**出力**: プロジェクト固有の REST 規約を含む api-standards.md

### 成功例: テスト戦略
**入力**: 「テスト方針を文書化して」  
**アクション**: テンプレート読込、テストファイル分析、パターン抽出  
**出力**: テスト構成とモック戦略をまとめた testing.md

## 安全性とフォールバック

- **テンプレートなし**: ドメイン知識ベースでゼロから生成
- **セキュリティ**: 秘密情報は記載しない（原則を参照）
- **重複回避**: コア steering 内容との重複を防ぐ

## 注記

- テンプレートは出発点であり、プロジェクトに合わせて調整する
- 粒度はコア steering と同じ原則に従う
- すべての steering ファイルはプロジェクト記憶として読み込まれる
- カスタムファイルはコアと同等に重要
- エージェント固有ツールディレクトリ（例: `.cursor/`, `.gemini/`, `.claude/`）は文書化しない
- `{{KIRO_DIR}}/specs/` と `{{KIRO_DIR}}/.memory-bank/steering/` の軽い参照は可。他の `.kiro/` ディレクトリへの言及は避ける
