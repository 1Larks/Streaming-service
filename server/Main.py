from Network_Handler import Network_Handler, BUFFSIZE
import Stream_Handler
import select

def main():
    network_h = Network_Handler()
    
    stream_h = Stream_Handler.Stream_Handler(network_h)
    
    network_h.start_server()
    while True:
            rlist, _, _ = select.select([network_h.server_socket] + network_h.clients, [], [])
            for sock in rlist:
                if sock is network_h.server_socket:
                    network_h.accept_new_connections()
                else:
                    try:
                        data = sock.recv(BUFFSIZE)
                        if data:
                            # HANDLE CLIENT RECIEVED DATA HERE
                            data = data.decode().strip('0')
                            print(data)
                            #Temporary
                            if data[:5] == 'PLAY:':
                                stream_h.start_stream(data[5:], sock)
                            
                        else:
                            network_h.remove_client(sock)
        
                    except Exception as err:
                        print(f'Error recieving data from client {sock}, Error: {err}')
                        network_h.remove_client(sock)
    
    
if __name__ == '__main__':
    main()