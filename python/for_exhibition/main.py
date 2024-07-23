#!/usr/bin/python3
# -*- coding: utf-8 -*-

import rospy
import time
import module
from std_msgs.msg import String
from std_msgs.msg import Bool
from std_msgs.msg import Float32
from speech_recognition_msgs.msg import SpeechRecognitionCandidates
import json
from PIL import Image
from io import BytesIO
import numpy as np
import MeCab
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from openai import OpenAI
import re
import datetime
import requests
from sound_play.libsoundplay import SoundClient
client = OpenAI()

raw_data_path = "data/raw/test0719.txt"
raw_data_path_for_wordcloud = "data/raw/test0719_for_wordcloud.txt"
analyzed_data_path = "data/analyzed/test0719.json"
html_data_path = "data/html/test0719.html"
print("generate picture")

class speechSubGeneratedFilePubNode():
    """
    音声認識結果をsubscribeする→ファイルに書き込む→書き込み完了をpublishする
    """
    def __init__(self):
        # Subscriberの作成
        self.sub = rospy.Subscriber("/speech_to_text", SpeechRecognitionCandidates , self.callback)
        # Publisherの作成
        self.pub = rospy.Publisher('/generated_file', Bool, queue_size=1)
        # self.pub = rospy.Publisher('/aaa', Bool, queue_size=1)
        # self.pub = rospy.Publisher('/aaa', String, queue_size=1)
        time.sleep(1)

    def callback(self, data):
        pub_msg = Bool()

        speech = data.transcript
        print(speech[0])
        rospy.loginfo(rospy.get_caller_id()+"I heard %s", speech)

        # 音声認識情報をファイルに書き込む
        with open(raw_data_path, mode='a', newline="\n") as raw_file:
            with open(raw_data_path_for_wordcloud, mode="a", newline="\n") as raw_file_for_wordcloud:
                raw_file_for_wordcloud.write(speech[0]+ "\n")
            raw_file.write(speech[0] + "\n")
        raw_file.close()
        raw_file_for_wordcloud.close()

        # 音声認識情報から名詞だけを抽出し、jsonファイルのカウントを更新する書き込む
        with open(analyzed_data_path, mode='rt') as analyzed_file: 
            noun_counter_dict = json.load(analyzed_file)
        analyzed_file.close()
        noun_list = module.extract_noun(speech[0])
        for noun in noun_list:
            if noun_counter_dict.get(noun) == None:
                noun_counter_dict[noun] = 1
            else:
                noun_counter_dict[noun] += 1
        with open(analyzed_data_path, mode="wt") as analyzed_file:
	        json.dump(noun_counter_dict, analyzed_file, ensure_ascii=False)
        analyzed_file.close()
        print("json file done")

        pub_msg.data = True
        self.publish(pub_msg)

    def publish(self, data):
        self.pub.publish(data)

class generatePromptForSentenceNode():
    def __init__(self):
        #rospy.init_node('generate_picture')
        time.sleep(3)
        self.pub = rospy.Publisher('/prompt_to_generate_sentence', String, queue_size=1)
        # Subscriberの作成
        self.sub = rospy.Subscriber("/generated_file", Bool, self.callback)

    def callback(self, data):
        last_spoken_word = "アイスクリーム"
        with open(analyzed_data_path, mode='rt') as analyzed_file:
            noun_counter_dict = json.load(analyzed_file)
        analyzed_file.close()
        with open(raw_data_path, mode="r") as raw_file:
            lines = raw_file.readlines()
        
        for line in lines[::-1]:
            noun_list = module.extract_noun(line)
            length = len(noun_list)
            if length != 0:
                last_spoken_word = noun_list[0]
                break
        
        # print("最大出現語=", max(noun_counter_dict, key=noun_counter_dict.get))
        print("最後に話されたのは", last_spoken_word)
        sorted_dict = sorted(noun_counter_dict.items(), key=lambda x:x[1], reverse=True)
        words_list = [last_spoken_word]
        for i in range(2):
            words_list.append(sorted_dict[i][0])
        print("in generate picture node")

        pub_msg = String()
        prompt = self.generate_prompt(words_list)
        print(prompt)
        pub_msg.data = prompt
        self.publish(pub_msg)

    def generate_prompt(self, words_list):
        length =len(words_list)
        what_to_do = "「"
        for i in range(length):
            what_to_do += words_list[i]
            if i != length -1:
                what_to_do += "と"
        what_to_do += "をしたい」"
        return "あなたはロボットの「ウモル」です。周囲の人の発言に影響されながら成長していきます。今日出会った人に" + what_to_do + "と言われました。そのとき、あなたは何をしたいと思いますか。「ウモルはね、〜〜したい」というように短文で答えてください。ただし、別の言葉で抽象化して言い換えて、自然な日本語を心がけてください。また、その理由も「それはね、〜〜だと思うからだよ。」というように付け足してください。そのあとに、「例えば〜〜をしたいな」というように、具体例も足してください。"

    def publish(self, data):
        self.pub.publish(data)


