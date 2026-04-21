---
name: init-memory-bank
description: .memory-bank/steering を初期化するためのスキル。プロジェクトのドキュメントを読み込み、.memory-bank/steering 内のファイルを更新する。
disable-model-invocation: true
---


## 目的
- Clineのための `.memory-bank/steering` を初期化する

## 手順
1. `docs/design/**/*.md` を読み込む
1. `.memory-bank/steering/projectBrief.md` を読み込み、必要なセクションを把握。
1. `docs/design/**/*.md` を唯一の情報源として `.memory-bank/steering/projectBrief.md` を更新
1. `.memory-bank/steering\productContext.md` を読み込み、必要なセクションを把握。
1. `docs/design/**/*.md` を唯一の情報源として `.memory-bank/steering\productContext.md` を更新
1. `.memory-bank/steering\techContext.md` を読み込み、必要なセクションを把握。
1. `docs/design/**/*.md` を唯一の情報源として `.memory-bank/steering\techContext.md` を更新
1. `.memory-bank/steering\systemPatterns.md` を読み込み、必要なセクションを把握。
1. `docs/design/**/*.md` を唯一の情報源として `.memory-bank/steering\systemPatterns.md` を更新
