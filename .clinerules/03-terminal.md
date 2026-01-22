# PowerShell Terminal Assistant Rules

## MUST
- ターミナルでコマンドを実行する際はコマンドの末尾に必ず下記をつけること
```
 | Select-Object -Last 200
```
- アプリケーションの起動は常にバックグラウンド起動にすること
```powershell
Start-Process PowerShell -ArgumentList "-Command", "cd return-workflow-system; mvn spring-boot:run" -WindowStyle Minimized
```