import sqlite3

class DBHandler:
    def __init__(self, users_db_file=r"./databases/users.db", songs_db_file="./databases/songs.db", preferences_db_file="./databases/preferences.db"):
        # Connect to databases
        self.users_conn = sqlite3.connect(users_db_file)
        self.songs_conn = sqlite3.connect(songs_db_file)
        self.preferences_conn = sqlite3.connect(preferences_db_file)
        # Create tables if they don't exist
        self._create_users_table()
        self._create_songs_table()
        self._create_preferences_table()

    def _create_users_table(self):
        cursor = self.users_conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT,
                           hashed_password TEXT,
                           salt TEXT)''')
        self.users_conn.commit()

    def _create_songs_table(self):
        cursor = self.songs_conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS songs
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           title TEXT,
                           album TEXT,
                           artist TEXT)''')
        self.songs_conn.commit()

    def _create_preferences_table(self):
        cursor = self.preferences_conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS preferences
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT,
                           preference TEXT)''')
        self.preferences_conn.commit()

    def insert_user(self, username, hashed_password, salt):
        cursor = self.users_conn.cursor()
        cursor.execute("INSERT INTO users (username, hashed_password, salt) VALUES (?, ?, ?)",
                       (username, hashed_password, salt))
        self.users_conn.commit()

    def search_user(self, username):
        cursor = self.users_conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        return cursor.fetchone()

    def get_salt_by_username(self, username):
        cursor = self.users_conn.cursor()
        cursor.execute("SELECT salt FROM users WHERE username=?", (username,))
        return cursor.fetchone()

    def insert_song(self, title, artist):
        cursor = self.songs_conn.cursor()
        cursor.execute("INSERT INTO songs (title, artist) VALUES (?, ?)", (title, artist))
        self.songs_conn.commit()

    def search_song(self, title):
        cursor = self.songs_conn.cursor()
        cursor.execute("SELECT * FROM songs WHERE title=?", (title,))
        return cursor.fetchone()

    def insert_preference(self, username, preference):
        cursor = self.preferences_conn.cursor()
        cursor.execute("INSERT INTO preferences (username, preference) VALUES (?, ?)", (username, preference))
        self.preferences_conn.commit()

    def get_preference(self, username):
        cursor = self.preferences_conn.cursor()
        cursor.execute("SELECT preference FROM preferences WHERE username=?", (username,))
        return cursor.fetchone()
