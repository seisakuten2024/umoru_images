from PIL import Image
import numpy as np
import MeCab
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt

#関数の設定
def mecab_tokenizer(path):
    # mecab= MeCab.Tagger('-Ochasen')
    mecab = MeCab.Tagger("-d /var/lib/mecab/dic/ipadic-utf8 -Ochasen")
    token_list = []
    with open(path) as f:
        lines = f.readlines()
        for l in lines:
            node = mecab.parseToNode(l)
            while node:
                if node.feature.split(",")[0] == "名詞" and node.feature.split(",")[1] in ["一般", "固有名詞"]:
                    token_list.append(node.surface)
                node = node.next
    return ' '.join(token_list)

font_path="/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
#関数の実行
# words = mecab_tokenizer("data/test-blog.txt")
# words = mecab_tokenizer("data/test0714.txt")

#色の設定
colormap="Paired"

img_color = np.array(Image.open("/home/leus/Downloads/heart.png"))
# img_color = np.array(Image.open("data/heart.jpg"))
# img_color = np.array(Image.open("data/heart.png"))
def generate_wordcloud(file_path):
    words = mecab_tokenizer(file_path)
    wordcloud = WordCloud(
        background_color="white",
        width=800,
        height=800,
        font_path=font_path,
        colormap = colormap,
        mask=img_color,
        stopwords=["する", "ある", "こと", "ない"],
        max_words=100,
    ).generate(words)

    # image_colors = ImageColorGenerator(img_color)
    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    # plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
    plt.axis("off")
    plt.show()
        
# generate_wordcloud("data/test0714.txt")
