#!/usr/bin/python3
# -*- coding: utf-8 -*-

import rospy
import time
from std_msgs.msg import String
from std_msgs.msg import Float32
from speech_recognition_msgs.msg import SpeechRecognitionCandidates
path = "data/test0714.txt"

class pubsubNode():
    def __init__(self):
        print("b")
        # Subscriberの作成
        self.sub = rospy.Subscriber("/speech_to_text", SpeechRecognitionCandidates , self.callback)
        # self.sub = rospy.Subscriber('/speech_to_text', Float32, self.callback)
        # Publisherの作成
        self.pub = rospy.Publisher('/generated_file', String, queue_size=1)

    def callback(self, data):
        print("hoge")
        pub_msg = String()
        speech = data.transcript
        print(speech[0])
        with open(path, mode='a', newline="\n") as f:
            f.write(speech[0] + "\n")
        f.close()
        rospy.loginfo(rospy.get_caller_id()+"I heard %s", speech)
        pub_msg.data = "y"
        self.publish(pub_msg)

    def publish(self, data):
        self.pub.publish(data)

if __name__ == '__main__':
    rospy.init_node('power_to_touch')
    print("a")
    time.sleep(3.0)
    node = pubsubNode()

    while not rospy.is_shutdown():
        rospy.sleep(0.1)
