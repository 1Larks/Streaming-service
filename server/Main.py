import select

import Stream_Handler
from User_Handler import User_Handler
from Network_Handler import Network_Handler, BUFFSIZE
from DB_Handler import DBHandler
from User_Handler import User_Handler

CMDLEN = 4

def handle_client_data(data, sock, network_h, stream_h, user_h):
    data = data.decode().strip('0')
    command = data[:CMDLEN]
    data = data[CMDLEN:]
    #Temporary
    if command == 'LOGN':
        pass
    elif command == 'RGST':
        pass
    elif command == 'PLAY':
        stream_h.start_stream(data, sock)
    

def main():
    network_h = Network_Handler()
    stream_h = Stream_Handler.Stream_Handler(network_h)
    db_h = DBHandler()
    user_h = User_Handler(db_h)
    
    network_h.start_server()
    while True:
            rlist, _, _ = select.select([network_h.ssl_sock] + network_h.clients, [], [])
            for sock in rlist:
                if sock is network_h.ssl_sock:
                    network_h.accept_new_connections()
                else:
                    try:
                        data = sock.recv(BUFFSIZE)
                        if data:
                            handle_client_data(data, sock, network_h, stream_h, user_h)
                            
                        else:
                            network_h.remove_client(sock)
        
                    except Exception as err:
                        print(f'Error recieving data from client {sock}, Error: {err}')
                        network_h.remove_client(sock)
    
    
if __name__ == '__main__':
    main()