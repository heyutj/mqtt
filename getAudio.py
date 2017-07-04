# -*- coding: utf-8 -*-
from pyaudio import PyAudio, paInt16
import numpy as np
from datetime import datetime
import wave

NUM_SAMPLES = 2000
SAMPLING_RATE = 8000


def save_wave_file(filename, data):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLING_RATE)
    for tmp in data:
        wf.writeframes(tmp)
    wf.close()


# 输入部分
pi = PyAudio()
istream = pi.open(format=paInt16, channels=1, rate=SAMPLING_RATE,
                  input=True, frames_per_buffer=NUM_SAMPLES)
save_buffer = []

# 输出部分
po = PyAudio()
ostream = po.open(format=paInt16, channels=1, rate=SAMPLING_RATE, output=True)

# 存储部分
# filename = datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + ".wav"

while True:
    string_audio_data = istream.read(NUM_SAMPLES)
    ostream.write(string_audio_data)
    save_buffer.append(string_audio_data)

pstream.close()
po.terminate()