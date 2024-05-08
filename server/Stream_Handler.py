import threading
import Network_Handler
import os
from pydub.utils import mediainfo

'''

A class that handles all stream-related activities for the server, it gives the Network Handler the song bytes
to pass onto the user's stream, since this class is in early development and still needs a proof of concept,
the stream handler will simply pull the song and send it, this may change in the future as the project develops.

'''

CHUNK_SIZE = 4096

class Stream_Handler:
    def __init__(self, network_handler: Network_Handler.Network_Handler) -> None:
        self.streaming = False
        self.network_h = network_handler
    
    def _play_song(self, song_name, client_sock):
        #Temporary
        path = f'server\\songs\\{song_name}.wav'
        self.network_h.send_data(client_sock, 'PLAY:', text=True)
        try:
            with open(path, 'rb') as song:
                
                info = mediainfo(path)
                
                sample_rate, channels = info['sample_rate'], info['channels']
                self.network_h.send_data(client_sock, f'{sample_rate}:{channels}', text=True)
                
                while self.streaming:
                    chunk = song.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    self.network_h.send_data(client_sock, chunk)
                    
                self.network_h.send_data(client_sock, ':STOP', text=True)
        except Exception as err:
            print(f"Error sending song to client: {err}")
    
    def start_stream(self, song_name, client_sock):
        self.streaming = True
        threading.Thread(target=self._play_song, args=(song_name, client_sock)).start()
    
    def stop_stream(self):
        self.streaming = False
        