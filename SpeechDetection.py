import speech_recognition as sr
import time
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write, read

class SpeechDetection:
    def __init__(self,format=np.int16,channel=1,rate=44100,duration=5):
        # Parameters for recording
        self.format = format
        self.channel = channel
        self.rate = rate
        self.duration = duration
        # Create a queue for storing audio chunks
        self.buffer = []
        self.denoised_buffer = []
        self.recognize_flag = False
    def record(self):
        start_time = time.time()
        print(f"-------------------------------------------------\n",
              f"Recording...")
        self.buffer = sd.rec(int(self.duration * self.rate), samplerate=self.rate, 
                           channels=self.channel, dtype=self.format)
        sd.wait()
        print(f"Stopped recording.\n",
              f"Time elapsed: {time.time()-start_time} sec")
        return self.buffer.flatten()
    
    def save_wav(self, filename, recording):
        self.buffer = np.asarray(recording, self.format)
        write(filename = filename, rate=self.rate, data=self.buffer)
        self.recognize_flag = True
    def recognize(self) -> str:
        if self.recognize_flag:
            self.recognize_flag = False
            filename = f"audio_chunk_{self.duration}s.wav"
        	# Initialize the recognizer
            r = sr.Recognizer()
            src = read(filename)
            # Listen for data
            with sr.AudioFile(filename) as src:
                audio = r.record(src)
                try:
                    text = r.recognize_google(audio)
                    text = text.lower()
                    return text
                except sr.UnknownValueError:
                    pass
                except sr.RequestError:
                    pass
            return None
        else: return None
    def checkMamaPapa(self,prt=True):
        recording = self.record()
        self.save_wav(f"audio_chunk_{self.duration}s.wav",recording)
        text = self.recognize()
        if prt: print(f"Baby said: {text}")
        return text


if __name__ == "__main__":
    sp = SpeechDetection()
    while True:
        try:    
            out = sp.checkMamaPapa()
        except KeyboardInterrupt:
            print("Interrupt")
    