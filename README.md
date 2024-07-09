# 食材の画像からレシピを自動でおすすめするアプリ

## レシピのスクレイピング

必要なライブラリのインストール

```
pip install -r requirements.txt
```

API キーを入れる config.py を作成

```
OPENAI_API_KEY = '{キー}'
```

get_recipe.py の ingredients に材料を入れて実行

```
python3 get_recipe.py
```

test フォルダに html ファイルが生成される．
Live server で html ファイルを開いて確認する．
