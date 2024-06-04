import hashlib
import secrets
import Network_Handler
import threading

return_values = {
    'N': 'username not found',
    'I': 'incorrect password',
    'T': 'username taken',
    'S': 'success'
}

class User_Handler:
    def __init__(self, network_handler: Network_Handler):
        self.network_h = network_handler
        self.authenticated = False
        self.username = None
        self.buffer = []
        
    
    # Register a new user on the server
    def register_user(self, username, password):
        # Generate a random salt
        salt = secrets.token_hex(16)
        
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        
        registration_data = f'RGST{username}:{hashed_password}:{salt}'
        
        self.network_h.send_data(registration_data, text=True)
        
        self.username = username
        return return_values['S']

    # Authenticate a user
    def _login(self, username, password):
        # Retrieve salt from the server (the server sends the salt for the provided username)
        
        self.network_h.send_data(f'SALT{username}', text=True)
        while len(self.buffer) == 0:
            continue
        salt = self.buffer.pop(0)
        
        if salt is None:
            return return_values['username not found']
        # Combine password and salt, then hash it
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        
        # Send login request to the server
        login_data = f'LOGN{username}:{hashed_password}'
        self.network_h.send_data(login_data, text = True)
        
        self.username = username
            
        return None
    
    def login(self, username, password):
        threading.Thread(target=self._login, args=(username, password)).start()
    
    def check_validity(self, serverResponse):
        print(return_values[serverResponse])
        if serverResponse == 'S':
            self.authenticated = True
            return True
        else:
            return False