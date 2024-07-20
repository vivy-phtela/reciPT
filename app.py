from flask import Flask, request, render_template, redirect, url_for, flash
from lib.extract_ingredients import get_ingredients_list
from lib.get_recipes import fetch_recipes
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.secret_key = 'secret_key'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('ファイルが選択されていません')
            return redirect(request.url)
        if file and allowed_file(file.filename):            
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            ingredients_list = get_ingredients_list(file_path)  # ChatGPTのAPIを使用
            if os.path.exists(file_path):
                os.remove(file_path)
            # ingredients_list = ["じゃがいも", "にんじん"]
            return render_template('edit_ingredients.html', ingredients=ingredients_list)
        else:
            flash('許可されていないファイル形式です')
            return redirect(request.url)
    else:
        return redirect(url_for('index'))

@app.route('/recipes', methods=['POST'])
def show_recipes():
    try:
        ingredients_list = request.form.getlist('ingredients')

        recipes = fetch_recipes(ingredients_list)

        return render_template('recipes.html', recipes=recipes, ingredients=ingredients_list)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
