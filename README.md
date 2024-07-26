# 環境構築
1. jsk_3rdpartyをcloneしてくる
2. ros_speech_recognitionとvoicevoxをbuildする
（voicevoxについては、[voicevox-docker]([url](https://github.com/iory/jsk_3rdparty/tree/voicevox-docker/3rdparty/voicevox))に従うと速く音声合成可能）

# 実行手順
## setup
```
$ mkdir -p ~/seisakuten_ws/src
$ cd ~/seisakuten_ws
$ catkin init
$ cd ~/ros/seisakuten_ws/src
$ git clone https://github.com/seisakuten2024/umoru_images
$ catkin build
```
## command
```
$ roslaunch ros_speech_recognition speech_recognition.launch language:=ja-JP
```
```
$ roslaunch voicevox voicevox_texttospeech.launch ip:=<IP docker is running>
```
```
$ roslaunch umoru_images umoru_images.launch
```
