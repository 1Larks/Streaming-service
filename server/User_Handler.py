import hashlib
import secrets

return_values = {
    'username not found': 'N',
    'incorrect password': 'I',
    'username taken': 'T',
    'success': 'S'
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
        data = self.db_h.search_user(username)
        if not data:
            return return_values['username not found']
        if hashed_password != data[2]:
            return return_values['incorrect password']
        else:
            return return_values['success']
        
    def send_salt(self, sock, username):
        data = self.db_h.search_user(username)
        if not data:
            return return_values['username not found']
        self.network_h.send_data(sock, 'SALT'+data[3], text = True)