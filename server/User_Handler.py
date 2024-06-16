return_values = {
    'username not found': 'N',
    'incorrect password': 'I',
    'username taken': 'T',
    'success': 'S'
}

class User_Handler:
    """
    Handles user-related activities such as registration, login, and sending salts.
    """
    
    def __init__(self, network_handler, db_handler) -> None:
        """
        Initializes the User_Handler with the given Network_Handler and DBHandler instances.
        """
        self.network_h = network_handler
        self.db_h = db_handler
    
    def register(self, username: str, hashed_password: str, salt: str) -> str:
        """
        Registers a new user with the given username, hashed password, and salt.
        Returns a status code indicating success or the type of error encountered.
        """
        search_for_username = self.db_h.search_user(username)
        if search_for_username is not None:
            return return_values['username taken']
        
        self.db_h.insert_user(username, hashed_password, salt)
        return return_values['success']

    def login(self, username: str, hashed_password: str) -> str:
        """
        Logs in a user with the given username and hashed password.
        Returns a status code indicating success or the type of error encountered.
        """
        data = self.db_h.search_user(username)
        if not data:
            return return_values['username not found']
        if hashed_password != data[2]:
            return return_values['incorrect password']
        return return_values['success']
        
    def send_salt(self, sock, username: str) -> None:
        """
        Sends the salt associated with the given username to the client.
        If the username is not found, sends an empty SALT response.
        """
        data = self.db_h.search_user(username)
        if not data:
            self.network_h.send_data(sock, 'SALT', text=True)
        else:
            self.network_h.send_data(sock, 'SALT' + data[3], text=True)