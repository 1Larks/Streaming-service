import Network_Handler
import threading
import pyaudio
import numpy as np
import subprocess
import time

BUFFERSIZE = 4096
STOP_BUFF = 'STOP'.zfill(BUFFERSIZE).encode()

#Temporary decorator function for debugging and optimization
def time_func(func):
    def inner(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(f'function name: {func.__name__}, time took: {time.time()-start}')
        return res
    
    return inner


class Stream_Handler:
    def __init__(self, network_handler: Network_Handler.Network_Handler) -> None:
        self.playing = False
        
        self.bytes_recieved = 0
        self.prev_sample_rate = None
        self.prev_channels = None
        self.network_h = network_handler

        self.chunks = []
        
        self.sample_rate = None
        self.channels = None
        
        self.audio = pyaudio.PyAudio()
        self.stream = None
        
    def _play_song(self):
        while len(self.chunks) == 0:
            continue
        
        info = self.chunks.pop(0).decode().strip('0').split(':')
        self.sample_rate, self.channels = int(info[0]), int(info[1])
        
        self.stream = self.audio.open(self.sample_rate, self.channels, pyaudio.paInt16, False, True, frames_per_buffer=BUFFERSIZE)
        
        while self.playing:
            if len(self.chunks) > 0:
                current_buffer = self.chunks.pop(0)
                if current_buffer == STOP_BUFF:
                    self.playing = False
                    break
                
                pcm_chunk = self.decode_mp3_chunk(current_buffer)
                
                
                self.stream.write(pcm_chunk)
        
        self.stream.close()
    @time_func
    def decode_mp3_chunk(self, mp3_chunk):
        # Use ffmpeg to decode MP3 chunk to raw PCM audio data
        process = subprocess.Popen([
            'ffmpeg.exe',
            '-i', 'pipe:0',       # Read from stdin
            '-f', 's16le',        # Set output format to signed 16-bit little-endian
            '-ac', f'{self.channels}',      # Set number of audio channels to stereo
            '-ar', f'{self.sample_rate}',   # Set audio sample rate to 44100 Hz
            '-'],                 # Output to stdout
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=mp3_chunk)
        if process.returncode == 0:
            pcm_data = np.frombuffer(stdout, dtype=np.int16)
            return pcm_data
        else:
            print("Error decoding MP3 chunk:", stderr)
            return None
    

    def start_stream(self):
        threading.Thread(target=self._play_song).start()
    
    def stop_stream(self):
        self.playing = False