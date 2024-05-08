import hashlib
import secrets


class User_Handler:
    def __init__(self, network_handler) -> None:
        self.network_h = network_handler
    
    def register(self, username, hashed_password, salt):
        pass