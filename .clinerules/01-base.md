# Cline 基本ルール

## セキュリティ/巨大ファイルの扱い
- `.env` やAPIキー等の**機密情報は**読み書き禁止。該当ファイルは `.clineignore` に明示する。
- 禁止：read_fileで全量読み／無制限出力
- 必須：検索→抜粋→必要なら周辺追加（200〜500行程度で上限）
  - 末尾: Get-Content <file> -Tail 200
  - 検索: Select-String -Path <file> -Pattern 'ERROR|FATAL|Exception|Traceback|panic' | Select-Object -Last 50
  - 周辺: Get-Content <file> -TotalCount $end | Select-Object -Skip ($start-1) > log_excerpt.txt
- 読むのは抜粋ファイル（log_excerpt.txt）のみ

## コマンド実行時の注意
- コマンドはPowershellに対応しているものを使用
- コマンド実行前にそのコマンドが使用可能か**必ず**確認する
- 使用不可の場合、作業一時中断しコマンドのインストールやセットアップを行う
- 巨大なターミナル出力は禁止。出力が多いコマンドは必ずログに保存し、表示は末尾200行のみ：
```
mvn clean compile *> mvn.log; Get-Content .\mvn.log -Tail 200; exit $LASTEXITCODE
```


