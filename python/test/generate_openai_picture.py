import matplotlib.pyplot as plt
from openai import OpenAI
client = OpenAI()
import requests
from PIL import Image
from io import BytesIO
response = client.images.generate(
  model="dall-e-3",
  # prompt="air inflatable robot that wants to play tennis, ping-pong and sup",
    # Focus on specific, visually representable elements. Describe actions and scenarios rather than abstract concepts. Avoid ambiguous language that could be interpreted as including text.
    prompt="Please write a scene which is a photographic, clean and minimalist art style. Focus on specific, visually representable elements. Avoid ambiguous language that could be interpreted as including text. 白くて丸いロボットのウモルが「ウモルはね、さまざまな体験をしてみたい。それはね、いろいろなことに挑戦することで成長できると思うからだよ。例えば、サップで水面の感覚を楽しんだり、卓球で反射神経を鍛えたり、論文で知識を深めたりしたいな。」と想像しています。",
  size="1024x1024",
  quality="standard",
  n=1,
)

def save_image(url, filename):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    # 画像を表示
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    
    plt.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False, bottom=False, left=False, right=False, top=False)

    plt.imshow(img)
    plt.show()
    img.save(filename)

image_url = response.data[0].url
# image_url = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-H5wqhCH0LFrmSQUAYIL7I6D9/user-4vR4rzWmMoHxhft4Tg9Du9tG/img-su4TAsIjYbLfSMNtbcVEKD9q.png?st=2024-07-20T10%3A52%3A59Z&se=2024-07-20T12%3A52%3A59Z&sp=r&sv=2023-11-03&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-07-19T23%3A30%3A00Z&ske=2024-07-20T23%3A30%3A00Z&sks=b&skv=2023-11-03&sig=ayIZGZAhHKaJVDoUGJX/3p1z3KTA0he2CpO6QlNc/As%3D"

print(image_url)
save_image(image_url, "test.jpg")
