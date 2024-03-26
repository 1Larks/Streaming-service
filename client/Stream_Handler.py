import pyaudio
import Network_Handler
import threading

class Stream_Handler:
    def __init__(self, network_handler: Network_Handler.Network_Handler) -> None:
        self.playing = False
        
        self.audio = pyaudio.PyAudio()
        
        self.bytes_recieved = 0
        self.prev_sample_rate = None
        self.prev_channels = None
        self.network_h = network_handler
        
        self.curr_buffer = None
        
    def _play_song(self):
        prev_buff = None
        
        stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=2,
            rate=44100,
            output=True,
            frames_per_buffer=Network_Handler.BUFFSIZE
        )
        
        while self.playing:
            if prev_buff:
                if self.curr_buffer != prev_buff:
                    stream.write(self.curr_buffer)
            else:
                stream.write(self.curr_buffer)
            
            prev_buff = self.curr_buffer
    
    def start_stream(self):
        threading.Thread(target=self._play_song).start()
    
    def stop_stream(self):
        self.playing = False