class generateTextResponseAndPromptForPictureNode():
    def __init__(self):
        self.sub = rospy.Subscriber("/prompt_to_generate_sentence", String, self.callback)
        self.pub_prompt = rospy.Publisher('/prompt_to_generate_picture', String, queue_size=1)
        self.pub_response = rospy.Publisher('/text_response', String, queue_size=1)
        print("generate prompt")
        time.sleep(1)

    def callback(self, data):
        sentence_response = self.generate_umoru_text_response(data.data)
        print("umoruの返答" + sentence_response)
        pub_response_msg = String()
        pub_response_msg.data = sentence_response
        self.publish_response(pub_response_msg)
        prompt = self.generate_prompt_for_picture(sentence_response)
        pub_prompt_msg = String()
        pub_prompt_msg.data = prompt
        self.publish_prompt(pub_prompt_msg)

    def publish_prompt(self, data):
        self.pub_prompt.publish(data)

    def publish_response(self, data):
        self.pub_response.publish(data)
    
    def generate_umoru_text_response(self, prompt):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたはロボットの「ウモル」です。周囲の人の発言に影響されながら成長していきます。"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    
    def generate_prompt_for_picture(self, sentence_response):
        return "Please write a scene which is a photographic, clean and minimalist art style. Focus on specific, visually representable elements. Avoid ambiguous language that could be interpreted as including text. 白くて丸いロボットのウモルが「"+ sentence_response + "」と想像しています。"


class generatePictureNode():
    def __init__(self):
        self.sub = rospy.Subscriber("/prompt_to_generate_picture", String, self.callback)
        print("generate picture")
        time.sleep(1)

    def callback(self, data):
        image_url = self.generate_umoru_picture_response(data.data)
        self.generate_HTML(html_data_path, image_url)
        self.save_image(image_url)

    def generate_umoru_picture_response(self, prompt):
        response = client.images.generate(
            model="dall-e-3",
            # prompt="air inflatable robot that wants to play tennis, ping-pong and sup",
                # Focus on specific, visually representable elements. Describe actions and scenarios rather than abstract concepts. Avoid ambiguous language that could be interpreted as including text.
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
            )
        image_url = response.data[0].url
        print(image_url)
        return image_url

    def generate_HTML(self, path, url):
        new_line = '<img src="' + url + '">\n'
        with open(path) as html_file:
            lines = html_file.readlines()
        for i in range(len(lines)):
            print(lines[i])
            if "img src" in lines[i]:
                lines[i] = new_line
                print("aaa")
                break
        with open(path, mode="w") as html_file:
            html_file.writelines(lines)

    def save_image(self, url):
        now = datetime.datetime.now()
        filename = "data/images/pictures/log_" + now.strftime('%Y%m%d_%H%M%S') + ".png"
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        """ # 画像を表示
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        
        plt.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False, bottom=False, left=False, right=False, top=False)

        plt.imshow(img)
        plt.show() """
        img.save(filename)

class generateWordcloudNode():
    def __init__(self):
        time.sleep(3)
        # Subscriberの作成
        self.sub = rospy.Subscriber("/generated_file", Bool, self.callback)

    def callback(self, data):
        now = datetime.datetime.now()
        filename_for_save = "data/images/wordclouds/log_" + now.strftime('%Y%m%d_%H%M%S') + ".png"
        filename_for_display = "data/images/wordclouds/display.png"
        module.generate_wordcloud(raw_data_path_for_wordcloud, filename_for_save, filename_for_display)
        print("making wordcloud")

class speakGeneratedText():
    def __init__(self):
        time.sleep(3)
        # Subscriberの作成
        self.sub = rospy.Subscriber("/text_response", String, self.callback)

    def callback(self, data):        
        client = SoundClient(sound_action='robotsound_jp', sound_topic='robotsound_jp')
        client.say(data.data, voice='白上虎太郎-ノーマル')

if __name__ == '__main__':
    rospy.init_node("test_node")
    node1 = speechSubGeneratedFilePubNode()
    node2 = generatePromptForSentenceNode()
    node3 = generateTextResponseAndPromptForPictureNode()
    node4 = generatePictureNode()
    node5 = speakGeneratedText()
    
    # node3 = generatePictureNode()
    # node4 = generateSentenceNode()
    node5 = generateWordcloudNode()

    while not rospy.is_shutdown():
        rospy.sleep(0.1)
