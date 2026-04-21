---
name: spec-design
description: 承認済み要件から技術設計を確定させる一連の手順（ギャップ分析 → 技術設計生成 → 設計品質レビュー）をサブエージェントで並列化しながら実行するスキル。ユーザが「設計書を作って」「技術設計を作成」「設計を確定させて」などと言った場合に起動する。
allowed-tools: Bash, Glob, Grep, LS, Read, Write, Edit, MultiEdit, WebSearch, WebFetch, Task
argument-hint: <feature-name> [-y]
---

# 技術設計パイプライン

<background_information>
- **ミッション**: 承認済み要件（WHAT）を、実装可能なアーキテクチャ設計（HOW）へ落とし込み、レビューを経て実装タスク生成の直前まで進める。
- **全体フロー**（単線・戻りあり）:

  ```
  [Phase 0] 前提読込・承認確認
        ↓
  [Phase 1] ギャップ分析   ← サブエージェント並列
        ↓
  [Phase 2] 調査・研究     ← サブエージェント並列
        ↓
  [Phase 3] 設計文書生成   ← 本体が統合して執筆
        ↓
  [Phase 4] 品質レビュー   ← 独立サブエージェント + ユーザ対話
        ↓
   GO → 完了 / NO-GO → Phase 2 or 3 へ戻って再実行
  ```

- **成功条件**:
  - 要件ID（数値）が設計コンポーネントに 1:1 で紐付いている
  - ギャップと調査結果が `gap-analysis.md` / `research.md` に一次情報付きで残っている
  - `design.md` がテンプレート骨格に厳密準拠し、型安全性・図・NFR を満たす
  - レビューで最重要課題（最大 3 件）が GO に対して残存していない
</background_information>

## 引数

| 位置 | 意味 | 例 |
|------|------|-----|
| `$1` | 機能名（日本語・英語いずれも可） | `ユーザーログイン` / `user-login` |
| `$2` | `-y` フラグ（要件自動承認） | `-y` |

- `$1` が日本語なら、Claude が英語 kebab-case スラッグ `<spec-name>` を自動決定する（`spec-requirements` と同じ規則）。
- `-y` が付与された場合は、`spec.json` の `approvals.requirements.approved = true` に更新してから Phase 1 へ進む。
- スキップ不可: Phase 1〜4 はすべて一連で実行する。ユーザが「ここまででいい」と停止要求を出すまで連続で進める。

## 出力先

```
.memory-bank/specs/<spec-name>/
├── spec.json           # メタデータ更新（各 Phase 終了時）
├── requirements.md     # 入力として参照（本スキルでは生成しない）
├── gap-analysis.md     # Phase 1 で生成／更新
├── research.md         # Phase 2 で生成／更新
└── design.md           # Phase 3 で生成／更新、Phase 4 で修正反映
```

- 親ディレクトリが存在しなければ作成する。
- 既存 `gap-analysis.md` / `research.md` / `design.md` がある場合は、**差分要点を提示した上で上書き可否をユーザへ確認**（無断上書き禁止）。差分が小さい場合はマージモード（参照文脈）として扱う。

<instructions>

## 主タスク

機能 **$1** について、`.memory-bank/specs/<spec-name>/requirements.md` を起点に、ギャップ分析・調査・設計・レビューを一連で実施し、実装タスク生成に進める状態まで確定させる。

---

## Phase 0: 前提読込・承認確認

**1. コンテキスト一括読込**（並列 Read 可）:

- `.memory-bank/specs/<spec-name>/spec.json`（言語・承認状態・既存フェーズ）
- `.memory-bank/specs/<spec-name>/requirements.md`（要件）
- `.memory-bank/specs/<spec-name>/gap-analysis.md`, `research.md`, `design.md`（存在すればマージ文脈）
- `.memory-bank/steering/` 全体（`productContext.md` / `projectBrief.md` / `systemPatterns.md` / `techContext.md` ＋カスタム steering）
- テンプレート: `.memory-bank/specs/design.md`（設計骨格）, `.memory-bank/specs/research.md`（調査ログ骨格）
- 本スキル同梱の `reference/` 全ファイル:
  - `reference/gap-analysis.md`（Phase 1 の分析フレームワーク）
  - `reference/design-discovery-full.md`（Phase 2: 新規・複雑統合の調査）
  - `reference/design-discovery-light.md`（Phase 2: 拡張機能の軽量調査）
  - `reference/design-synthesis.md`（Phase 2 終盤: Generalization / Build vs Adopt / Simplification）
  - `reference/design-principles.md`（Phase 3 の設計原則・セクション記法）
  - `reference/design-review-gate.md`（Phase 3→4 の機械的ゲートチェック）
  - `reference/design-review.md`（Phase 4 のレビュー基準・出力形式）

