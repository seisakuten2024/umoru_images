from PIL import Image
import numpy as np
import MeCab
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt

# fontの指定
font_path="/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
# 色の設定
colormap="Paired"
# 形の設定
img_color = np.array(Image.open("/home/leus/Downloads/heart.png"))
mecab = MeCab.Tagger("-d /var/lib/mecab/dic/ipadic-utf8 -Ochasen")

def extract_noun(line):
    noun_list = []
    node = mecab.parseToNode(line)
    while node:
        if node.feature.split(",")[0] == "名詞" and node.feature.split(",")[1] in ["一般", "固有名詞"]:
            noun_list.append(node.surface)
        node = node.next
    return noun_list

#関数の設定
def mecab_tokenizer(path):
    # mecab= MeCab.Tagger('-Ochasen')
    
    token_list = []
    with open(path) as f:

        lines = f.readlines()
        for l in lines:
            token_list += extract_noun(l)
    return ' '.join(token_list)

def generate_wordcloud(file_path, save_image_path, display_image_path):
    words = mecab_tokenizer(file_path)
    wordcloud = WordCloud(
        background_color="white",
        width=800,
        height=800,
        font_path=font_path,
        colormap = colormap,
        # mask=img_color,
        stopwords=["する", "ある", "こと", "ない"],
        max_words=100,
    ).generate(words)

    plt.figure(figsize=(10,10))
    

    # image_colors = ImageColorGenerator(img_color)
    # plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    # plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
    plt.axis("off")
    plt.savefig(save_image_path)
    plt.savefig(display_image_path)
    plt.close()
    # plt.show()
        
# generate_wordcloud("data/test0714.txt")
