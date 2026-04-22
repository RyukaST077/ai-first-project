---
name: spec-impl
description: 承認済みの spec（requirements.md / design.md / tasks.md）に基づき、TDD（Red-Green-Refactor）手法で tasks.md の未完了タスクを実行し、チェックボックスを `- [x]` に更新するスキル。ユーザが「タスクを実装して」「TDD で仕様タスクを実行」「/spec-impl」「未完了タスクを進めて」などと言った場合に起動する。
allowed-tools: Bash, Read, Write, Edit, MultiEdit, Grep, Glob, LS, WebFetch, WebSearch
argument-hint: <feature-name> [task-numbers]
---

# 実装タスク実行（TDD）

<background_information>
- **ミッション**: 承認済み仕様に基づき、テスト駆動開発（TDD）手法で tasks.md の実装タスクを実行する
- **成功条件**:
  - 実装コードより前にすべてのテストを記述している
  - コードが全テストを通過し、回帰を起こしていない
  - tasks.md 上で実行したタスクが `- [x]` に更新されている
  - 実装が design.md / requirements.md と整合している
</background_information>

## 引数

| 位置 | 意味 | 例 |
|------|------|-----|
| `$1` | 機能名（spec-name。日本語・英語いずれも可） | `ユーザーログイン` / `user-login` |
| `$2` | 実行対象タスク番号（任意。カンマ or 単一） | `1.1` / `1,2,3` |

- `$1` が日本語なら、Claude が英語 kebab-case スラッグ `<spec-name>` を自動決定する（`spec-requirements` / `spec-design` / `spec-tasks` と同じ規則）。
- `$2` 省略時は `tasks.md` の未完了（`- [ ]`）タスクをすべて実行する。

## 入出力

```
.memory-bank/specs/<spec-name>/
├── requirements.md  # 要件（入力）
├── design.md        # 設計（入力）
└── tasks.md         # 実行対象。完了マークで更新
```

<instructions>

## 主タスク

機能 **$1** について、TDD サイクルで `tasks.md` の実装タスクを実行し、完了マークを更新する。

---

## 実行手順

### Phase 0: コンテキスト読込・前提検証

**1. コンテキスト一括読込**（並列 Read 可）:

- `.memory-bank/specs/<spec-name>/requirements.md`
- `.memory-bank/specs/<spec-name>/design.md`
- `.memory-bank/specs/<spec-name>/tasks.md`
- `.memory-bank/steering/` 全体(プロジェクト記憶として)

**2. spec-name 決定**:

- `$1` が日本語なら Claude が英語 kebab-case スラッグ `<spec-name>` を自動決定

**3. 前提検証**:

- `requirements.md` / `design.md` / `tasks.md` がすべて存在することを確認
- いずれかが不足している場合は **停止**（Safety & Fallback 参照）

---

### Phase 1: タスク選択

- `$2` が指定された場合: 指定されたタスク番号を実行（例: `1.1` 単体、`1,2,3` 複数）
- `$2` 未指定の場合: `tasks.md` の未完了（`- [ ]`）タスクをすべて実行
- 実行順序は tasks.md の記載順（Foundation → Core → Integration → Validation）に従う

---

### Phase 2: TDD で実行

選択した各タスクについて、Kent Beck の TDD サイクルを厳守する:

**1. RED — 失敗するテストを書く**
- 次に実装する最小単位に対するテストを書く
- テストは失敗する（コードがまだ存在しないため）
- 説明的なテスト名を用いる

**2. GREEN — 最小限のコードを書く**
- そのテストを通過させる最もシンプルな実装を書く
- 「このテスト」を通すことだけに集中する（過剰設計禁止）

**3. REFACTOR — 整理する**
- コード構造と可読性を改善
- 重複を取り除き、適切な箇所でデザインパターンを適用
- リファクタ後も全テストが通過することを保証

**4. VERIFY — 品質を検証する**
- すべてのテスト（新規・既存）が通過
- 既存機能に回帰がない
- コードカバレッジが維持または改善されている

**5. 完了マーク**
- `tasks.md` の該当タスクのチェックボックスを `- [ ]` → `- [x]` に更新

---

## 重要な制約

- **TDD 必須**: 実装コードより先にテストを書く（順序違反は禁止）
- **タスク範囲**: 当該タスクが要求する範囲のみ実装（スコープ外変更禁止）
- **テストカバレッジ**: すべての新規コードはテストを持つ
- **回帰禁止**: 既存テストは継続して通過しなければならない
- **設計整合**: 実装は `design.md` の仕様に従う
- **要件整合**: 実装は `_Requirements:_` で紐付く要件 ID をすべて満たす

</instructions>

## ツールガイダンス

- **最初に読み込む**: 実装前に spec / steering をすべてロード
- **最初にテスト**: コードより先にテストを書く
- **WebSearch/WebFetch**: 必要に応じてライブラリドキュメント参照に使用

## 出力仕様

日本語で簡潔に報告:

1. **実行タスク**: タスク番号と TDD 各サイクルの結果、テスト結果
2. **状態**: `tasks.md` に反映した完了タスク一覧、残タスク件数

**形式**: 簡潔（150 語未満）

## 安全性とフォールバック

### エラーシナリオ

**仕様ファイル不足**:
- 実行停止
- メッセージ: 「`.memory-bank/specs/<spec-name>/` に requirements.md / design.md / tasks.md のいずれかが存在しません」
- 推奨: 「先に前フェーズを完了してください: `/spec-requirements` → `/spec-design` → `/spec-tasks`」

**テスト失敗**:
- 実装停止（REFACTOR / 次タスクに進まない）
- アクション: 失敗しているテストをデバッグして修正し、GREEN を再確立してから進める

**既存テストの回帰検出**:
- 該当タスクの変更を見直し、回帰を解消するまで次タスクに進まない
- 解消困難な場合は停止し、ユーザへ設計見直し or `/spec-design` への差し戻しを提案

### タスク実行の呼び出し例

- `/spec-impl <feature> 1.1` — 単一タスク
- `/spec-impl <feature> 1,2,3` — 複数タスク
- `/spec-impl <feature>` — 未完了タスクをすべて実行（コンテキスト肥大化のため非推奨）

### 推奨運用

- タスクごとに会話コンテキストをクリアし、新鮮な状態で集中する
- 複数タスクをまとめて実行する場合も、各タスク完了後にコミット粒度で区切る
