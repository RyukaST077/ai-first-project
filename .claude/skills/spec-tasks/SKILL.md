---
name: spec-tasks
description: 承認済みの requirements.md と design.md から、実装タスクリスト（tasks.md）を生成するスキル。要件とすべてのコンポーネントを 1〜3 時間粒度の自然言語タスクへ落とし込み、並列実行可能なタスクには `(P)` マーカーを付与する。ユーザが「タスク一覧を作って」「実装タスクを生成」「tasks.md を作成」などと言った場合に起動する。
allowed-tools: Bash, Glob, Grep, LS, Read, Write, Edit, MultiEdit
argument-hint: <feature-name>
---

# 実装タスクジェネレーター

<background_information>
- **ミッション**: 技術設計を実行可能な作業項目へ変換する、詳細かつ実行可能な実装タスクを生成する
- **成功条件**:
  - すべての要件（数値 ID）が具体的なタスクへ 1:1 で対応付けられている
  - サブタスク粒度が適切（各 1〜3 時間）
  - 階層（最大 2 階層）と順序（Foundation → Core → Integration → Validation）が明確
  - 並列実行可能なタスクに `(P)` マーカーが付与されている
  - 自然言語で「何をするか」を記述（実装詳細・ファイル名・関数名は書かない）
</background_information>

## 引数

| 位置 | 意味 | 例 |
|------|------|-----|
| `$1` | 機能名（日本語・英語いずれも可） | `ユーザーログイン` / `user-login` |

- `$1` が日本語なら、Claude が英語 kebab-case スラッグ `<spec-name>` を自動決定する（`spec-requirements` / `spec-design` と同じ規則）。
- **前提**: 本スキルを呼び出す時点で `requirements.md` と `design.md` は人間により承認済みであることを想定する。`spec.json` の `approvals.requirements.approved` / `approvals.design.approved` の状態は **検証しない**（承認済みとして扱う）。

## 出力先

```
.memory-bank/specs/<spec-name>/
├── spec.json        # メタデータ更新
├── requirements.md  # 入力（本スキルでは生成しない）
├── design.md        # 入力（本スキルでは生成しない）
└── tasks.md         # 本スキルで生成／更新
```

- 親ディレクトリが存在しなければ作成する。
- 既存 `tasks.md` がある場合は、**差分要点を出力ログに記録した上で自動上書き**する。既存内容は参照文脈（マージモード）として取り込み、残作業・変更点を新版に統合する（ユーザ確認は取らない）。

<instructions>

## 主タスク

承認済みの `requirements.md` と `design.md` を基に、機能 **$1** の実装タスクを生成し、`.memory-bank/specs/<spec-name>/tasks.md` に書き出す。

---

## 実行手順

### Phase 0: コンテキスト読込・入力健全性チェック

**1. コンテキスト一括読込**（並列 Read 可）:

- `.memory-bank/specs/<spec-name>/spec.json`（言語・承認状態・既存フェーズ）
- `.memory-bank/specs/<spec-name>/requirements.md`（要件・数値 ID の源泉）
- `.memory-bank/specs/<spec-name>/design.md`（コンポーネント・境界・契約の源泉）
- `.memory-bank/specs/<spec-name>/tasks.md`（存在すればマージ文脈）
- `.memory-bank/specs/<spec-name>/gap-analysis.md`, `research.md`（存在すれば参考）
- `.memory-bank/steering/` 全体（`productContext.md` / `projectBrief.md` / `systemPatterns.md` / `techContext.md` ＋カスタム steering）
- テンプレート: `.memory-bank/specs/tasks.md`（タスク骨格）
- 本スキル同梱の `.claude\skills\spec-requirements\reference/` 全ファイル:
  - `.claude\skills\spec-requirements\reference/tasks-generation.md`（生成原則・レビューゲート）
  - `.claude\skills\spec-requirements\reference/tasks-parallel-analysis.md`（`(P)` 判定基準）
  - `.claude\skills\spec-requirements\reference/tasks-template.md`（`(P)` マーカー対応フォーマット）

**2. spec-name 決定**:

- `$1` が日本語なら Claude が英語 kebab-case スラッグ `<spec-name>` を自動決定
- 出力先ディレクトリが無ければ作成、既存 `tasks.md` があれば参照文脈として読み込み、書き出し時に自動マージ上書き（ユーザ確認は取らない）

**3. 入力健全性チェック**:

- `requirements.md` に数値 ID が無い／英字ラベル（"Requirement A" 等）が含まれる場合: 停止し `/spec-requirements` で修正を依頼
- `requirements.md` または `design.md` が存在しない場合: 停止し、先に `/spec-requirements` / `/spec-design` の完了を案内
- 承認状態（`approvals.*`）は検証しない。**本スキル呼び出し時点で requirements/design は承認済みである前提**で続行する

---

### Phase 1: タスクプランのドラフト作成

**目的**: `.claude\skills\spec-requirements\reference/tasks-generation.md` のすべての原則を適用し、`tasks.md` のドラフトを内部的に組み立てる。書き出しは Phase 3。

