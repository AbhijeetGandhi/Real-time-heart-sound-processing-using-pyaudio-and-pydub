from pydub import AudioSegment
from pydub.scipy_effects import low_pass_filter as lf
import pyaudio
from pydub.playback import play
from scipy.io.wavfile import write
import threading as th
import numpy as np
import matplotlib.pyplot as plt

chunk = 8192
audio_format = pyaudio.paInt16
sample_width = 2
channels = 1
sample_rate = 16000 
keep_going = True

def key_capture_thread():
    global keep_going
    input()
    keep_going = False

def filter_data(sound):
    sound = sound.low_pass_filter(120,order=5)
    return sound.normalize()

p = pyaudio.PyAudio()
stream = p.open(format=audio_format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk,
               )

fig, ax = plt.subplots(2,figsize=(14,6))
x = np.arange(0, 2*chunk, 2)
ax[0].set_ylim(-5000, 5000)
ax[0].set_xlim(0, chunk)
ax[1].set_ylim(-30000, 30000)
ax[1].set_xlim(0, chunk)
line, = ax[0].plot(x, np.random.rand(chunk))
line1, = ax[1].plot(x, np.random.rand(chunk))

final_audio = AudioSegment.empty()
while keep_going:
    th.Thread(target=key_capture_thread, args=(), name='key_capture_thread', daemon=True).start()
    data = stream.read(chunk)
    
    sound = AudioSegment(data,sample_width=sample_width, channels=channels, frame_rate=sample_rate)
    filtered_data = filter_data(sound)
    final_audio += filtered_data

    line.set_ydata(np.frombuffer(data, np.int16))
    line1.set_ydata(filtered_data.get_array_of_samples())
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.01)

final_audio.export("output.wav",format="wav")
    
