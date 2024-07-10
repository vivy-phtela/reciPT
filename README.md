# 食材の画像からレシピを自動でおすすめするアプリ

## ローカル環境での実行方法

1.必要なライブラリのインストール

```
pip install -r requirements.txt
```

2.API キーを入れる config.py を作成

```
OPENAI_API_KEY = '{APIキー}'
```

3.実行

```
python3 app.py
```

## Docker 環境での実行方法

1.Docker アプリを起動（アプリがない場合はインストール）

2.Docker の立ち上げ

```
docker-compose up --build
```
