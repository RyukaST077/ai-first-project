---
name: init-memory-bank
description: .memory-bank/steering を初期化するためのスキル。プロジェクトのドキュメントを読み込み、.memory-bank/steering 内のファイルを更新する。
disable-model-invocation: true
---


## 目的
- Clineのための `.memory-bank/steering` を初期化する
- `.memory-bank/` が存在しないプロジェクトでも、本 Skill に同梱したテンプレートから初期化できるようにする

## 前提
- 本 Skill は `reference/steering-templates/` に 4 種の雛形を同梱している:
  - `projectBrief.md` / `productContext.md` / `techContext.md` / `systemPatterns.md`

## 手順
1. `.memory-bank/steering/` が存在しなければ作成する（`mkdir -p .memory-bank/steering`）
1. `docs/design/**/*.md` を読み込む
1. 以下の 4 ファイルそれぞれについて同じ処理を行う:
   - `projectBrief.md`
   - `productContext.md`
   - `techContext.md`
   - `systemPatterns.md`

   各ファイルの処理:
   1. `.memory-bank/steering/<file>` が存在しなければ、本 Skill の `reference/steering-templates/<file>` をコピーして初期配置する
   1. `.memory-bank/steering/<file>` を読み込み、必要なセクションを把握する
   1. `docs/design/**/*.md` を唯一の情報源として `.memory-bank/steering/<file>` を更新する
