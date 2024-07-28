from flask import Flask, request, render_template, redirect, url_for, flash
from lib.extract_ingredients import get_ingredients_list
from lib.get_recipes import fetch_recipes
from werkzeug.utils import secure_filename
from supabase import create_client, Client
import config_key
import os
import mimetypes
import uuid

app = Flask(__name__)
app.secret_key = 'secret_key'

url = config_key.SUPABASE_URL
key = config_key.SUPABASE_KEY
supabase: Client = create_client(url, key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files['file']
    original_filename = secure_filename(file.filename)
    
    # ファイル名にUUIDを追加してユニークにする
    unique_filename = f"{uuid.uuid4()}_{original_filename}"
    
    file_path = os.path.join('/tmp', unique_filename)
    file.save(file_path)

    # ファイルのMIMEタイプを取得
    mime_type, _ = mimetypes.guess_type(file_path)

    # Supabaseのストレージにファイルをアップロード
    with open(file_path, 'rb') as f:
        response = supabase.storage.from_("recipt-image").upload(unique_filename, f.read(), {
            "content-type": mime_type
        })

    # レスポンスのエラーチェック
    if response.status_code != 200:
        flash('File upload failed: ' + response.json().get('message', 'Unknown error'))
        return redirect(url_for('index'))

    # アップロードされたファイルのURLを取得
    file_url = f"{url}/storage/v1/object/public/recipt-image/{unique_filename}"

    # ファイルのURLを使用してget_ingredients_list関数を呼び出す
    ingredients_list = get_ingredients_list(file_url)
        
    return render_template('edit_ingredients.html', ingredients=ingredients_list)

@app.route('/edit_ingredients')
def edit_ingredients():
    ingredients = request.args.getlist('ingredients')
    return render_template('edit_ingredients.html', ingredients=ingredients)

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
