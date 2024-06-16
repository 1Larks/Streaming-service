from kivy.core.window import Window
from Network_Handler import Network_Handler, BUFFSIZE
from Stream_Handler import Stream_Handler
from User_Handler import User_Handler
from GUI import AudioStreamingApp
import threading
from select import select
import pickle

# Command length used to extract headers from server messages
CMDLEN = 4      

def handle_server_data(data, network_h, stream_h):
    """
    Processes incoming data from the server and routes it to the appropriate handler.
    """
    data_header = data[:CMDLEN].decode().strip('0')
    data_no_header = data[CMDLEN:]
    
    if data_header == 'CHNK':
        if stream_h.playing:
            stream_h.chunks.append(data_no_header)
    elif data_header == 'PLAY':
        stream_h.playing = True
        stream_h.start_stream()
    elif data_header in ['RGST', 'LOGN']:
        data_no_header = data_no_header.decode().strip('0')
        network_h.buffers['auth'] = data_no_header
    elif data_header == 'SALT':
        network_h.buffers['salt'] = data_no_header.decode().strip('0')
    elif data_header == 'SRCH':
        search_result = pickle.loads(data_no_header)
        print(search_result)
        network_h.buffers['search'] = search_result

def run_network_handler(network_h, stream_h, user_h):
    """
    Listens for data from the server and handles incoming messages.
    """
    sock_list = [network_h.ssl_sock]
    while True:
        rlist, _, _ = select(sock_list, [], [])
        for sock in rlist:
            if sock is network_h.ssl_sock:
                data = sock.recv(BUFFSIZE)
                if not data:
                    print('Connection from the server broken.')
                    network_h.close_connection()
                    return
                else:
                    handle_server_data(data, network_h, stream_h)

def start_login_gui(network_h, user_h, stream_h):
    """
    Initializes and runs the login GUI for the audio streaming application.
    """
    app = AudioStreamingApp(network_h, user_h, stream_h)
    Window.size = (700, 600)
    app.run()

def main():
    """
    Entry point of the client application. Initializes network and GUI components.
    """
    network_h = Network_Handler('127.0.0.1', 31337)
    network_h.connect_to_server()
    stream_h = Stream_Handler()
    user_h = User_Handler(network_h)

    network_thread = threading.Thread(target=run_network_handler, args=(network_h, stream_h, user_h))
    network_thread.daemon = True
    network_thread.start()

    start_login_gui(network_h, user_h, stream_h)

if __name__ == '__main__':
    main()