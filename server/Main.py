import select
import pickle
from Stream_Handler import Stream_Handler
from User_Handler import User_Handler
from Network_Handler import Network_Handler, BUFFSIZE
from DB_Handler import DBHandler

# CMDLEN is the length of each header, explanation is in the project's book page 7
CMDLEN = 4

def handle_client_data(data, sock, network_h, stream_h, user_h, db_h):
    """
    Handle data received from a client.

    Parameters:
    data: Data received from the client.
    sock: Client's socket.
    network_h: Instance of Network_Handler.
    stream_h: Instance of Stream_Handler.
    user_h (User_Handler): Instance of User_Handler.
    db_h: Instance of DBHandler.
    """
    
    data = data.decode().strip('0')
    command = data[:CMDLEN]
    data = data[CMDLEN:]
    
    if command == 'LOGN':
        username, hashed_password = data.split(':')
        resp = user_h.login(username, hashed_password)
        network_h.send_data(sock, 'LOGN' + resp, text=True)
        
    elif command == 'SALT':
        user_h.send_salt(sock, data)
        
    elif command == 'RGST':
        username, password, other_data = data.split(':')
        resp = user_h.register(username, password, other_data)
        network_h.send_data(sock, 'RGST' + resp, text=True)
        
    elif command == 'SRCH':
        result = db_h.search(data)
        # Serialize the data before sending it.
        serialized_data = pickle.dumps(result)
        network_h.send_data(sock, 'SRCH'.encode() + serialized_data, text=False)
        
    elif command == 'PLAY':
        song_id, seek = data.split(':')
        # Find the path accourding to the directory tree's rules.
        artist_id, album_id = db_h.get_song_path(song_id)
        path = f'./server/uploads/artists/{artist_id}/albums/{album_id}/songs/{song_id}'
        stream_h.start_stream(path, int(seek), sock)
        
    elif command == 'PAUS':
        stream_h.stop_stream(sock)
    
    elif command == 'NEXT':
        network_h.send_data(sock, 'SONG'+str(db_h.get_next_song_id(int(data))), text=True)
    
    elif command == 'PREV':
        network_h.send_data(sock, 'SONG'+str(db_h.get_previous_song_id(int(data))), text=True)
    
    elif command == 'ALBM':
        network_h.send_data(sock, 'SONG'+str(db_h.get_first_song_id(int(data))), text=True)
    
    else:
        pass

def main():
    """
    Main function to start the server and handle incoming connections and data.
    """
    network_h = Network_Handler()
    stream_h = Stream_Handler(network_h)
    db_h = DBHandler()
    user_h = User_Handler(network_h, db_h)
    
    network_h.start_server()
    
    while True:
        rlist, _, _ = select.select([network_h.ssl_sock] + network_h.clients, [], [])
        for sock in rlist:
            if sock is network_h.ssl_sock:
                network_h.accept_new_connections()
                stream_h.streaming[sock] = False
            else:
                try:
                    data = sock.recv(BUFFSIZE)
                    if data:
                        handle_client_data(data, sock, network_h, stream_h, user_h, db_h)
                    else:
                        print(f'Client {sock} disconnected')
                        network_h.remove_client(sock)
                        del stream_h.streaming[sock]
                except Exception as err:
                    print(f'Error receiving data from client {sock}, Error: {err}')
                    network_h.remove_client(sock)
                    del stream_h.streaming[sock]

if __name__ == '__main__':
    main()