import config_key
from openai import OpenAI
import base64
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI APIキーの設定
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def encode_image_from_url(image_url):  # 画像URLから画像をダウンロードし、Base64にエンコード
    response = requests.get(image_url)
    image_data = response.content
    return base64.b64encode(image_data).decode("utf-8")

def parse_ingredients(ingredients_text):  # 出力結果の整形
    ingredients_list = [line.strip('- ').strip() for line in ingredients_text.split('\n') if line.strip()]
    return ingredients_list

def get_ingredients_list(image_url):  # ChatGPTのAPIを使用して画像から材料リストを抽出
    base64_image = encode_image_from_url(image_url)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": [
                {"type": "text", "text": "Please list the specific ingredients contained in this image in Japanese only and in short words. Output a list of ingredients."},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"}
                }
            ]}
        ],
        temperature=0.0,
    )

    res = response.choices[0].message.content
    ingredients_list = parse_ingredients(res)
    return ingredients_list