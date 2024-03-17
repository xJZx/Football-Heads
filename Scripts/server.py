import socket
from _thread import *

server = '127.0.0.1'
port = 5555
thread_count = 0

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.bind((server, port))
except socket.error as e:
    str(e)

# 2 in listen as 2 players can connect
server_socket.listen(2)
print("Waiting for a connection, Server Started")


def threaded_client(connection):
    connection.send(str.encode("Player joined"))

    while True:
        data = connection.recv(2048)
        reply = "Server Received: " + data.decode("utf-8")
        if not data:
            break
        connection.sendall(str.encode(reply))
    connection.close()


while True:
    # connection is an object representing what is connected
    connection, address = server_socket.accept()
    print("Connected to: ", address)

    start_new_thread(threaded_client, (connection, ))
    thread_count += 1
    print("Thread number: " + str(thread_count))

server_socket.close()
