from io import BytesIO
from itertools import count
import requests
import torch
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image, ImageFilter

## カスタマイズ部分
idevice =  "mps" #デバイス名(macの場合はmpsを使う)
model_name = "CompVis/stable-diffusion-v1-4" #モデル名
file_path ="data/robots_wrestling.png" #元画像のファイルパス
prompt = "A fantasy landscape, trending on artstation" #呪文部分
image_size = (768,512) #横幅と高さ。2の倍数の値で入力。

data_len = 100 #実行回数

## 画像作成
def createImage(output_name:str,count:int):

    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
        model_name,
        use_auth_token=True
    ).to(device)

    init_image =  Image.open(file_path).convert("RGB").resize(image_size)
    images = pipe(prompt=prompt, image=init_image, strength=0.75, guidance_scale=7.5).images
    images[0].save(output_name + '_' +str(count).zfill(4) +'.jpg')


## 実行部分
for i in range(data_len):
    print(str(i).zfill(4) + "枚目の画像を出力中です。")
    createImage("output",i)
