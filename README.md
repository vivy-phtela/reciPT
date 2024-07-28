# 食材の画像からレシピを自動でおすすめするアプリ


## 1. 必要なライブラリのインストール

```
pip install -r requirements.txt
```

## 2. OpenAIのAPIとSupabaseのキーを入れる.envファイルを作成

```
OPENAI_API_KEY = "~"
SUPABASE_URL = "~"
SUPABASE_KEY = "~"
```

## 3. 実行

### ローカル環境での実行方法
ターミナルで以下のコマンドを実行
```
python3 app.py
```

### Docker 環境での実行方法
Dockerデスクトップアプリを起動（アプリがない場合はインストール）して，ターミナルで以下のコマンドを実行
```
docker-compose up --build
```
