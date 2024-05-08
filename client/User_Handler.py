import hashlib
import secrets
import Network_Handler

return_values = {
    'username not found': '-1',
    'incorrect password': '-2',
    'success': '0'
}

class User_Handler:
    def __init__(self, network_handler):
        self.network_h = network_handler
        self.authenticated = False
        self.username = None
        
    
    # Register a new user on the server
    def register_user(self, username, password):
        # Generate a random salt
        salt = secrets.token_hex(16)
        
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        
        registration_data = f'{username}:{hashed_password}:{salt}'
        
        return return_values['success']

    # Authenticate a user
    def login_user(self, username, password):
        # Retrieve salt from the server (the server sends the salt for the provided username)
        salt = self.network_h.retrieve_salt_from_server(username)
        
        if salt is None:
            return return_values['username not found']
        # Combine password and salt, then hash it
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        
        # Send login request to the server
        login_data = f'{username}:{hashed_password}'
        server_response = self.network_h.send_data(login_data)
        
        if server_response == return_values['success']:
            self.authenticated = True
            self.username = username
            
        return server_response
    