import socket
import threading

class Entity:
    def __init__(self):
        raise NotImplementedError

    def connect(self, host, port):
        raise NotImplementedError
    
    def send(self, data):
        raise NotImplementedError
    
    def receive(self):
        raise NotImplementedError
    
    def close(self):
        raise NotImplementedError
    
class Peer(Entity):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
    
    def connect(self, host, port):
        self.sock.connect((host, port))
        self.connected = True
    
    def send(self, data):
        self.sock.sendall(data)
    
    def receive(self):
        return self.sock.recv(1024)
    
    def close(self):
        self.sock.close()
        self.connected = False