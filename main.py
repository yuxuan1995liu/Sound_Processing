#coding=utf-8
import wave
from pyaudio import PyAudio,paInt16
import socket
import threading
import time
import json
from watson_developer_cloud.websocket import RecognizeCallback
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import SpeechToTextV1

speech_to_text=SpeechToTextV1(
            username='1b163616-96bf-4ef9-9410-3b57185cc8f9',
            password='ndBvG4Rgqozk',
            url='https://stream.watsonplatform.net/speech-to-text/api'
        )


framerate=16000
NUM_SAMPLES=2000
channels=1
sampwidth=2
TIME=2
recordFile = 'audio_record/'

time_span = 5.0
time_span_2 = 600.0
ini_time = time.time()
start_time = time.time()
k = ini_time

currentStatus="normal"
currentText=""
finalText=""
emotion="none"
currentTone="none"

final_output_path = 'web/data/emotion_output.txt'
file = open(final_output_path, "w") 
file.close()
class EmotionGeter:
    def __init__(self):
        self.analyzer=ToneAnalyzerV3(
            version='2017-09-21',
            username='35a04742-f815-4073-b4cb-1a31d17dd10f',
            password='qv8CRsERYT00',
        )
        self.tone="none"

    def getEmotion(self,message):
        tone=self.getTone(message)
        return tone

    def getTone(self,message):
        tones = self.__getData(message)
        result = 'none'
        score = 0
        for tone in tones:
            if tone['score'] > score:
                score = tone['score']
                result = tone['tone_id']
        self.tone = result
        return result

    def __getData(self,message):
        content_type='text/plain'
        datas=self.analyzer.tone({"text": message},content_type)
        datas=datas['document_tone']['tones']
        return datas

class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_transcription(self, transcript):
        print(transcript)

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Service is listening')

    def on_transcription_complete(self):
        print('Transcription completed')

    def on_hypothesis(self, hypothesis):
        global currentText
        currentText=hypothesis
        print(hypothesis)

def save_wave_file(filename,data):
    '''save the date to the wavfile'''
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()
# recordFile='temp.wav'
# isRecording=False
# currentStatus="normal"
# currentText=""
# finalText=""
# emotion="none"
# currentTone="none"
filename_add = 0
def record_save_detection():
    global filename_add
    global k
    #t = threading.Timer(2.0,record).start() # set timer to run run() every 10 seconds
    global currentStatus
    global start_time
    global ini_time
    currentStatus="I'm listening..."
    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)
    
    my_buf=[]
    #count =0
    #count+=1
    while k>0:
        string_audio_data = stream.read(NUM_SAMPLES,exception_on_overflow = False)
        my_buf.append(string_audio_data)
        k = time.time()
        if k-start_time >= time_span:
            print('.')
            #my_buf.append(string_audio_data)
            save_wave_file(recordFile+'record.wav',my_buf) #save wave file as the "temp.wav"
            my_buf =[]
            getText()
            eg=EmotionGeter()
            global emotion
            global currentTone
            emotion=eg.getEmotion(finalText)
            print(emotion)
            with open(final_output_path,"w") as f:
                f.write(str(emotion))
            #f.close()
            start_time = time.time()
            filename_add+=1
        if k-ini_time >= time_span_2:
            break
    stream.close()
    # global filename_add
    # t = threading.Timer(10.0,run).start() # set timer to run run() every 10 seconds
    # global currentStatus
    # currentStatus="I'm listening..."

    # pa=PyAudio()
    # stream=pa.open(format = paInt16,channels=1,
    #                rate=framerate,input=True,
    #                frames_per_buffer=NUM_SAMPLES)
    # my_buf=[]
    # count=0
    # while isRecording:
    #     string_audio_data = stream.read(NUM_SAMPLES)
    #     my_buf.append(string_audio_data)
    #     count+=1
    #     print('.')
    # save_wave_file(recordFile+str(filename_add)+'.wav',my_buf) #save wave file as the "temp.wav"
    # filename_add+=1
    # stream.close()

# 运行流程，先录音，再转文字，再分析情绪
# def run():
#     record()
#     #isRecording = True
#     # getText()
#     # eg=EmotionGeter()
#     # global emotion
#     # global currentTone
#     # emotion=eg.getEmotion(finalText)
#     currentTone=eg.tone
#     global currentStatus
#     currentStatus="normal"

#如果不在函数里启动线程，会提示线程只能启动一次，在函数里可以反复启动
# def start():
#     recordThread = threading.Thread(target=run)
#     recordThread.start()

def speechToText():
    global currentStatus
    currentStatus="I'm thinking..."
    callback = MyRecognizeCallback()
    with open(recordFile+'record.wav', 'rb') as audio_file:
        content = speech_to_text.recognize_with_websocket(
            audio=audio_file,
            content_type='audio/l16;rate=16000',
            model='en-US_BroadbandModel',
            recognize_callback=callback
        )

def getText():
    global currentStatus
    currentStatus = "I'm thinking..."
    text=""
    with open(recordFile+'record.wav', 'rb') as audio_file:
        content = speech_to_text.recognize('en-US_NarrowbandModel', #zh-CN_NarrowbandModel
                                               audio=audio_file,
                                               content_type='audio/wav',
                                               word_confidence=True,
                                               )
    if content['results']!=[]:
        text=content['results'][0]['alternatives'][0]['transcript']
    print(text)
    global currentText
    global finalText
    currentText=text
    finalText=text

record_save_detection()
