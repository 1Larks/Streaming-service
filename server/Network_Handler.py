import socket
import ssl

BACKLOG = 10
SERV_ADDR = '127.0.0.1'
PORT = 31337
BUFFSIZE = 4096

class Network_Handler:
    """
    Handles network operations including starting the server, sending data,
    accepting new connections, and removing clients.
    """
    
    def __init__(self, addr: str = SERV_ADDR, port: int = PORT) -> None:
        """
        Initializes the network handler with the given server address and port.
        Sets up the SSL context and prepares to accept clients.
        """
        self.host = addr
        self.port = port
        self.server_socket = None
        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.ssl_context.load_cert_chain(certfile=r"server\encryption\certificate.pem",
                                         keyfile=r"server\encryption\private_key.pem")
        self.ssl_sock = None
        self.clients = []
    
    def start_server(self) -> None:
        """
        Starts the server by binding to the specified address and port,
        setting up the SSL socket, and beginning to listen for connections.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(BACKLOG)
        self.ssl_sock = self.ssl_context.wrap_socket(self.server_socket, server_side=True)
        print(f'Server started on {self.host}:{self.port}')
        
    def send_data(self, client_sock: socket.socket, data: str, text: bool = False) -> None:
        """
        Sends data to a client socket. If the data is text, it is encoded
        and padded to match BUFFSIZE. Otherwise, the data is sent as is.
        """
        try:
            if text:
                client_sock.sendall(data.encode() + (b''.zfill(BUFFSIZE - len(data))))
            else:
                client_sock.sendall(data)
        except Exception as err:
            print(f"Error sending data to client: {err}")
    
    def accept_new_connections(self) -> None:
        """
        Accepts new client connections and adds them to the clients list.
        """
        client_sock, client_addr = self.ssl_sock.accept()
        print(f'New connection created, client address: {client_addr}')
        self.clients.append(client_sock)
    
    def remove_client(self, client_sock: socket.socket) -> None:
        """
        Removes a client socket from the clients list and closes the connection.
        """
        if client_sock in self.clients:
            self.clients.remove(client_sock)
            client_sock.close()
            print(f'Client {client_sock} removed and connection closed')