**2. spec-name 決定**:

- `$1` が日本語なら Claude が英語 kebab-case スラッグ `<spec-name>` を自動決定
- 出力先ディレクトリが無ければ作成、既存ファイル衝突は上書き確認

**3. 要件承認の検証**:

- `$2 == "-y"` の場合: `spec.json.approvals.requirements.approved = true` に更新して続行
- 未承認かつ `-y` 無しの場合: 実行停止し `「-y で要件を自動承認すれば続行できます」` と案内
- `requirements.md` に数値 ID が無い／英字ラベル（"Requirement A" 等）が含まれる場合: 停止し `/spec-requirements` で修正を依頼

---

## Phase 1: ギャップ分析

**目的**: 要件と既存コードベースの差分を可視化し、Phase 2 以降の調査観点と実装アプローチ候補を洗い出す。最終判断はしない。

**サブエージェント並列起動**（**必ず 1 メッセージ内で複数 Task 呼び出し**）:

- **A. 既存実装マップ**: `code-explorer`
  - プロンプト: 「要件 `<requirements.md の ID とタイトル一覧>` に対応する既存機能・モジュール・データモデルを特定せよ。エントリポイント、レイヤ構造、データフロー、依存関係をマップして報告。対象: `<プロジェクトルート>`。詳細はファイル名:行番号で引用。300 語以内で要約。」
- **B. パターン・規約調査**: `Explore`（thoroughness: medium）
  - プロンプト: 「プロジェクトで踏襲すべき命名規則、エラーハンドリング、DI/モジュール境界、テスト規約を調べ、新機能が従うべき既存パターンをリストアップせよ。」
- **C. 統合ポイント・外部依存調査**: `Explore`（thoroughness: medium）
  - プロンプト: 「この機能が触れる可能性のある API 境界、イベントバス、外部サービス、設定、環境変数を洗い出せ。バージョン互換性の懸念も含めて報告。」

**本体処理**:

- サブエージェント 3 つの結果を集約
- `reference/gap-analysis.md` のフレームワーク（Current State / Feasibility / Options A-B-C / Out-of-Scope / Complexity & Risk / Output Checklist）に沿って `.memory-bank/specs/<spec-name>/gap-analysis.md` を生成／更新
- 複数の実装アプローチ（拡張 / 新規 / ハイブリッド）をトレードオフ付きで提示
- 追加調査が必要な領域を「Phase 2 の調査項目」として明示化
- ユーザに **簡易確認**（「この方針で Phase 2 の調査に進んでよいか？」）を取る。修正要望があれば gap-analysis を更新してから進む。

---

## Phase 2: 調査・研究

**目的**: Phase 1 で特定した調査項目と、機能タイプに応じた深度で技術調査を行い、`research.md` に永続化する。

**1. 機能タイプ分類**:

- 新規機能（グリーンフィールド）・複雑統合 → `reference/design-discovery-full.md` に従う（full discovery）
- 拡張（既存システム）→ `reference/design-discovery-light.md` に従う（light discovery）
- 単純追加（CRUD/UI）→ minimal（本体で Grep/Read を 1〜2 箇所確認して完了）
- light 実施中に「大規模アーキ変更・複雑統合・セキュリティ・性能」要素が見つかったら `design-discovery-light.md` の "When to Escalate to Full Discovery" に従い full へ昇格

**2. サブエージェント並列起動**（機能タイプに応じて **1 メッセージ内で複数 Task**）:

- **R1. アーキテクチャ比較・境界マップ**: `architect`
  - プロンプト: 「要件の非機能要件と制約 `<抜粋>` に対し、候補アーキテクチャパターン（例: レイヤード / ヘキサゴナル / イベント駆動）を 2〜3 案比較し、ステアリング文脈 `<techContext.md, systemPatterns.md の要約>` との整合を評価せよ。推奨案と境界マップを提示。」
