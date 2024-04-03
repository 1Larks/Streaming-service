import socket
import ssl

BACKLOG = 10
SERV_ADDR = '127.0.0.1'
PORT = 31337

#Temporary buffer size
BUFFSIZE = 4096

class Network_Handler:
    def __init__(self, addr: str = SERV_ADDR, port: int = PORT) -> None:
        self.host = addr
        self.port = port
        self.server_socket = None
        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.ssl_context.load_cert_chain(certfile=r"server\encryption\server.csr", keyfile=r"server\encryption\server.key")
        self.ssl_sock = None
        self.clients = []
        self.streaming = True
    
    # May change return type to bool for control and debugging
    def start_server(self) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(BACKLOG)
        self.ssl_sock = self.ssl_context.wrap_socket(self.server_socket, server_side=True)
        
    def send_data(self, client_sock, data, text: bool = False) -> None:
        try:
            client_sock.sendall(data.zfill(BUFFSIZE).encode() if text else data)
        except Exception as err:
            print(f"Error sending data to client: {err}")
    
    def accept_new_connections(self) -> None:
        client_sock, client_addr = self.server_socket.accept()
        print(f'New connection created, client address: {client_addr}')
        self.clients.append(client_sock)
    
    def remove_client(self, client_sock) -> None:
        if client_sock in self.clients:
            self.clients.remove(client_sock)
            client_sock.close()
    