**1. 要件とコンポーネントの棚卸し**:

- `requirements.md` から全数値 ID を抽出（例: 1.1, 1.2, 2.1, 2.2, ...）
- `design.md` から全コンポーネント／インターフェース契約／統合ポイント／ NFR 検証項目を抽出
- 既存 `tasks.md` があれば、残作業・変更点・廃止項目を識別

**2. タスク分解**（`.claude\skills\spec-requirements\reference/tasks-generation.md` の Core Principles に厳密準拠）:

- **Task Ordering**: Foundation → Core → Integration → Validation の順で並べる
- **最大 2 階層**: メジャータスク（1, 2, 3...）とサブタスク（1.1, 1.2, ...）のみ。3 階層以上禁止
- **サブタスク粒度**: 各 1〜3 時間、詳細 3〜10 項目
- **単一サブタスク構造**の潰し込み: メジャータスクの下にサブタスクが 1 件しか無いならメジャーへ昇格（容れ物メジャー禁止）
- **自然言語**: 「何をするか」を記述し、ファイル名・関数名・型定義は書かない（それらは `design.md` に属する）
- **Observable Completion**: 各実行可能タスクに「完了時に何が真となるか」を示す詳細 1 項目以上を含める
- **Requirements Mapping**: 各タスクの末尾に `_Requirements: X.Y, Z.W_` を付す（**数値 ID のみ**、説明サフィックス・括弧・翻訳・英字ラベル禁止）
- **Boundary Scope**: `(P)` タスクには `_Boundary: <Component>_` を必須、それ以外は省略可
- **Depends**: 順序から自明でないクロスバウンダリ依存のみ `_Depends: X.Y_` で明示

**3. 並列タスク識別**:

- `.claude\skills\spec-requirements\reference/tasks-parallel-analysis.md` の 5 条件をすべて満たすタスクに `(P)` を付与
  1. 保留中タスクへのデータ依存がない
  2. 共有可変リソースやファイルが衝突しない
  3. 他タスクのレビュー／承認を事前要求しない
  4. Foundation フェーズの前提作業が完了済み
  5. `_Boundary:_` が非重複コンポーネントを示す
- Foundation フェーズは通常 `(P)` にならない（共有前提を作る側のため）
- Core フェーズが主な `(P)` 候補
- `(P)` タスクでクロスバウンダリ依存がある場合は `_Depends: X.Y_` を明示
- `(P)` は番号直後に配置（チェックボックス外）: `- [ ] 2.1 (P) ...`

**4. オプションテストタスク**:

- 設計が機能カバレッジを保証しており、MVP 優先でテストを後回しにできる場合のみ `- [ ]*` で markable
- 詳細に `requirements.md` の受け入れ基準を直接参照させる
- 実装作業や統合クリティカル検証には使用禁止

---

### Phase 2: Task Plan Review Gate

**目的**: 書き出し前にドラフトを機械的・判断的に検査し、最大 2 pass で修復する。通らなければ真の spec ギャップとして停止し、前フェーズへ差し戻す。

**1. Coverage Review**:

- `requirements.md` の全数値 ID がドラフト内のいずれかのタスクの `_Requirements:_` に登場するか
- `design.md` の全コンポーネント／契約／統合／NFR 検証がタスクに紐付いているか
- カバレッジ不足があれば、タスクプランのローカル修復で解消できるか判定
  - 解消可能: ドラフトを更新してレビューを再実行
  - 解消不可（要件・設計の曖昧／矛盾／未特定）: **停止**し `/spec-requirements` または `/spec-design` へ差し戻し

**2. Executability Review**:

- 各サブタスクが 1〜3 時間で実行可能か
- 各サブタスクに Observable Completion bullet が含まれるか
- 複数の独立検証可能成果を混ぜたタスクは分割
- 複数境界をまたぐ通常タスクは、明示的な Integration タスクへ再編
- 過度な `_Boundary:_` 横断や小さすぎる記帳だけのタスクは統合 or 再分解
- 暗黙前提は先行タスクとして顕在化
- 編集後に `_Depends:_` / `_Boundary:_` / `(P)` を再検証

**3. Loop 制限**:

- 最大 2 pass。通らなければ spec ギャップとして Phase 0 の前段へ戻す

---

### Phase 3: 書き出しと spec.json 更新

**1. tasks.md 書き出し**:

- `.claude\skills\spec-requirements\reference/tasks-template.md` のフォーマットに厳密準拠して `.memory-bank/specs/<spec-name>/tasks.md` を書き出す
- 記述言語は `spec.json` 指定に従う（未指定なら `en`）
- 既存 `tasks.md` がある場合は、上書き確認済みの前提でマージ結果を書き出す

**2. spec.json メタデータ更新**:

- `phase: "tasks-generated"`
- `approvals.tasks.generated: true, approved: false`
- `approvals.requirements.approved: true`
- `approvals.design.approved: true`
- `updated_at` を更新