- **R2. 外部依存・ライブラリ検証**: `docs-lookup` もしくは本体 WebSearch/WebFetch
  - バージョン互換性、移行ガイド、既知脆弱性、パフォーマンス指標
- **R3. 既存統合ポイント深掘り**（拡張・複雑統合時のみ）: `code-explorer`
  - Phase 1 の結果を起点に、具体的な拡張点・拡張不可点を確定
- **R4. 並列化・依存関係の評価**: `planner`
  - 後続 `spec-tasks` で並列化可能な単位と依存関係を洗い出す
- **R5. 脅威モデル・性能予測**（セキュリティ／性能クリティカル時のみ）: `security-reviewer`, `performance-optimizer`
  - OWASP 観点・性能ボトルネック予測

**3. 本体処理**:

- 各サブエージェント結果を `.memory-bank/specs/research.md` の骨格へ統合し、`.memory-bank/specs/<spec-name>/research.md` を生成／更新
- 各トピックに**情報源・示唆・設計への影響**を明記
- 記述言語は `spec.json` 指定に従う（未指定なら `en`）

**4. Design Synthesis**（`reference/design-synthesis.md` に従い、**並列化せず本体で実施**）:

- **Generalization**: 複数要件の共通構造を抽出し、汎用化すべきインターフェースを特定。実装範囲は現要件に限定し、インターフェースだけ汎化
- **Build vs Adopt**: 主要コンポーネントごとに、RFC / 既存ライブラリ / プラットフォーム機能で代替可能か評価。採用時は保守状況・スタック整合・NFR 満足を確認。自作時は却下理由を `research.md` に記録
- **Simplification**: "念のため" のコンポーネントや抽象層を削除。単一実装しかないインターフェースは除去を検討
- 結果を `research.md` の "Design Decisions" 節へ追記

---

## Phase 3: 設計文書生成

**目的**: Phase 1〜2 の成果を統合し、`design.md` を生成する。**本体が執筆する**（サブエージェントには書かせない）。

**1. ドラフト執筆**（`reference/design-principles.md` を厳密適用）:

- `.memory-bank/specs/design.md` の骨格に**厳密準拠**（見出し階層・番号・プレースホルダ構造を逸脱しない）
- 収集情報（API 契約、採用技術、既存パターン）をコンポーネント定義・設計判断・統合ポイントへ統合
- `design-principles.md` の以下を特に遵守:
  - **Boundary First**: `Boundary Commitments` / `Out of Boundary` / `Allowed Dependencies` / `Revalidation Triggers` を最初に埋める
  - **Type Safety Mandatory**: TypeScript の `any` 禁止、動的型付け言語は型ヒント、公開契約を明文化
  - **Design vs Implementation**: WHAT に集中、実装コードは書かない
  - **Dependency Direction**: アーキテクチャ節で依存方向を明示（例: Types → Config → Repository → Service → Runtime → UI）
  - **Requirement IDs**: `requirements.md` の数値 ID を `2.1, 2.3` 形式で**正確に転記**（"Requirement 2.1" のような接頭辞・創作 ID・英字ラベル禁止）
  - **Mermaid Rules**: ノード ID は英数字＋アンダースコアのみ、ラベルに `()/[]/""/@/` 等の記号禁止
- 章「Architecture」「File Structure Plan」「Components & Interface Contracts」は `research.md` の裏付けを参照
- 既存 `design.md` があればマージモード（差分提示 → 上書き確認）

**2. Design Review Gate**（書き出し前の機械的ゲート、`reference/design-review-gate.md` に従う）:

本体で以下をドラフトに対して実施。**失敗したら修復して再実行**。最大 2 pass。

- **機械的チェック**:
  - [ ] `requirements.md` の全数値 ID がドラフトのトレーサビリティに現れているか
  - [ ] `Boundary Commitments` / `Out of Boundary` / `Allowed Dependencies` / `Revalidation Triggers` がプレースホルダでなく実体を持つか
  - [ ] `File Structure Plan` に具体ファイルパスが入っているか（"TBD" 禁止）
  - [ ] 境界記述と File Structure Plan の所有範囲が一致しているか
  - [ ] ドラフト内で言及されたコンポーネントが全て File Structure Plan に行を持つか（孤立コンポーネント禁止）
