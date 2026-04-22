---
name: spec-orchestrate
description: 承認済み `requirements.md` を起点に、`spec-design` → `spec-tasks` → `spec-impl` の3スキルをサブエージェントで直列オーケストレーションし、技術設計・タスク生成・TDD 実装までを一気通貫で完遂するスキル。ユーザが「設計からタスク実装まで通しで走らせて」「spec を最後まで進めて」「/spec-orchestrate」などと言った場合に起動する。
allowed-tools: Bash, Glob, Grep, LS, Read, Write, Edit, Task
argument-hint: <feature-name> [start-phase] [task-numbers]
---

# Spec パイプライン オーケストレータ

<background_information>
- **ミッション**: 承認済み要件を起点に、技術設計 → 実装タスク生成 → TDD 実装の 3 段を無人で走破させる
- **戦略**: 各フェーズは独立サブエージェントに委譲し、親エージェントはオーケストレーションとゲートチェックのみ担当する。これにより親コンテキストを肥大化させず、フェーズ間の汚染を防ぐ
- **対象スキル**（すべて既存）:
  1. `.claude/skills/spec-design/SKILL.md` — 技術設計
  2. `.claude/skills/spec-tasks/SKILL.md` — 実装タスク生成
  3. `.claude/skills/spec-impl/SKILL.md` — TDD 実装
- **直列実行が必須**: spec-tasks は `design.md` を入力、spec-impl は `tasks.md` を入力するため、段を飛ばしたり並列化したりはしない
- **成功条件**:
  - `.memory-bank/specs/<spec-name>/` 配下に `design.md` / `tasks.md` が生成済み
  - `tasks.md` の実行対象タスクが `- [x]` 済
  - 各フェーズの要約が親から一括報告されている
</background_information>

## 引数

| 位置 | 意味 | 例 |
|------|------|-----|
| `$1` | 機能名（日本語・英語いずれも可） | `ユーザーログイン` / `user-login` |
| `$2` | 開始フェーズ（任意）。`design` / `tasks` / `impl` のいずれか。既定 `design` | `tasks` |
| `$3` | `spec-impl` 用の task 番号（任意）。省略時は未完了全件 | `1.1` / `1,2,3` |

- `$1` が日本語なら親エージェントが英語 kebab-case スラッグ `<spec-name>` を自動決定し、サブエージェントへ明示的に渡す
- `$2` を使うと中断・再開が可能（例: design/tasks 済みで impl だけ再実行）
- **前提**: `requirements.md` は人間により承認済みで `.memory-bank/specs/<spec-name>/` に存在する

## 入出力

```
.memory-bank/specs/<spec-name>/
├── spec.json           # 各サブエージェントが更新
├── requirements.md     # 入力（このスキルでは生成しない）
├── gap-analysis.md     # Phase 1 (spec-design) 生成物
├── research.md         # Phase 1 (spec-design) 生成物
├── design.md           # Phase 1 (spec-design) 生成物
├── tasks.md            # Phase 2 (spec-tasks) 生成物／Phase 3 で更新
└── <実装コード>         # Phase 3 (spec-impl) 生成物
```

<instructions>

## 主タスク

機能 **$1** について、`spec-design` → `spec-tasks` → `spec-impl` を順に無人実行し、各フェーズの成果物を検証しつつ最終結果を統合報告する。

---

## Phase 0: 前提検証（親エージェント）

**1. spec-name 決定**:

- `$1` が日本語なら英語 kebab-case スラッグ `<spec-name>` を決定
- 以降、全サブエージェントへ決定済みの `<spec-name>` を明示的に渡す（サブエージェント側で再決定させない）

**2. 入力存在チェック**（並列 Read / LS）:

- `.memory-bank/specs/<spec-name>/requirements.md` が存在すること
- `requirements.md` に数値 ID があること（英字ラベル "Requirement A" 等が混入していないこと）
- `$2 == impl` の場合は `design.md` と `tasks.md` も必須
- `$2 == tasks` の場合は `design.md` も必須

**3. 対象スキルの SKILL.md 読込**:

- `.claude/skills/spec-design/SKILL.md`
- `.claude/skills/spec-tasks/SKILL.md`
- `.claude/skills/spec-impl/SKILL.md`

