import threading
import Network_Handler
import os
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
        path = f'server\\songs\\{song_name}.mp3'
        self.network_h.send_data(client_sock, 'PLAY:', text=True)
        try:
            with open(path, 'rb') as song:
                
                sample_rate, channels = self.skip_mp3_header(song)
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
        
        
    def find_sync_word(self, file):
        while True:
            byte = file.read(1)
            if byte == b'':
                return None  # End of file
            if byte == b'\xff':
                return file.tell() - 1

    """
    A function to extract crucial information about the song before sending it to the client,
    while making this function i got lots of help from ChatGPT, this is okay since this function
    is about super specific headers and bytes inside of an mp3 file and does not matter much for the project at whole,
    but is just useful information extracted in an efficent way insted of using external libraries.
    """
    def get_frame_size(self, file):
        header_bytes = file.read(4)  # Read the header bytes
        if len(header_bytes) < 4:
            return None, None, None, None  # Not enough bytes for a header
        header_data = int.from_bytes(header_bytes, byteorder='big')
        sync = (header_data >> 21) & 0x7FF
        if sync != 0x7FF:
            return None, None, None, None  # Not a valid header
        version = (header_data >> 19) & 0x3
        layer = (header_data >> 17) & 0x3
        bitrate_index = (header_data >> 12) & 0xF
        sample_rate_index = (header_data >> 10) & 0x3
        padding = (header_data >> 9) & 0x1
        bitrate = {
            1: [0, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448],
            2: [0, 32, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 384],
            3: [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320],
        }.get(version, [0] * 15)[bitrate_index]
        sample_rates = [44100, 48000, 32000]
        sample_rate = sample_rates[sample_rate_index]
        if version == 3:  # MPEG 1
            frame_size = ((144 * bitrate * 1000) // sample_rate) + padding
        else:  # MPEG 2 or 2.5
            frame_size = ((72 * bitrate * 1000) // sample_rate) + padding
        channels = 2 if layer == 1 else 1  # For MPEG 1, 2 channels; for MPEG 2 or 2.5, 1 channel
        print(bitrate)
        return frame_size, bitrate, channels, sample_rate
    
    def skip_mp3_header(self, file):
        sync_word_offset = self.find_sync_word(file)
        if sync_word_offset is None:
            return  # No sync word found
        file.seek(sync_word_offset)
        frame_size, bitrate, channels, sample_rate = self.get_frame_size(file)
        if frame_size is None:
            return  None, None, None, None
        file.seek(frame_size - 4, os.SEEK_CUR)  # Skip the frame header and data
        return sample_rate, channels