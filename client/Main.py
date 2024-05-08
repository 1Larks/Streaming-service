from Network_Handler import Network_Handler, BUFFSIZE
from Stream_Handler import Stream_Handler
from select import select
import os

CMDLEN = 4

def handle_server_data(data, network_h, stream_h):
    if stream_h.playing:
        stream_h.chunks.append(data)
    else:
        if data.decode().strip('0')[:CMDLEN] == 'PLAY':
            stream_h.playing = True
            stream_h.start_stream()
        else:
            #Handle other info from the server
            pass
                    

def main():
    
    network_h = Network_Handler('127.0.0.1', 31337)
    network_h.connect_to_server()
    stream_h = Stream_Handler(network_h)
    
    sock_list = [network_h.ssl_sock]
    network_h.send_data(input('enter command:'), text=True)
    
    while True:
        rlist, _, _ = select(sock_list, [], [])
        for sock in rlist:
            if sock is network_h.ssl_sock:
                #Recieved data from server
                data = sock.recv(BUFFSIZE)
                if not data:
                    print('Connection from the server broken.')
                    network_h.close_connection()
                else:
                    handle_server_data(data, network_h, stream_h)        

if __name__ == '__main__':
    main()