---

## 重要な制約

- **ルール厳守**: `.claude\skills\spec-requirements\reference/tasks-generation.md` の原則はすべて必須
- **自然言語**: コード構造・ファイル名・関数名ではなく「何をするか」を記述
- **完全網羅**: `requirements.md` の全数値 ID と `design.md` の全コンポーネントをタスクへ対応付ける
- **最大 2 階層**: メジャータスクとサブタスクのみ（3 階層以上禁止）
- **連番維持**: メジャータスクは 1, 2, 3... と増分、重複不可
- **統合性**: すべてのタスクはシステムに接続される（孤立作業を作らない）
- **要件 ID の形式**: `_Requirements:_` は数値 ID のカンマ区切りのみ（"Requirement 2.1" のような接頭辞・創作 ID・英字ラベル禁止）
- **並列マーカー**: `(P)` は番号直後・チェックボックス外
- **オプションマーカー `- [ ]*`**: 延期可能な補助テストに限定。実装・統合検証には不可
- **サブエージェント**: 本スキルでは原則使わず、本体で `tasks.md` を執筆する（サブエージェントにファイル書込みさせない）

</instructions>

## ツールガイダンス

- **最初に読み込む**: Phase 0 で spec / steering / templates / .claude\skills\spec-requirements\reference を一括読込
- **最後に書き込む**: Phase 1〜2 のドラフト・レビューが固まってから Phase 3 で `tasks.md` と `spec.json` を書き出す
- **Grep / Glob 活用**: `requirements.md` の数値 ID 抽出、`design.md` のコンポーネント抽出で使用

## 出力仕様（コマンド実行出力、成果物本文とは別）

`spec.json` 指定言語で簡潔に報告:

1. **ステータス**: `.memory-bank/specs/<spec-name>/tasks.md` にタスクを生成／更新したことを確認
2. **タスク要約**:
   - 合計: X 件のメジャータスク、Y 件のサブタスク
   - Z 件の要件（数値 ID）をすべてカバー
   - 並列タスク数（`(P)` 付与数）
   - サブタスク平均粒度: 1〜3 時間
3. **品質検証**:
   - ✅ すべての要件 ID がタスクに対応
   - ✅ すべての設計コンポーネントが対応
   - ✅ タスク依存関係を検証
   - ✅ `(P)` タスクの `_Boundary:_` 非重複を確認
4. **次アクション**: `/spec-impl <feature>` でタスク実行、または特定タスクは `/spec-impl <feature> 1.1`

**形式**: 簡潔（200 語未満）。

## 安全性とフォールバック

### エラーシナリオ

**要件または設計ファイル不足**:
- 実行停止
- メッセージ: 「`.memory-bank/specs/<spec-name>/` に requirements.md または design.md がありません」
- 推奨: 「先に `/spec-requirements` と `/spec-design` を完了してください」

**要件 ID の数値欠如**:
- 実行停止
- メッセージ: 「requirements.md に英字 ID（例: Requirement A）が含まれます。数値 ID へ正規化してください」
- 推奨: 「`/spec-requirements` で修正してください」

**要件カバレッジ不足**（Phase 2 で検出）:
- タスクプラン側で解消可能: ドラフトを修復して再レビュー（最大 2 pass）
- 解消不可: 停止し、意図的ギャップかユーザへ確認、または `/spec-requirements` / `/spec-design` へ差し戻し

**テンプレート／ルール欠如**:
- メッセージ: 「`.memory-bank/specs/tasks.md` テンプレートが見つかりません」
- フォールバック: `.claude\skills\spec-requirements\reference/tasks-template.md` を直接使用（警告付き）
- 推奨: 「リポジトリ設定を確認するか、テンプレートを復元してください」

**出力先既存ファイル**:
- 既存 `tasks.md` がある場合は、差分要点を出力ログに記録した上で**自動上書き**する（ユーザ確認は取らない）

**spec-name 衝突**:
- 自動決定したスラッグが想定外の既存ディレクトリと衝突する場合は、数値サフィックス（`-2`, `-3`…）を自動付与して新規スラッグとする（ユーザ確認は取らない）

### 次フェーズ: 実装

**実装開始前**:
- **重要**: `/spec-impl` 実行前に会話履歴をクリアし、コンテキストを解放することを推奨
- 初回タスク開始時・タスク切り替え時のいずれも適用
- 新鮮なコンテキストにより、クリーンな状態と適切なタスク集中を確保

**タスク承認済みの場合**:
- 特定タスク実行: `/spec-impl <feature> 1.1`（推奨: タスクごとに文脈クリア）
- 複数タスク実行: `/spec-impl <feature> 1.1,1.2`（慎重に使用。間で文脈クリア）
- 引数なし: `/spec-impl <feature>`（未完了全実行。文脈肥大化のため非推奨）

**修正が必要な場合**:
- フィードバックを反映し本スキルを再実行
- 既存 `tasks.md` は参照文脈（マージモード）として利用
