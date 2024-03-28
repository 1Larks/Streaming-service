import sounddevice
import numpy as np
import Network_Handler
import threading
from pydub import pyaudioop
#import pymp3

STOP_BUFF = ':STOP'.zfill(4096).encode()

class Stream_Handler:
    def __init__(self, network_handler: Network_Handler.Network_Handler) -> None:
        self.playing = False
        
        self.bytes_recieved = 0
        self.prev_sample_rate = None
        self.prev_channels = None
        self.network_h = network_handler
        
        self.curr_buffer = []
        
        self.sample_rate = None
        self.channels = None
        
        self.stream = None
        
    def _play_song(self):
        while len(self.curr_buffer)==0:
            continue
        
        info = self.curr_buffer[0].decode().strip('0').split(':')
        self.sample_rate, self.channels = int(info[0]), int(info[1])
        index = 1
        self.stream = sounddevice.RawOutputStream(samplerate=self.sample_rate, channels= self.channels, blocksize=4096, dtype='float32')
        self.stream.start()
        while self.playing:
            
            if index < len(self.curr_buffer):
                if self.curr_buffer[index] == STOP_BUFF:
                    self.playing = False
                    break
                
                self.stream.write(self.curr_buffer[index])
                
                index+=1
        self.stream.close()
        self.stream = None
    
    
    def start_stream(self):
        threading.Thread(target=self._play_song).start()
    
    def stop_stream(self):
        self.playing = False
