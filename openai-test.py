import config
from openai import OpenAI

client = OpenAI(api_key=config.OPENAI_API_KEY)

# call new API
response = client.chat.completions.create(model="gpt-3.5-turbo",
messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Say this is a test"}
])

print(response.choices[0].message.content.strip())
