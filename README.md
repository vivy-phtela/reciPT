# 食材の画像からレシピをおすすめするアプリ
Render.comでデプロイ済み(https://recipt.onrender.com)

※ Render.comフリープランの仕様上，非アクティブ状態が15分続くと停止状態になる.停止状態からリクエストを送ると再度起動するが，応答までに時間がかかる(2分程度)．

## 流れ
食材の画像(例：冷蔵庫内の画像)をアップロード

↓

ChatGPTで画像認識して食材を出力

↓

出力された食材を編集・追加

↓

楽天レシピでの検索結果をスクレイピングして表示

<br>

## 使用技術
Flask，Docker，Supabase，OpenAI API

<br>

## 実行方法
### 1. 必要なライブラリのインストール

```
pip install -r requirements.txt
```

### 2. OpenAIのAPIとSupabaseのキーを入れる.envファイルを作成

```
OPENAI_API_KEY = "~"
SUPABASE_URL = "~"
SUPABASE_KEY = "~"
```

### 3. 実行

#### ◯ローカル環境での実行方法
ターミナルで以下のコマンドを実行
```
python3 app.py
```

#### ◯Docker環境での実行方法
Dockerデスクトップアプリを起動（アプリがない場合はインストール）して，ターミナルで以下のコマンドを実行
```
docker-compose up --build
```