- **判断的レビュー**: Requirements Coverage / Architecture Readiness / Boundary Readiness / Executability（`design-review-gate.md` の各節）
- 2 pass 以内に通らなければ「真の spec ギャップ」として停止し、Phase 2 へ戻るか `/spec-requirements` へ差し戻す

**3. 書き出し**: ゲート通過後のみ `.memory-bank/specs/<spec-name>/design.md` として書き出す。

**spec.json メタデータ更新**:

- `phase: "design-generated"`
- `approvals.design.generated: true, approved: false`
- `approvals.requirements.approved: true`
- `updated_at` を更新

---

## Phase 4: 品質レビュー（GO/NO-GO 判定）

**目的**: `design.md` の実装準備完了度を、独立視点のサブエージェント + ユーザ対話で判定する。

**1. 独立レビュー（サブエージェント）**:

以下を **並列起動**:

- **V1. アーキテクチャ独立レビュー**: `architect`（または `code-reviewer`）
  - プロンプト: 「`.memory-bank/specs/<spec-name>/design.md` と `requirements.md` を独立視点でレビューせよ。`reference/design-review.md` の Core Review Criteria（Existing Architecture Alignment / Design Consistency & Standards / Extensibility & Maintainability / Type Safety & Interface Design）に従い、**最重要課題を最大 3 件**、設計の強みを 1〜2 件挙げよ。各課題は `🔴 Critical Issue [n]: Title / Concern / Impact / Suggestion / Traceability (requirements.md の ID) / Evidence (design.md のセクション)` のフォーマットで報告。全体の GO/NO-GO 案と根拠も添えよ。」
- **V2. 要件トレーサビリティ照合**: `Explore`（thoroughness: quick）
  - プロンプト: 「`requirements.md` の全数値 ID が `design.md` 内で参照されているか、参照漏れ／創作 ID が無いかを照合して報告。」

**2. 本体処理（ユーザ対話重視）**:

- サブエージェント結果を本体で整理
- **ユーザへ重要課題を 1 件ずつ提示** し、意見を聞きながら合意形成（一方通行禁止）
- 合意した改善案を記録
- 全課題について合意が取れた段階で、`reference/design-review.md` の Output Format に従って最終評価を出力:
  1. **Design Review Summary**（2〜3 文）
  2. **Critical Issues**（最大 3 件、各 5〜7 行、Traceability ＋ Evidence 必須）
  3. **Design Strengths**（1〜2 件）
  4. **Final Assessment**: **GO** / **NO-GO**、Rationale、Next Steps
  5. **Interactive Discussion**: 設計者の観点・代替案・必要な変更について対話
- 全体で約 400 語を目安（`design-review.md` の Length & Focus）

**3. 判定後の処理**:

- **GO**:
  - `spec.json.approvals.design.approved = true` に更新
  - `updated_at` を更新
  - 次アクションとして `/spec-tasks <feature> -y` を案内して終了
- **NO-GO**:
  - 重要課題のうち「再調査が必要」なものは **Phase 2 へ戻る**
  - 「設計文書の修正のみで解消」なものは **Phase 3 へ戻る**
  - 修正後、Phase 4 を再実行して再判定

## 重要な制約

- **設計に集中**: アーキテクチャ・インターフェース・契約のみ（実装コードは書かない）
- **型安全性**:
  - TypeScript では `any` を絶対に使わない
  - 動的型付け言語は型ヒント／アノテーション + 境界での入力検証
  - 公開インターフェースと契約を明文化
