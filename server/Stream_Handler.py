import threading
import traceback
import wave
from Network_Handler import Network_Handler

CHUNK_SIZE = 4096

class Stream_Handler:
    """
    Handles all stream-related activities for the server, including sending
    song frames through the Network Handler to users.
    """
    
    def __init__(self, network_handler: Network_Handler) -> None:
        """
        Initializes the Stream_Handler with a given Network_Handler instance.
        """
        self.streaming = {}
        self.network_h = network_handler
        
    def _play_song(self, path: str, seek: int, client_sock) -> None:
        """
        Streams a song to the client. This is a threaded function and should
        not be called directly. Handles sending song metadata and chunks.
        """
        path = f'{path}.wav'
        self.network_h.send_data(client_sock, 'PLAY', text=True)
        try:
            with wave.open(path, 'rb') as song:
                
                # Getting all the crucial info for playing the song (metadata).
                sample_rate = song.getframerate()
                channels = song.getnchannels()
                width = song.getsampwidth()
                # Calculate the size of each frame in the audio file then 
                # calculate the size of the whole file and then the size of each chunk in bytes.
                frame_size = channels * width
                size = song.getnframes() * frame_size
                chunk_size = (CHUNK_SIZE - 4) // frame_size
                 # If the seek parameter is equal to -1, it means that the song havent 
                 # started playing yet (not paused) and so we need to send the metadata.
                 # Else we seek to the given point
                if seek == -1:
                    self.network_h.send_data(client_sock, f'CHNK{sample_rate}:{channels}:{size}:{width}', text=True)
                else:
                    # Calculate the specific frame
                    seek_frame = seek // frame_size
                    song.setpos(seek_frame)
                
                while self.streaming.get(client_sock, False):
                    chunk = song.readframes(chunk_size)
                    if not chunk:
                        self.stop_stream(client_sock)
                        break
                    self.network_h.send_data(client_sock, b'CHNK' + chunk)
                
        except Exception as err:
            print(f"Error sending song to client: {err}")
            print(traceback.format_exc())
    
    def start_stream(self, path: str, seek: int, client_sock) -> None:
        """
        Starts streaming a song to the client by creating a new thread.
        """
        self.streaming[client_sock] = True
        threading.Thread(target=self._play_song, args=(path, seek, client_sock)).start()
    
    def stop_stream(self, client_sock) -> None:
        """
        Stops streaming to the given client socket.
        """
        self.streaming[client_sock] = False 
        