# プロキシエラー解決ガイド

## 問題
`407 Proxy Authentication Required` エラーが発生し、pipでパッケージをインストールできない。

## 原因
企業プロキシサーバー `proxy-metro.ibis.intec.co.jp:8080` が認証を要求している。

## 解決策（優先度順）

### 解決策1: IT管理者に依頼（推奨）
```cmd
# IT管理者に以下を依頼
1. プロキシ認証の自動設定
2. PyPI (pypi.org, files.pythonhosted.org) への直接アクセス許可
3. 社内PyPIミラーサーバーの提供
```

### 解決策2: ユーザーレベルインストール
```cmd
# 管理者権限不要でインストール
pip install --user openpyxl pandas tabulate
```

### 解決策3: オフラインインストール
```cmd
# 別の環境でwheelファイルをダウンロード
pip download openpyxl pandas tabulate -d wheels/

# オフラインでインストール
pip install --find-links wheels/ --no-index openpyxl pandas tabulate
```

### 解決策4: 認証情報付きプロキシ設定
```cmd
# 環境変数に認証情報を設定（セキュリティリスクあり）
set HTTP_PROXY=http://username:password@proxy-metro.ibis.intec.co.jp:8080
set HTTPS_PROXY=http://username:password@proxy-metro.ibis.intec.co.jp:8080
```

## 使用方法
1. `run_final.cmd` を実行
2. エラーが発生した場合、上記の解決策を順番に試す
3. 成功したら通常通り使用可能

## 注意事項
- 認証情報をスクリプトに直接記載しない
- 可能な限りIT管理者と連携する
- セキュリティポリシーを遵守する
