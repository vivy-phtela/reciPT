from flask import Flask, jsonify
import lib.extract_ingredients as extract_ingredients
import lib.get_recipes as get_recipes

app = Flask(__name__)

@app.route('/')
def hello_world():
    try:
        image_path = "image/image1.jpeg"

        # 画像から材料リストを抽出
        ingredients_list = extract_ingredients.get_ingredients_list(image_path)
        print(ingredients_list)

        # 材料リストを使用してレシピを取得
        recipes = get_recipes.fetch_recipes(ingredients_list)
        for recipe in recipes:
            print(recipe)

        return jsonify(recipes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)