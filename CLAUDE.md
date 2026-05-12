# プロジェクト運用ルール

このリポジトリでは、ソースコードの変更に追随して **設計ドキュメント (`Docs/` または `docs/`)** と **共有メモリバンク (`MemoryBank/` または `memory-bank/`)** を常に最新に保つ運用を採用している。
従来この運用は `.claude/hooks/` 配下の PowerShell フックで強制していたが、フックが動作しない環境（非 Windows、PowerShell 未導入、Hooks 無効化など）でも同じ振る舞いを再現できるよう、ここに明文化する。

以下のルール 1〜3 は、フックの有無に関わらず常に遵守すること。

---

## ルール 1: セッション開始時とコンパクション後の MemoryBank 読み込み

セッションを開始した直後、および会話履歴がコンパクションされた直後は、最初の作業に着手する前に `MemoryBank/` 配下の以下のファイルを **必ず読む**。

- `MemoryBank/activeContext.md` — 現在のフォーカス
- `MemoryBank/decisionLog.md` — 直近の意思決定ログ
- `MemoryBank/openQuestions.md` — 未解決の論点

(ディレクトリ名が `memory-bank/` の場合も同様。どちらも存在しない場合は読み飛ばしてよい。)

これらは「コンパクションで失われると以後の判断品質が著しく落ちる前提知識」を保持しているため、再注入を欠かさないこと。各ファイル 4000 文字を超える部分は要点だけ把握すればよい。

## ルール 2: ソースコード編集後の Docs / MemoryBank 更新

以下に該当するファイルを `Edit` / `Write` した直後は、関連する設計書 (`Docs/` または `docs/`) と共有メモリ (`MemoryBank/` または `memory-bank/`) の更新要否を **必ず検討する**。

**対象パス（いずれかで始まる）**
`src/`, `app/`, `packages/`, `api/`, `db/`, `schema/`, `backend/`, `frontend/`

**対象拡張子**
`.ts`, `.tsx`, `.js`, `.jsx`, `.mjs`, `.cjs`, `.py`, `.go`, `.java`, `.rb`, `.php`, `.sql`, `.yaml`, `.yml`, `.json`, `.cs`, `.cpp`, `.c`, `.h`

**除外パス（更新検討は不要）**
`Docs/`, `docs/`, `MemoryBank/`, `memory-bank/`, `.claude/`

更新の最低基準:

- `MemoryBank/activeContext.md` と `MemoryBank/decisionLog.md` は必ず内容をレビューし、影響があれば追記する
- パターン化された設計判断が発生したら `MemoryBank/patterns.md` を更新
- 未解決の論点が発生したら `MemoryBank/openQuestions.md` を更新
- 仕様や設計に影響するコード変更なら `Docs/` (または `docs/`) の該当ファイルを更新

作業のまとめで「どの Docs / MemoryBank ファイルを更新したか」を明示的に報告すること。

## ルール 3: 終了前の整合性チェック（Docs / MemoryBank 同時更新）

ユーザーへの最終応答を返す前に、変更状態を確認する:

```bash
git diff --name-only HEAD
git ls-files --others --exclude-standard
```

これらに含まれるパスを次の 3 区分に分類する:

- **docs**: `Docs/` または `docs/` で始まる
- **memory**: `MemoryBank/` または `memory-bank/` で始まる
- **claude meta**: `.claude/` で始まる
- **non-meta**: 上記いずれにも該当しない（= ソース / 設定 / その他の実体ファイル）

**non-meta が 1 件以上あるのに docs または memory の更新が無い** 場合は、まだ作業を終わらせない。
不足側 (`Docs/` / `MemoryBank/`) を更新してから完了報告すること。やむを得ず更新しない場合は、その理由をユーザーに明示的に伝えてから終わる。

(ディレクトリが存在しない、または対象外と判断した場合は、その旨をユーザーに告げて完了してよい。)

---

## 補足: フック実装との対応

以下は参考情報。CLAUDE.md のルールが優先される。

| ルール | 対応フック | トリガ |
| --- | --- | --- |
| 1 | `.claude/hooks/inject_memory_bank.ps1` | `SessionStart` (matcher: `compact`) |
| 2 | `.claude/hooks/docs_memory_reminder.ps1` | `PostToolUse` (matcher: `Edit\|Write`) |
| 3 | `.claude/hooks/ensure_docs_memory_updated.ps1` | `Stop` |

PowerShell が利用できる環境ではフックも併用されるが、フックは「忘れた場合の保険」として機能する。一次的な責任はこの CLAUDE.md に従う Claude 側にある。
