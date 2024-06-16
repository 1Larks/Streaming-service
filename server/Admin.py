from DB_Handler import DBHandler
import shutil

CMDLEN = 5

def main():
    print('Hello Admin')
    
    db_h = DBHandler()
    
    while True:
        cmd = input('Enter command: ')
        data = cmd[CMDLEN:]
        cmd = cmd[:CMDLEN]
        if cmd == 'ARTS:':
            # Create a new album registry and directory tree gets artistName
            print('Trying to register a new artist...')
            id = db_h.create_artist(data)
            print(f'Created the entry for the artist, id is: {id}')
        elif cmd == 'ALBM:':
            # Create a new album registry and directory gets artistID:albumName
            print('Trying to create an album...')
            data = data.split(':')
            id = db_h.create_album(data[0], data[1])
            print(f'Created the entry for the album, id is: {id}')
        elif cmd == 'GART:':
            # Get the id of an artist by his name gets artist name
            print(db_h.get_artist_id_by_name(data))
        elif cmd == 'GALB:':
            # Get the id of an album by its name gets album name
            print(db_h.get_album_id_by_name(data))
        elif cmd == 'SNGR:':
            # Register a new song without adding the file, in case of DB Reset, gets songname:albumID:track_number
            data = data.split(':')
            db_h.insert_song(data[0], data[1], data[2])
            
        elif cmd == 'SNGU:':
            # Register a new song and add the file, gets a songname:albumID:track_number:path to wav file
            data = data.split(':')
            db_h.insert_song(data[0], data[1], data[2])
            id = db_h.get_song_id_by_name(data[0])
            info = db_h.get_song_path(id)
            # path = str(os.path.abspath(os.getcwd())).replace(r'\\', '/')
            directory = f'./server/uploads/artists/{info[0]}/albums/{info[1]}/songs/{id}.wav'
            shutil.move(data[3], directory)
   
   
if __name__ == '__main__':
    main()