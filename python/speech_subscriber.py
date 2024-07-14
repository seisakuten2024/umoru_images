#!/usr/bin/env python
import rospy
from speech_recognition_msgs.msg import SpeechRecognitionCandidates
path = "data/test0714.txt"

def callback(data):
    speech = data.transcript
    with open(path, mode='a', newline="\n") as f:
        f.write(speech[0] + "\n")
    rospy.loginfo(rospy.get_caller_id()+"I heard %s", speech)
    
def listener():

    # in ROS, nodes are unique named. If two nodes with the same
    # node are launched, the previous one is kicked off. The 
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaenously.
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("speech_to_text", SpeechRecognitionCandidates , callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
        
if __name__ == '__main__':
    listener()
