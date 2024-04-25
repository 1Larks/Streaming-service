import Network_Handler
import threading
import pyaudio
import numpy as np
import subprocess
import io
import wave
import sounddevice as sd


STOP_BUFF = 'STOP'.zfill(Network_Handler.BUFFSIZE).encode()

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
    
        self.stream = sd.RawOutputStream(self.sample_rate, 1152, dtype='int16')
        self.stream.start()
        while self.playing:
            try:
                current_buffer = None
                if len(self.chunks) > 0:
                    current_buffer = self.chunks.pop(0)
                if current_buffer == STOP_BUFF:
                    self.playing = False
                    break
                if current_buffer is not None:
                    pcm_chunk = self.decode_mp3_chunk(current_buffer)
                    
                    arr = np.frombuffer(pcm_chunk, np.int16)
                    arr = np.reshape(arr, (-1, self.channels))
                    
                    # the fixed length for every subarray should be
                    # the length of the pcm chunk // the GCD of the two constant PCM chunk sizes (16128,13824) (which is 2304)
                    splitted_array = np.split(arr, len(pcm_chunk) // 2304)
                    while splitted_array:
                        print(len(splitted_array[0]))
                        self.stream.write(splitted_array.pop(0))

            except Exception as error:
                print(f'Error while playing song: {error}')
        
        self.stream.close()
    
    
    def decode_mp3_chunk(self, mp3_chunk):
        # Use ffmpeg to decode MP3 chunk to raw PCM audio data
        process = subprocess.Popen([
            'ffmpeg.exe',
            '-i', 'pipe:0',
            '-f', 's16le',
            '-ac', f'{self.channels}',
            '-ar', f'{self.sample_rate}',
            '-'],
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