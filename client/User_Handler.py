import hashlib
import secrets
import Network_Handler

return_values = {
    'N': 'username not found',
    'I': 'incorrect password',
    'T': 'username taken',
    'S': 'success'
}

class User_Handler:
    """
    Handles user registration and login processes using a network handler.
    """

    def __init__(self, network_handler: Network_Handler):
        """
        Initializes the User_Handler
        """
        self.network_h = network_handler
        self.username = None
        
    
    def register_user(self, username, password):
        """
        Registers a new user on the server.
        """
        # Generate a random salt
        salt = secrets.token_hex(16)
        
        # Hash the password with the salt
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        
        # Registration data to send to the server
        registration_data = f'RGST{username}:{hashed_password}:{salt}'
        
        # Send registration data to the server
        self.network_h.send_data(registration_data, text=True)
        
        # Store the username locally
        self.username = username

    def login(self, username, password):
        """
        Authenticates a user with the server.
        """
        # Request salt for the given username
        self.network_h.send_data(f'SALT{username}', text=True)
        
        # Retrieve salt asynchronously
        salt = self.network_h.getAsyncBuffer('salt')
        
        # If salt is None, username does not exist
        if salt is None:
            return return_values['username not found']
        
        # Combine password and salt, then hash it with sha256
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        
        # Send login request to the server
        login_data = f'LOGN{username}:{hashed_password}'
        self.network_h.send_data(login_data, text=True)
        
        # Store the username locally
        self.username = username