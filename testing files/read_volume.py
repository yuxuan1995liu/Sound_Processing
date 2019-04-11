import threading
import wave
from wavefile import WaveReader
from pyaudio import PyAudio,paInt16
import time

recordFile = 'audio_record/temp0.wav'

with WaveReader(recordFile) as r:
    for data in r.read_iter(size=512):
        left_channel = data[0]
        volume = np.linalg.norm(left_channel)
        print volume
