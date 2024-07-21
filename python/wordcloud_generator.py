#!/usr/bin/env python
import rospy
from speech_recognition_msgs.msg import SpeechRecognitionCandidates
from generate_wordcloud import generate_wordcloud
from std_msgs.msg import String

path = "data/test0714.txt"
import time

def callback(data):
    generate_wordcloud(path)
    
def generated_file_subscriber():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("generated_file", String , callback)
    rospy.spin()
        
if __name__ == '__main__':
    generated_file_subscriber()
