import threading
import wave
from pyaudio import PyAudio,paInt16
import time

filename_add = 0
framerate=16000
NUM_SAMPLES=2000
channels=1
sampwidth=2
TIME=2
recordFile = 'audio_record/temp'

time_span = 3.0
ini_time = time.time()
start_time = time.time()
k = ini_time


def save_wave_file(filename,data):
    '''save the date to the wavfile'''
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()


def record():
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
	    string_audio_data = stream.read(NUM_SAMPLES)
	    my_buf.append(string_audio_data)
	    k = time.time()
	    if k-start_time >= time_span:
	        print('.')
	        #my_buf.append(string_audio_data)
	        save_wave_file(recordFile+str(filename_add)+'.wav',my_buf) #save wave file as the "temp.wav"
	        filename_add+=1
	        start_time = time.time()
	        my_buf =[]
	    if k-ini_time >= 30.0:
	        break
    stream.close()

record()