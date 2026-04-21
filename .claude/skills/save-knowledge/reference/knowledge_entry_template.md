<!--
このファイルは /save-knowledge Skill から Read で参照される、
ナレッジエントリの「入力仕様 + ひな形」の単一ソースです。

構成:
  1. Frontmatter スキーマ (必須キー・型・説明)
  2. Markdown テンプレート本体 (コピペして埋める)
  3. 記述ガイド (書き方のコツ)

このファイル以外にスキーマ定義は置かない。後段の
publish_project_knowledge.bat / classify_common_knowledge.bat は
生成後のファイルを扱うだけなので、本ファイルを変更しても
.bat の改修は不要。
-->

# ナレッジエントリ仕様

## 1. Frontmatter スキーマ (すべて必須)

下記キーは **すべて必須**。欠けているか、`TBD` / 空文字 / プレースホルダが
残っている場合は保存してはならない。

| キー | 型 | 内容 |
| --- | --- | --- |
| `schema_version` | int | 固定で `1` |
| `project` | string | プロジェクト名（リポジトリルートのディレクトリ名を既定値とする） |
| `title` | string | 1 行で表現できる事象タイトル（句点なし） |
| `date` | string(YYYY-MM-DD) | 記録日 |
| `tags` | list[string] | 3〜6 個程度。技術領域・症状カテゴリを表す英小文字ケバブ |
| `symptom` | string | 観測された症状を 1〜2 文で |
| `action_taken` | string | 実施した対処を 1〜3 文で |
| `outcome` | string | 対処後の結果を 1〜2 文で（可能なら数値で） |
| `generalizable` | bool | 他プロジェクトでも有用そうなら `true` |
| `confidentiality` | enum | `public` / `internal` / `restricted` のいずれか |

## 2. Markdown テンプレート

以下のブロックをそのままコピーし、`<...>` を埋める。
見出しの構成・順序は変更しない（後段の類型化バッチが前提とする）。

```markdown
---
schema_version: 1
project: <project-name>
title: <1 行タイトル>
date: <YYYY-MM-DD>
tags: [<tag1>, <tag2>, <tag3>]
symptom: <症状>
action_taken: <対処>
outcome: <結果>
generalizable: <true|false>
confidentiality: <public|internal|restricted>
---

# 背景

<何をしていて、どういう状況で起きたか>

# 原因

<判明した原因。推定の場合は「推定」と明記>

# 対処

<実施した作業の具体手順。コマンドや変更ファイルは可能なら引用>

# 結果

<対処後の観測結果。数値があれば数値で>

# 再発防止

<同じ問題を防ぐための設定・運用・監視の提案>
```

## 3. 記述ガイド

- **秘匿値は事前に伏せる**: API key・トークン・パスワード・個人名・顧客固有名は
  そのまま書かず `<REDACTED>` 等で置換する。最終的なマスキングは後段の
  `publish_project_knowledge.bat` が担うが、Skill 段階でも混入させない。
- **原因欄は推定可**: 確定していない場合は「推定:」と明記して書いてよい。
  書かないまま保存するより、根拠付きで推定を残す方が再利用しやすい。
- **対処欄はコマンド単位で**: 変更ファイルパス・実行コマンド・設定キー名を
  具体的に書く。抽象的な「調整した」では再利用不能。
- **結果欄は観測値で**: 「直った」ではなく「p95 が 800ms → 120ms」など、
  事後に検証可能な粒度で残す。
- **`generalizable` の判断**: 特定顧客・特定プロジェクト固有事情が主因なら
  `false`。設定値・再試行方針・運用手順など他所でも通じるなら `true`。
- **`confidentiality`**:
  - `public` — 公開しても問題ない一般技術知見
  - `internal` — 社内共有可。既定値はこれ
  - `restricted` — 特定チームのみ。`publish` でも共有先を制限する想定
- **タグ付け**: `database` / `timeout` / `retry` / `ci` / `deploy` のように
  **技術領域 + 症状カテゴリ**を 3〜6 個。自由作文せず短い単語で。