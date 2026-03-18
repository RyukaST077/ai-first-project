# 出力制限ルール（PowerShell）

## 目的

* **全ログはファイルへ保存**し、後から参照できるようにする。
* **端末（標準出力）にはログの末尾200行のみ**を表示し、AIエージェントの入力エラー（出力量過多）を防ぐ。

## 基本方針

* `Select-Object -Last 200` で直接絞るのは避ける（実行が終わるまで出力が出ず、内部で溜め込むため）。
* まず **全出力をログファイルへ**書き出し、完了後に **Tail（末尾）だけ**表示する。
* PowerShell では外部コマンドの出力を確実にまとめるため、`2>&1` より **`*>&1` を優先**する。

## テンプレート

```powershell
Set-Location <project-path>
$log = "cline_terminal_log/<logfile>.log"

<command> *>&1 |
  Out-File -FilePath $log -Encoding utf8

Get-Content $log -Tail 200
```

## 例：npm test（ChromeHeadless / watch無効）

```powershell
Set-Location netsuheni-app/netsuheni/client
$log = "npm-test.log"

npm test -- --watch=false --browsers=ChromeHeadless *>&1 |
  Out-File -FilePath $log -Encoding utf8

Get-Content $log -Tail 200
```

## 運用メモ

* ログファイルは実行ディレクトリ配下に生成される。必要に応じてパスを明示する。
* 追加で情報を絞りたい場合は、ログファイルに対して `Select-String` 等で抽出する（端末出力は最小限に）。
