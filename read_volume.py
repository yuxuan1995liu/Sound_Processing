import threading
import wave
import sounddevice as sd
import numpy as np
from pyaudio import PyAudio,paInt16
import time

duration = 10  # seconds
final_output_path = 'volume.txt'
def print_sound(indata, outdata, frames, time, status):
    volume_norm = np.linalg.norm(indata)*10
    with open(final_output_path,"a") as f:
        f.write(str(volume_norm)+ '\n')
    print ("|" * int(volume_norm))

with sd.Stream(callback=print_sound):
    sd.sleep(duration * 1000)