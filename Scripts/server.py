import socket
from _thread import *

server = ""
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind(server, port)
except socket.error as e:
    str(e)

# 2 in listen as 2 players can connect
s.listen(2)
print("Waiting for a connection, Server Started")


def threaded_client(conn):
    pass


while True:
    # conn is an object representing what is connected
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn, ))
