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
    
        self.stream = sd.RawOutputStream(self.sample_rate, Network_Handler.BUFFSIZE, dtype='int16')
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
                    self.stream.write(current_buffer)

            except Exception as error:
                print(f'Error while playing song: {error}')
        
        self.stream.close()
    
    def start_stream(self):
        threading.Thread(target=self._play_song).start()
    
    def stop_stream(self):
        self.playing = False