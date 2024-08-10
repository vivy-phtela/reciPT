# 食材の画像からレシピをおすすめするアプリ
Renderにてデプロイまで完了(https://recipt.onrender.com)

※ Render.comフリープランの仕様上，非アクティブ状態が15分続くと停止状態になる.停止状態からリクエストを送ると再度起動するが，応答までに時間がかかる(2分程度)．

## 流れ
【ユーザ】食材の画像(例：冷蔵庫内の画像)をアップロード

↓

画像をSupabaseのストレージに保存

↓

保存した画像をChatGPTのAPI(モデル：4o)に渡して，画像認識を行い，画像内の食材を出力

↓

【ユーザ】出力された食材を削除・編集・追加

↓

リストを楽天レシピの検索クエリに追加して検索．検索結果をスクレイピングして，タイトル・画像・URLを抽出．

↓

【ユーザ】指定した食材を使った料理の一覧を見る．

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
