import sqlite3
import os

class DBHandler:
    """
    Handles all database operations related to artists, albums, songs, and users.
    """

    def __init__(self, db="./server/database/echo.db"):
        """
        Initializes the database handler and sets up the tables if they don't exist.
        """
        self.connection = sqlite3.connect(db)
        self.create_tables()
        
    def create_tables(self):
        """
        Creates the necessary tables in the database for artists, albums, songs, and users.
        """
        cursor = self.connection.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS artists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS albums (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            artist_id INTEGER,
            FOREIGN KEY (artist_id) REFERENCES artists(id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            album_id INTEGER,
            track_number INTEGER
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            hashed_password TEXT NOT NULL,
            salt TEXT NOT NULL
        )
        ''')

        self.connection.commit()
    
    def insert_user(self, username, hashed_password, salt):
        """
        Adds a new user to the database.
        """
        cursor = self.connection.cursor()
        cursor.execute('''
        INSERT INTO users (username, hashed_password, salt) VALUES (?, ?, ?)
        ''', (username, hashed_password, salt))
        self.connection.commit()

    def search_user(self, username):
        """
        Searches for a user by their username.

        Returns The user info if found, Else None.
        """
        cursor = self.connection.cursor()
        cursor.execute('''
        SELECT * FROM users WHERE username = ?
        ''', (username,))
        return cursor.fetchone()
    
    def get_username_by_id(self, user_id):
        """
        Retrieves the username for a given user ID.

        Returns The username if found, Else None.
        """
        cursor = self.connection.cursor()
        cursor.execute('''
        SELECT username FROM users WHERE id = ?
        ''', (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    def insert_song(self, name, album_id, track_number):
        """
        Adds a new song to the database.
        """
        cursor = self.connection.cursor()
        cursor.execute('''
        INSERT INTO songs (name, album_id, track_number) VALUES (?, ?, ?)
        ''', (name, album_id, track_number))
        self.connection.commit()
        
    def insert_album(self, name, artist_id):
        """
        Adds a new album to the database.
        """
        cursor = self.connection.cursor()
        cursor.execute('''
        INSERT INTO albums (name, artist_id) VALUES (?, ?)
        ''', (name, artist_id))
        self.connection.commit()
    
    def insert_artist(self, name):
        """
        Adds a new artist to the database.
        """
        cursor = self.connection.cursor()
        cursor.execute('''
        INSERT INTO artists (name) VALUES (?)
        ''', (name,))
        self.connection.commit()
    
    def search(self, term):
        """
        Searches for albums and songs that match a search term.

        Returns A dictionary containing lists of matching albums and songs.
        """
        term = f"%{term}%"
        cursor = self.connection.cursor()

        cursor.execute('''
        SELECT 'album' AS type, id, name, artist_id FROM albums WHERE name LIKE ?
        ''', (term,))
        albums = cursor.fetchall()

        cursor.execute('''
        SELECT 'song' AS type, id, name, album_id FROM songs WHERE name LIKE ?
        ''', (term,))
        songs = cursor.fetchall()

        return {
            'albums': albums,
            'songs': songs
        }
    
    def get_album_by_id(self, album_id):
        """
        Retrieves an album by its ID.

        Returns The album record if found, Else None.
        """
        cursor = self.connection.cursor()
        cursor.execute('''
        SELECT id, name, artist_id FROM albums WHERE id = ?
        ''', (album_id,))
        return cursor.fetchone()
    
    def get_song_by_id(self, song_id):
        """
        Retrieves a song by its ID.

        Returns The song record if found, Else None.
        """
        cursor = self.connection.cursor()
        cursor.execute('''
        SELECT id, name, album_id FROM songs WHERE id = ?
        ''', (song_id,))
        return cursor.fetchone()
    
    def get_artist_by_id(self, artist_id):
        """
        Retrieves an artist by their ID.

        Returns The artist record if found, Else None.
        """
        cursor = self.connection.cursor()
        cursor.execute('''
        SELECT id, name FROM artists WHERE id = ?
        ''', (artist_id,))
        return cursor.fetchone()
    
    def get_song_id_by_name(self, song_name):
        """
        Retrieves the ID of a song by its name.

        Returns the song ID if found, Else None.
        """
        cursor = self.connection.cursor()
        cursor.execute('''
        SELECT id FROM songs WHERE name = ?
        ''', (song_name,))
        song_id = cursor.fetchone()
        return song_id[0] if song_id else None
    
    def get_album_id_by_name(self, album_name):
        """
        Retrieves the ID of an album by its name.

        Returns The album ID if found, Else None.
        """
        cursor = self.connection.cursor()
        cursor.execute('''
        SELECT id FROM albums WHERE name = ?
        ''', (album_name,))
        album_id = cursor.fetchone()
        return album_id[0] if album_id else None
    
    def get_artist_id_by_name(self, artist_name):
        """
        Retrieves the ID of an artist by their name.

        Returns The artist ID if found, otherwise None.
        """
        cursor = self.connection.cursor()
        cursor.execute('''
        SELECT id FROM artists WHERE name = ?
        ''', (artist_name,))
        artist_id = cursor.fetchone()
        return artist_id[0] if artist_id else None
    
    def get_song_path(self, song_id):
        """
        Retrieves the path of a song based on its ID.

        Returns The artist ID and album ID.
        """
        cursor = self.connection.cursor()
        cursor.execute('''
        SELECT artists.id AS artist_id, albums.id AS album_id
        FROM songs
        JOIN albums ON songs.album_id = albums.id
        JOIN artists ON albums.artist_id = artists.id
        WHERE songs.id = ?
        ''', (song_id,))
        result = cursor.fetchone()
        artist_id, album_id = result
        return artist_id, album_id
    
    def create_artist(self, name):
        """
        Creates a new artist entry and directory structure.
        """
        self.insert_artist(name)
        artist_id = self.get_artist_id_by_name(name)
        try:
            os.makedirs(f'./server/uploads/artists/{artist_id}')
            os.makedirs(f'./server/uploads/artists/{artist_id}/albums')
        except:
            pass
        return artist_id
    
    def create_album(self, artist_id, name):
        """
        Creates a new album entry and directory structure.
        """
        self.insert_album(name, artist_id)
        album_id = self.get_album_id_by_name(name)
        try:
            os.makedirs(f'./server/uploads/artists/{artist_id}/albums/{album_id}')
            os.makedirs(f'./server/uploads/artists/{artist_id}/albums/{album_id}/songs')
        except:
            pass
        return album_id
    
    def get_next_song_id(self, song_id):
        cursor = self.connection.cursor()
        
        # Get album_id and track_number of the current song
        cursor.execute('''
        SELECT album_id, track_number
        FROM songs
        WHERE id = ?
        ''', (song_id,))
        current_song = cursor.fetchone()
        
        if not current_song:
            return None
        
        album_id, current_track_number = current_song
        
        # Get the next song in the same album
        cursor.execute('''
        SELECT id
        FROM songs
        WHERE album_id = ? AND track_number > ?
        ORDER BY track_number ASC
        LIMIT 1
        ''', (album_id, current_track_number))
        next_song = cursor.fetchone()
        
        if next_song:
            return next_song[0]
        
        # If no next song is found, return the first song in the album
        cursor.execute('''
        SELECT id
        FROM songs
        WHERE album_id = ?
        ORDER BY track_number ASC
        LIMIT 1
        ''', (album_id,))
        first_song = cursor.fetchone()
        
        return first_song[0] if first_song else None
    
    def get_previous_song_id(self, song_id):
        cursor = self.connection.cursor()

        # Get album_id and track_number of the current song
        cursor.execute('''
        SELECT album_id, track_number
        FROM songs
        WHERE id = ?
        ''', (song_id,))
        current_song = cursor.fetchone()
        
        if not current_song:
            return None
        
        album_id, current_track_number = current_song
        
        # Get the previous song in the same album
        cursor.execute('''
        SELECT id
        FROM songs
        WHERE album_id = ? AND track_number < ?
        ORDER BY track_number DESC
        LIMIT 1
        ''', (album_id, current_track_number))
        previous_song = cursor.fetchone()
        
        if previous_song:
            return previous_song[0]
        
        # If no previous song is found, return the last song in the album
        cursor.execute('''
        SELECT id
        FROM songs
        WHERE album_id = ?
        ORDER BY track_number DESC
        LIMIT 1
        ''', (album_id,))
        last_song = cursor.fetchone()
        
        return last_song[0] if last_song else None
    
    def get_first_song_id(self, album_id):
        cursor = self.connection.cursor()
        
        # Get the first song in the album based on track_number
        cursor.execute('''
        SELECT id
        FROM songs
        WHERE album_id = ?
        ORDER BY track_number ASC
        LIMIT 1
        ''', (album_id,))
        first_song = cursor.fetchone()
        
        if first_song:
            return first_song[0]
        else:
            return None