import hashlib
import secrets

return_values = {
    'username not found': '1',
    'incorrect password': '2',
    'username taken': '3',
    'success': '0'
}

class User_Handler:
    def __init__(self, network_handler, db_handler) -> None:
        self.network_h = network_handler
        self.db_h = db_handler
    
    def register(self, username, hashed_password, salt):
        search_for_username = self.db_h.search_user(username)
        if search_for_username != None:
            #Let the client know
            return return_values['username taken']
        
        self.db_h.insert_user(username, hashed_password, salt)
        return return_values['success']
        


    def login(self, username, hashed_password):
        pass