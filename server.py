import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = '192.168.20.71'
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

currentId = "0"
pos = ["0:50", "1:100"]
def threaded_client(conn):
    global currentId, pos
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            if not data:
                conn.send(str.encode("Bye Bye"))
                break
            else:
                print("Recieved: " + reply)
            conn.sendall(reply)
        except:
            break

    print("Conexión cerrada")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Conectado a: ", addr)

    start_new_thread(threaded_client, (conn,))