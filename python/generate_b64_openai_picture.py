from openai import OpenAI

import cv2
import numpy as np
import base64
from PIL import Image
from io import BytesIO

client = OpenAI()

encode_file = r"encode_file.txt"
response = client.images.generate(
  model="dall-e-3",
  # prompt="air inflatable robot that wants to play tennis, ping-pong and sup",
    # Focus on specific, visually representable elements. Describe actions and scenarios rather than abstract concepts. Avoid ambiguous language that could be interpreted as including text.
    prompt="Please write a scene which is a photographic, clean and minimalist art style. Focus on specific, visually representable elements. Avoid ambiguous language that could be interpreted as including text. 白くて丸いロボットのウモルが「ウモルはね、さまざまな体験をしてみたい。それはね、いろいろなことに挑戦することで成長できると思うからだよ。例えば、サップで水面の感覚を楽しんだり、卓球で反射神経を鍛えたり、論文で知識を深めたりしたいな。」と想像しています。",
  size="1024x1024",
  quality="standard",
  n=1,
  response_format="b64_json",
)


# 'response.data[0].b64_json'がDALL·E 3から受け取ったBase64 JSONデータであると仮定
image_data = base64.b64decode(response.data[0].b64_json)
pil_image = Image.open(BytesIO(image_data)).resize((256, 256))
image_data = BytesIO()
pil_image.save(image_data, format='JPEG', quality=80)
compressed_image = base64.b64encode(image_data.getvalue()).decode('utf-8')
str_image = 'data:image/jpeg;base64,' + compressed_image
print(str_image)

# with open(encode_file,"wb") as f:
#     f.write(response.data[0].b64_json)


# #Base64でエンコードされたファイルのパス
# #デコードされた画像の保存先パス
# image_file=r"decode.jpg"

# with open(encode_file, 'rb') as f:
#     img_base64 = f.read()

# #バイナリデータ <- base64でエンコードされたデータ  
# img_binary = base64.b64decode(img_base64)
# jpg=np.frombuffer(img_binary,dtype=np.uint8)

# #raw image <- jpg
# img = cv2.imdecode(jpg, cv2.IMREAD_COLOR)
# #画像を保存する場合
# cv2.imwrite(image_file,img)

# #表示確認
# cv2.imshow('window title', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
