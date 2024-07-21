import rospy
from sound_play.libsoundplay import SoundClient

rospy.init_node('say_node')

client = SoundClient(sound_action='robotsound', sound_topic='robotsound')

client.say('hello!')
client.say('こんにちは', voice='ja')
