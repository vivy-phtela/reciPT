from flask import Flask, request, render_template, redirect, url_for, flash
from lib.extract_ingredients import get_ingredients_list
from lib.get_recipes import fetch_recipes
from werkzeug.utils import secure_filename
from supabase import create_client, Client
import os
import mimetypes
import uuid
from dotenv import load_dotenv
from waitress import serve

app = Flask(__name__)
app.secret_key = 'secret_key'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

load_dotenv()
url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(url, key)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files['file']

    # ファイルが空かどうかチェック
    if file.filename == '':
        flash('ファイルが選択されていません')
        return redirect(url_for('index'))

    # 許可された拡張子かどうかチェック
    if not allowed_file(file.filename):
        flash('許可されていないファイル形式です')
        return redirect(url_for('index'))
    
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

    # アップロードされたファイルのURLを取得
    file_url = f"{url}/storage/v1/object/public/recipt-image/{unique_filename}"

    print("ファイル名",unique_filename)

    # ファイルのURLを使用してget_ingredients_list関数を呼び出す
    ingredients_list = get_ingredients_list(file_url)

    # DBからファイルを削除
    supabase.storage.from_("recipt-image").remove([unique_filename])
        
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
    # app.run(host='0.0.0.0', port=5000, debug=True)
    serve(app, host='0.0.0.0', port=5000, threads=10)
