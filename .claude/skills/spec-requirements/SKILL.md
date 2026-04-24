---
name: spec-requirements
description: 要求仕様を確定させる
allowed-tools: Bash, Glob, Grep, LS, Read, Write, Edit, MultiEdit, Update, WebSearch, WebFetch
argument-hint: <feature-name> <design-doc-path>
---

# 要件生成

<background_information>
- **ミッション**: spec 初期化時のプロジェクト説明を基に、EARS 形式で網羅的かつテスト可能な要件を生成する
- **成功条件**:
  - ステアリング文脈と整合した完全な要件文書を作成
  - すべての受け入れ基準で、プロジェクトの EARS パターンと制約に従う
  - 実装詳細を含めず、コア機能に集中
</background_information>

## 引数

本 Skill は以下の 2 引数を**必須**で受け取る前提で動作する:

| 位置 | 意味 | 例 |
|------|------|-----|
| `$1` | 機能名（日本語・英語いずれも可） | `ユーザーログイン` / `user-login` |
| `$2` | 個別設計書のパス | `docs/design/features/user-login.md` |

`$2` が未指定の場合は Phase 冒頭でユーザに確認し、パスを取得してから実行手順へ進む。勝手に `docs/` 配下から推測しない。

`$1` が日本語で渡された場合、Claude は内容を解釈して英語の kebab-case スラッグ（`<spec-name>`）を自動決定する。スラッグは出力先ディレクトリ名に使用するため、英数字とハイフンのみで構成する。

<instructions>

## 主タスク
`docs/design/basic_design.md` のプロジェクト説明と、引数 `$2` で指定された個別設計書を基に、機能 **$1** の完全な要件を生成する。

## 出力

生成した要件定義は次のパスに書き出す:

```
.memory-bank/specs/<spec-name>/requirements.md
```

- `<spec-name>`: `$1` から導出する英語 kebab-case スラッグ（例: `ユーザーログイン` → `user-login`）。Claude が自動決定する。
- 出力ファイルの**書式は `.claude\skills\spec-requirements\reference/requirements.md` に厳密準拠**する（見出し階層・番号付け・プレースホルダ構造を逸脱しない）。
- 親ディレクトリ `.memory-bank/specs/<spec-name>/` が存在しない場合は作成する。
- 出力先に既存ファイルがある場合は**上書き前にユーザへ確認**する（無断で上書きしない）。

## 実行手順

1. **コンテキスト読込**:
   - `docs/design/basic_design.md` を読み、プロジェクト説明を確認
   - 引数 `$2`（個別設計書）を読み、機能に必要な要件を確認
   - `docs/design/**/*.md` を読み必要な情報を確認。
   - **ステアリング文脈をすべて読み込む**: `.memory-bank/steering/` 全体（以下を含む）
     - 既定ファイル: `.memory-bank/steering/productContext.md`, `.memory-bank/steering/projectBrief.md`, `.memory-bank/steering/systemPatterns.md`, `.memory-bank/steering/techContext.md`
     - これにより、完全なプロジェクト記憶と文脈を得る

2. **ガイドライン読込**:
   - `.claude\skills\spec-requirements\reference/ears-format.md` を読み、EARS 構文ルールを確認
   - `.claude\skills\spec-requirements\reference/requirements.md` を読み、文書構造を確認

3. **要件生成**:
   - プロジェクト説明から初期要件を作成
   - 関連機能を論理的な要件領域にグルーピング
   - すべての受け入れ基準に EARS 形式を適用

4. **spec-name 決定と書き出し**:
   - `$1` が日本語なら、内容を解釈して英語 kebab-case スラッグ `<spec-name>` を決定（例: `ユーザーログイン` → `user-login`）
   - 出力先ディレクトリ `.memory-bank/specs/<spec-name>/` を確認・作成
   - 既存の `requirements.md` があれば上書き確認をユーザに取る
   - `.claude\skills\spec-requirements\reference/requirements.md` のテンプレート骨格に要件本文を流し込み、`.memory-bank/specs/<spec-name>/requirements.md` として保存

## 重要な制約
- HOW ではなく WHAT に集中（実装詳細を含めない）
- 要件はテスト可能・検証可能であること
- EARS 文の主語は適切に選択（ソフトウェアでは system/service 名）
- まず初版を生成し、その後ユーザーフィードバックで反復（最初に連続質問しない）
- requirements.md の要件見出しは、先頭に数値 ID を必ず含める（例: "Requirement 1", "1.", "2 Feature ..."）。"Requirement A" のような英字 ID は不可。
- 出力ファイルは `.claude\skills\spec-requirements\reference/requirements.md` の見出し階層・番号付け・プレースホルダ配置を逸脱しない
</instructions>


## 安全性とフォールバック

### エラーシナリオ
- **$2 未指定 / パス不正**: 個別設計書のパスが渡されていない、または存在しない場合は処理を止め、ユーザに正しいパスを確認する（`docs/` 配下を推測で探しに行かない）
- **要件の曖昧さ**: 先に初版を提示し、ユーザーと反復して精緻化（先に多数質問しない）
- **要件の不完全性**: 生成後、期待機能を網羅しているか明示的にユーザーへ確認
- **非数値見出し**: 既存見出しが数値 ID で始まらない場合（例: "Requirement A"）、数値 ID へ正規化し、その対応を一貫して維持（数値と英字を混在させない）
- **出力先既存ファイル**: `.memory-bank/specs/<spec-name>/requirements.md` が既に存在する場合は、差分の要点を提示した上で上書き可否をユーザに確認（自動上書き禁止）
- **spec-name 衝突**: 自動決定したスラッグが既存ディレクトリと衝突する場合は、ユーザに別名を確認

