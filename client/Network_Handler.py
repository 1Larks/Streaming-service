import socket
import ssl

BUFFSIZE = 4096

class Network_Handler:
    def __init__(self, server_addr: str, server_port: int) -> None:
        self.serv_addr = server_addr
        self.serv_port = server_port
        self.sock = None
        self.ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        self.ssl_sock = None
        self.buffers = {
            'salt': None,
            'auth': None
            }
    
    def getAsyncBuffer(self, buffName):
        while self.buffers[buffName] == None:
            continue
        result = self.buffers[buffName]
        self.buffers[buffName] = None
        return result
    
    def connect_to_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ssl_sock = self.ssl_context.wrap_socket(self.sock, server_hostname=self.serv_addr)
        self.ssl_sock.connect((self.serv_addr, self.serv_port))
        print(f"Connected to server: {self.serv_addr}:{self.serv_port}")
    
    def send_data(self, data, text: bool = False):
        try:
            self.ssl_sock.sendall(data.zfill(BUFFSIZE).encode() if text else data)
        except Exception as err:
            print(f"Error sending data to server: {err}")
    
    def close_connection(self):
        if self.sock:
            self.sock.close()
            print("Connection closed")