親はこれらの手順を把握した上でサブエージェント用プロンプトへ転写する（サブエージェントは本会話のコンテキストを知らないため、必要事項はプロンプトに自己完結で記載する）。

**4. 失敗時**:

- 必須ファイル不在 → 停止し、`/spec-requirements <feature>` などの前工程を案内

---

## Phase 1: 技術設計（サブエージェント委譲）

**起動条件**: `$2` が `design` もしくは未指定。

**サブエージェント呼び出し**（`Task` ツール、`subagent_type: general-purpose`）:

- `description`: `spec-design pipeline for <spec-name>`
- `prompt`（自己完結で記載）:
  > あなたは `.claude/skills/spec-design/SKILL.md` を厳密に実行する担当エージェントです。まず当該 SKILL.md を Read し、その `<instructions>` に従って機能 **`<spec-name>`**（元引数: `$1`）について Phase 0〜4 を無人で完走させてください。成果物は `.memory-bank/specs/<spec-name>/{gap-analysis.md, research.md, design.md}` と `spec.json` 更新です。SKILL.md 内で並列起動が指示されているサブエージェントはあなた自身が起動してください（Task ツールを使用）。完了時は以下を 300 語以内で親へ報告してください: (a) 生成ファイルパス一覧、(b) 採用アーキテクチャ要点、(c) Phase 4 の GO/NO-GO と根拠、(d) 未決事項・リスク受容事項。

**親エージェントのゲートチェック**:

- `.memory-bank/specs/<spec-name>/design.md` が存在・非空であることを Read で確認
- サブエージェント報告から Phase 4 判定を抽出
- **NO-GO** の場合: 親は停止し、サブエージェント報告をそのままユーザへ提示（再実行の判断はユーザに委ねる）
- **GO** の場合: Phase 2 へ進む

---

## Phase 2: 実装タスク生成（サブエージェント委譲）

**起動条件**: Phase 1 GO、かつ `$2` が `design` / `tasks` / 未指定。

**サブエージェント呼び出し**:

- `description`: `spec-tasks pipeline for <spec-name>`
- `prompt`:
  > あなたは `.claude/skills/spec-tasks/SKILL.md` を厳密に実行する担当エージェントです。まず当該 SKILL.md を Read し、その `<instructions>` に従って機能 **`<spec-name>`** について Phase 0〜3 を無人で完走させてください。入力は `.memory-bank/specs/<spec-name>/{requirements.md, design.md}`、出力は `tasks.md` と `spec.json` 更新です。完了時は以下を 200 語以内で親へ報告してください: (a) `tasks.md` パス、(b) メジャー／サブタスク件数と `(P)` 件数、(c) 要件 ID カバレッジ、(d) レビューゲート結果。

**親エージェントのゲートチェック**:

- `.memory-bank/specs/<spec-name>/tasks.md` が存在・非空であることを Read で確認
- 先頭 100 行程度を Read し、`- [ ]` 形式の未完了タスクが存在することを確認
- 生成失敗時は停止し、サブエージェント報告をそのままユーザへ提示

---

## Phase 3: TDD 実装（サブエージェント委譲）

**起動条件**: Phase 2 成功、かつ `$2` が `design` / `tasks` / `impl` / 未指定。

**サブエージェント呼び出し**:

- `description`: `spec-impl TDD for <spec-name>`
- `prompt`（`$3` が指定されていれば明記）:
  > あなたは `.claude/skills/spec-impl/SKILL.md` を厳密に実行する担当エージェントです。まず当該 SKILL.md を Read し、その `<instructions>` に従って機能 **`<spec-name>`** の tasks.md を TDD（Red-Green-Refactor-Verify）で実行してください。対象タスク: `<$3 もしくは "未完了の全タスク">`。実装ごとに tasks.md のチェックボックスを `- [x]` へ更新すること。完了時は以下を 200 語以内で親へ報告してください: (a) 実行したタスク番号一覧と TDD 各サイクル要点、(b) 新規・既存テストの合否、(c) 回帰有無、(d) `tasks.md` の残タスク件数。

**親エージェントのゲートチェック**:

- `.memory-bank/specs/<spec-name>/tasks.md` を再 Read し、指定タスク（もしくは既存の `- [ ]` タスク）が `- [x]` へ更新されていることを確認
- テスト失敗・回帰検出のまま終了していれば停止し、サブエージェント報告を添えてユーザへ提示

