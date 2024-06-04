from Network_Handler import Network_Handler, BUFFSIZE
from Stream_Handler import Stream_Handler
from select import select
import os
from User_Handler import User_Handler


CMDLEN = 4

def handle_server_data(data, network_h, stream_h, user_h):
    dataHeader = data[:CMDLEN].decode().strip('0')
    dataNoHeader = data[CMDLEN:]
    if dataHeader == 'CHNK':
        stream_h.chunks.append(dataNoHeader)
    elif dataHeader == 'PLAY':
        stream_h.playing = True
        stream_h.start_stream()
    
    elif dataHeader == 'RGST' or dataHeader == 'LOGN':
        dataNoHeader = dataNoHeader.decode().strip('0')
        if user_h.check_validity(dataNoHeader):
            print('Successfuly ' + ('registered' if dataHeader == 'RGST' else 'logged in'))
            print('Hello, ' + user_h.username + r' Enter command, for example: PLAY{Songname}')
            network_h.send_data(input('enter command:'), text=True)
    elif dataHeader == 'SALT':
        user_h.buffer.append(dataNoHeader.decode().strip('0'))
                    

def main():
    
    network_h = Network_Handler('127.0.0.1', 31337)
    network_h.connect_to_server()
    stream_h = Stream_Handler(network_h)
    user_h = User_Handler(network_h)
    sock_list = [network_h.ssl_sock]
    
    print('Enter Command, 1 to log in, 2 to register')
    response = input('Command: ')
    if response == '1':
        un = input('Username: ')
        pw = input('Password: ')
        user_h.login(un, pw)
    elif response == '2':
        un = input('Username: ')
        pw = input('Password: ')
        user_h.register_user(un, pw)
    
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
                    handle_server_data(data, network_h, stream_h, user_h)        

if __name__ == '__main__':
    main()