# Excel(.xlsx) / Word(.docx) -> Markdown 変換（Windows向け）

## 前提
- Windows
- Python 3.12+（未インストールなら例：`winget install -e --id Python.Python.3.12`）
```mermaid
flowchart LR
    A[既存設計書<br>（.xlsx or .docx）] -->|Pythonコマンド<br>convert_to_md.cmd| B[Cline用一時的な情報<br>`temp_design/`]
    B -->|Clineコマンド<br>/adjust_md_design| C[最終的なmdの設計書<br>docs/design配下に永続化想定]

```

## 使い方（エクスプローラー上で完結します）
1. このリポジトリをクローン
2. `設計書/` フォルダに `.xlsx` や `.docx` ファイルを入れる（サブフォルダOK）
3. `run.cmd` を実行（ダブルクリックで実行可）

出力は `converted_md_design/` に、`設計書/` と同じサブディレクトリ構造で保存されます。
- 各xlsxファイル：「シートごとにmdファイル」を生成
- 各docxファイル：「1つのmdファイル」を生成

## オプション
- 空行2行以上で表を分割したい場合:
  `run.cmd --blank-rows 2`

## 注意
- 結合セルは、結合範囲を同じ値で埋めてMarkdown表にします。
- 数式は「表示結果の値」を読みます（Excelで保存時点の計算結果が必要）。
  値が空になる場合は、Excelで一度開いて保存してから実行してください。
- 画像は無視します。
