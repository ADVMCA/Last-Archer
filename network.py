from copyreg import pickle
import socket, pickle


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "192.168.20.194" 
        self.port = 5555
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        data = self.client.recv(2048)
        return pickle.loads(data)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            receivedData = self.client.recv(2048)
            reply = pickle.loads(receivedData)
            return reply
        except socket.error as e:
            return str(e)