import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote
from jinja2 import Template

RAKUTEN_BASE_URL = "https://recipe.rakuten.co.jp" # 楽天レシピのURL

def create_search_recipes_url(ingredients): # 検索用のURLの作成
    query = quote(" ".join(ingredients)) # 材料をスペース区切って結合
    return f"{RAKUTEN_BASE_URL}/search/{query}"

def validate_recipe(recipe): # バリデーション
    if 'url' in recipe and 'image' in recipe and 'title' in recipe:
        return True
    return False

def fetch_recipes(ingredients): # レシピの取得
    url = create_search_recipes_url(ingredients)
    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')

    recipes = []

    for element in soup.select('.recipe_ranking__item'):
        image = element.select_one(".recipe_ranking__item img")['src'] # 画像
        title = element.select_one('.recipe_ranking__recipe_title').text # タイトル
        url = element.select_one('.recipe_ranking__item a')['href'] # URL

        full_url = urljoin(RAKUTEN_BASE_URL, url) if url else None
        
        new_recipe = {'url': full_url, 'image': image, 'title': title}
        
        if validate_recipe(new_recipe):
            recipes.append(new_recipe)
        else:
            print(f"Invalid recipe: {new_recipe}")
    
    return recipes

ingredients = ['卵', '牛乳'] # ここに材料を記述
recipes = fetch_recipes(ingredients)

# 取得したものをHTMLファイルに出力
template = Template('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recipes</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        .recipe {
            border: 1px solid #ddd;
            margin-bottom: 20px;
            padding: 10px;
            border-radius: 5px;
        }
        .recipe img {
            max-width: 100px;
            height: auto;
        }
        .recipe h2 {
            margin: 0;
            font-size: 1.5em;
        }
    </style>
</head>
<body>
    <h1>Recipes</h1>
    {% for recipe in recipes %}
    <div class="recipe">
        <h2>{{ recipe.title }}</h2>
        <img src="{{ recipe.image }}" alt="{{ recipe.title }}">
        <p><a href="{{ recipe.url }}">View Recipe</a></p>
    </div>
    {% endfor %}
</body>
</html>
''')

html_output = template.render(recipes=recipes)

with open('test/test-recipes.html', 'w', encoding='utf-8') as f:
    f.write(html_output)

print("Success!")