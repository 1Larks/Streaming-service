from Network_Handler import Network_Handler, BUFFSIZE
from Stream_Handler import Stream_Handler
from select import select
import socket

def main():
    network_h = Network_Handler('127.0.0.1', 31337)
    network_h.connect_to_server()
    stream_h = Stream_Handler(network_h)
    
    sock_list = [network_h.sock]
    network_h.send_data(input('enter command:'))
    while True:
        rlist, _, _ = select(sock_list, [], [])
        
        for sock in rlist:
            if sock is network_h.sock:
                #Recieved data from server
                data = sock.recv(BUFFSIZE)
                if not data:
                    print('Connection from the server broken.')
                    network_h.close_connection()
                else:
                    #Handle data here
                    
                    if stream_h.playing:
                        stream_h.curr_buffer.append(data)
                    
                    else:
                        if data.decode().strip('0')[:5] == 'PLAY:':
                            stream_h.playing = True
                            stream_h.start_stream()
                        else:
                            #Handle other info from the server
                            pass
                        
        
        

if __name__ == '__main__':
    main()