---

## Phase 4: 統合レポート（親エージェント）

3 フェーズの報告を統合し、`spec.json` 指定言語（未指定なら日本語）で以下を出力:

1. **完了フェーズ**: 実行した Phase とスキップした Phase
2. **生成／更新成果物**: ファイルパス一覧
3. **設計サマリ**: Phase 1 の GO 根拠・採用アーキテクチャ要点
4. **タスクサマリ**: メジャー／サブタスク件数、`(P)` 件数、要件 ID カバレッジ
5. **実装サマリ**: 実行済みタスク、テスト合否、残タスク件数
6. **次アクション**: 残タスクの継続実行コマンド（`/spec-orchestrate <feature> impl <次番号>` 等）

**形式**: 簡潔な Markdown（全体 500 語未満）。

---

## 重要な制約

- **直列実行**: 3 スキルは依存関係により並列化しない。並列はあくまで各スキル内部の調査サブエージェントに限る
- **1 スキル = 1 サブエージェント**: 各フェーズは独立サブエージェントで実行し、親コンテキストを保護する
- **サブエージェントは自己完結**: プロンプトに `<spec-name>`、対象 SKILL.md パス、期待成果物、報告フォーマットを必ず明示する（親の会話文脈には依存させない）
- **ゲート不通過は停止**: 前フェーズの成果物が欠落／不正なら次フェーズへ進めない
- **既存成果物の扱い**: 各サブスキルの「自動上書き」ポリシーに従う。親では再確認しない
- **ユーザ確認は取らない**: 全フェーズ無人連続実行。NO-GO・失敗時のみ停止して報告
- **`$2` による部分実行**: `tasks` 指定なら Phase 1 をスキップし Phase 2〜3、`impl` 指定なら Phase 3 のみ実行
- **成果物の書込みは各サブスキルが行う**: 親は Read / LS による検証と統合報告のみ

</instructions>

## ツールガイダンス

- **Task**: 各フェーズ 1 回ずつ、`subagent_type: general-purpose` で起動。3 フェーズ直列のため**並列起動しない**
- **Read / LS**: 各ゲートチェックで成果物の存在と大まかな内容を確認
- **Bash**: 必要に応じ `ls` / `git status` 等で状態確認（破壊的操作は禁止）
- **他の書込みツール**: 親は原則使わない。成果物の編集はサブエージェントに委ねる

## 安全性とフォールバック

### エラーシナリオ

**`requirements.md` 不在** (Phase 0):
- 停止。`/spec-requirements <feature>` の実行を案内

**要件 ID が不正** (Phase 0):
- 停止。`/spec-requirements <feature>` で数値 ID へ正規化するよう案内

**Phase 1 が NO-GO**:
- 停止。サブエージェントの Critical Issues と Next Steps をそのままユーザへ提示。ユーザ判断後の再実行を待つ

**Phase 2 でカバレッジ不足等により spec ギャップ差し戻し**:
- 停止。`/spec-requirements` / `/spec-design` のいずれへ戻るべきかをサブエージェント報告から抽出して提示

**Phase 3 でテスト失敗／回帰**:
- 停止。失敗テストと原因候補をそのまま提示。ユーザが設計見直しを選ぶ場合は `/spec-orchestrate <feature> design` での再入口を案内

**サブエージェント自体が失敗 / 例外終了**:
- 親エージェントは残フェーズを起動しない
- 取得できた部分報告と停止理由を Phase 4 レポート形式でユーザへ提示

### 部分再実行の呼び出し例

- `/spec-orchestrate <feature>` — design から全通し
- `/spec-orchestrate <feature> tasks` — design スキップ、tasks と impl を実行
- `/spec-orchestrate <feature> impl 1.1` — impl のみ、タスク 1.1 を TDD 実行
- `/spec-orchestrate <feature> impl 1,2,3` — impl のみ、複数タスク

### 推奨運用

- `impl` を通しで走らせる場合でもコンテキスト肥大を避けるため、本スキル自体をタスク単位で再実行することを推奨
- 大規模機能では Phase 1 完了後に一旦停止し、人間が `design.md` を確認してから `/spec-orchestrate <feature> tasks` で続行する運用も可能
