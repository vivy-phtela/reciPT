from flask import Flask, request, render_template, redirect, url_for
import lib.extract_ingredients as extract_ingredients
import lib.get_recipes as get_recipes
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# ファイルの保存フォルダを作成
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return redirect(url_for('show_recipes', image_path=file_path))
    return redirect('/')

@app.route('/recipes')
def show_recipes():
    try:
        image_path = request.args.get('image_path')

        # ingredients_list = extract_ingredients.get_ingredients_list(image_path) # 画像から材料リストを抽出
        # print(ingredients_list)
        ingredients_list = ['トマト', '白菜'] # テスト用

        recipes = get_recipes.fetch_recipes(ingredients_list) # 材料リストを使用してレシピを取得

        return render_template('recipes.html', recipes=recipes)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
