import Network_Handler
import threading
import sounddevice as sd
from time import sleep

class Stream_Handler:
    """
    Handles streaming of audio data received from the network using sounddevice.
    """

    def __init__(self):
        """
        Initializes the Stream_Handler with attributes for managing streaming state and audio data.
        """
        self.playing = False
        self.frames_received = -1
        self.chunks = []
        self.sample_rate = None
        self.channels = None
        self.stream = None
        self.size = None
        self.frame_size = None

    def _play_song(self):
        """
        Internal method that streams audio data received as chunks, meant to be threaded and not called by itself.
        """
        while len(self.chunks) == 0:
            continue
        
        if not self.sample_rate and not self.channels and not self.size:
            info = self.chunks.pop(0).decode().strip('0').split(':')
            self.sample_rate = int(info[0])
            self.channels = int(info[1])
            self.size = int(info[2])
            width = int(info[3])
            self.frame_size = self.channels * width
            self.frames_received = 0
        
        self.stream = sd.RawOutputStream(self.sample_rate, Network_Handler.BUFFSIZE, channels=self.channels, dtype='int16')
        self.stream.start()
        
        while self.playing:
            try:
                current_buffer = None
                if len(self.chunks) > 0:
                    current_buffer = self.chunks.pop(0)
                
                if current_buffer is not None:
                    self.stream.write(current_buffer)
                    self.frames_received += len(current_buffer) // self.frame_size
                else:
                    self.stop_stream()
                    self.reset_stream()
                
            except Exception as error:
                print(f'Error while playing song: {error}')
        
        print('Playback stopped')
        self.stream.close()

    def start_stream(self):
        """
        Starts streaming audio data in a separate thread.
        """
        threading.Thread(target=self._play_song).start()

    def stop_stream(self):
        """
        Stops the audio stream.
        """
        self.playing = False
        sleep(0.2)  # Wait for the loop to close
        self.chunks.clear()

    def reset_stream(self):
        """
        Resets stream and attributes.
        """
        self.playing = False
        self.frames_received = -1
        self.sample_rate = None
        self.channels = None
        self.size = None
        self.frame_size = None