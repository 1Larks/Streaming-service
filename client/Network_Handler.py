import socket
import ssl

BUFFSIZE = 4096

class Network_Handler:
    """
    Handles network communication with the server using SSL sockets.
    """

    def __init__(self, server_addr, server_port):
        """
        Initializes the Network_Handler with the server address and port.
        """
        self.serv_addr = server_addr
        self.serv_port = server_port
        self.sock = None
        self.ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        self.ssl_sock = None
        self.buffers = {
            'salt': None,
            'auth': None,
            'search': None
        }
    
    def getAsyncBuffer(self, buff_name):
        """
        Retrieves data from the specified buffer asynchronously.
        Blocks until data is available.
        """
        while self.buffers[buff_name] is None:
            continue
        result = self.buffers[buff_name]
        self.buffers[buff_name] = None
        return result
    
    def connect_to_server(self):
        """
        Establishes a connection to the server using SSL.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ssl_sock = self.ssl_context.wrap_socket(self.sock, server_hostname=self.serv_addr)
        self.ssl_sock.connect((self.serv_addr, self.serv_port))
        print(f"Connected to server: {self.serv_addr}:{self.serv_port}")
    
    def send_data(self, data, text=False):
        """
        Sends data to the server over the SSL socket.
        """
        try:
            self.ssl_sock.sendall(data.zfill(BUFFSIZE).encode() if text else data)
        except Exception as err:
            print(f"Error sending data to server: {err}")
    
    def close_connection(self):
        """
        Closes the connection to the server.
        """
        if self.sock:
            self.sock.close()
            print("Connection closed")