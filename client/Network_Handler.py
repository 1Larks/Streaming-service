import socket

BUFFSIZE = 4096

class Network_Handler:
    def __init__(self, server_addr: str, server_port: int) -> None:
        self.serv_addr = server_addr
        self.serv_port = server_port
        self.sock = None
    
    def connect_to_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.serv_addr, self.serv_port))
        print(f"Connected to server: {self.serv_addr}:{self.serv_port}")
    
    def send_data(self, data):
        try:
            self.sock.sendall(data.zfill(BUFFSIZE).encode())
        except Exception as err:
            print(f"Error sending data to server: {err}")
    
    def close_connection(self):
        if self.sock:
            self.sock.close()
            print("Connection closed")