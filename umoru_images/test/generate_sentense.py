
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "あなたはロボットの「ウモル」です。周囲の人の発言に影響されながら成長していきます。"},
    {"role": "user", "content": prompt}
  ]
)

print(response.choices[0].message.content.strip())