- **最新情報**: 外部依存・ベストプラクティスは WebSearch/WebFetch か `docs-lookup` で確認
- **ステアリング整合**: `.memory-bank/steering/` の既存パターンを尊重
- **テンプレート準拠**: `.memory-bank/specs/design.md` / `research.md` の構造を厳密遵守
- **要件トレーサビリティ ID**: 数値 ID のみを正確に転記（創作・英字ラベル禁止）
- **ギャップ分析は決定しない**: 最終判断は Phase 3 で行う
- **レビューは完全性より品質保証**: 許容可能なリスクは受け入れ、最重要 3 件に絞る
- **レビューは対話**: 一方通行評価禁止
- **サブエージェント分担**:
  - 独立タスクは **必ず 1 メッセージで並列起動**
  - 各プロンプトは**自己完結**（本会話の文脈を知らない前提）
  - サブエージェントは**ファイル書込みしない**。本体が最終成果物を書く
  - 既存コード探索: `Explore` / `code-explorer`
  - アーキテクチャ判断・独立レビュー: `architect`（必要に応じ `code-reviewer`）
  - ライブラリ文書: `docs-lookup`
  - 並列化・依存関係: `planner`
  - セキュリティ・性能: `security-reviewer` / `performance-optimizer`（セキュリティ／性能クリティカル時のみ）

</instructions>

## ツールガイダンス

- **並列化を第一に**: 独立した調査・レビューは **1 メッセージで複数 Task 並列起動**
- **最初に読み込む**: Phase 0 で spec / steering / templates / reference を一括読込
- **不確実なら調査**: 外部依存・API は WebSearch/WebFetch または `docs-lookup` で補強
- **最後に書き込む**: 各 Phase の分析・合意が固まってから `gap-analysis.md` / `research.md` / `design.md` を書き出す

## 出力仕様（コマンド実行出力、成果物本文とは別）

各 Phase 終了時に `spec.json` 指定言語で簡潔に以下を提示する:

- **Phase 1 終了時**: 実装アプローチ候補のサマリー（3〜5 項目）、起動サブエージェント一覧、次 Phase 案内
- **Phase 2 終了時**: 調査タイプ（full/light/minimal/full+）、主要発見 2〜3 点、起動サブエージェント一覧
- **Phase 3 終了時**: 生成ファイルパス、採用アーキテクチャパターンの要点、要件 ID カバレッジ
- **Phase 4 終了時**: レビュー要約・重要課題・強み・最終評価（GO/NO-GO）、次アクション

**形式**: 簡潔な Markdown（各 Phase 300 語未満）。成果物本文ではない。

## 安全性とフォールバック

### エラーシナリオ

**共通**:

- **requirements.md 不在**: 停止し、`/spec-requirements <feature>` 実行を案内
- **spec.json 不在**: 停止し、初期化手順を案内
- **steering 空**: 警告し、設計品質が低下しうる旨を明記して続行
- **テンプレート欠如**: `.memory-bank/specs/design.md` / `research.md` 不在なら警告してインライン骨格で代用
- **言語未定義**: `spec.json` に言語がなければ英語 `en` を既定
- **サブエージェント失敗**: 代替として本体で直接調査を実施（停止はしない）。失敗したエージェントとその影響を Phase 終了出力に明記

**Phase 0**:

- **要件未承認かつ `-y` 無し**: 停止。`-y` 付与または手動承認を促す
- **不正な要件 ID**: 停止し、`/spec-requirements` で数値 ID への修正を依頼

**Phase 1**:

- **複雑統合が判別しづらい**: ブロックせず、`gap-analysis.md` に「要追加調査」タグを残して Phase 2 へ申し送り

**Phase 2**:

- **調査の複雑度が不明瞭**: デフォルトで full を採用（取りこぼしより過剰調査を優先）

**Phase 3**:

- **既存 design.md と差分が大きい**: 差分要点を提示して上書き可否を確認

**Phase 4**:

- **重要課題が 3 件を超える**: 最重要 3 件に絞り、残りは `research.md` の「未決事項」節へ退避
- **ユーザが GO を主張するが Blocker 残存**: NO-GO 推奨を明示し、受容する場合はリスク受容として `spec.json` に記録

### 出力先既存ファイル

- 既存 `gap-analysis.md` / `research.md` / `design.md` がある場合は**差分要点を提示**し、**上書き可否をユーザに確認**（自動上書き禁止）

### 次フェーズ（本スキル完了後）

- **Phase 4 で GO**: `/spec-tasks <feature> -y` で実装タスク生成へ
- **Phase 4 で NO-GO**: 重要課題を反映し、Phase 2 or 3 へ戻って本スキル内で再実行
