import socket
import os
import threading 
from threading import Thread

clients = set()
clients_lock = threading.Lock()

def serverlistener(client, address):
    print(f'Accepted Connection From: {addr[0]}:{addr[1]}')
    with clients_lock:
        clients.add(client)
    try:
        while True:
            data = client.recv(1024)
            if not data:
                break
            else:
                print(repr(data))
                with clients_lock:
                    for c in clients:
                        c.sendall(data)
    finally:
        with clients_lock:
            clients.remove(client)
            client.close()




s = socket.socket()
HOST = '172.16.75.74'
PORT = 1234

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)

th = []

# def check

# checksum = threading.timer(10, function, [function_arguments])
# while True:
#     checksum.start()



while True:
    print('Server is listening for connections...')
    conn, addr = s.accept()
    th.append(Thread(target=serverlistener, args=(conn, addr)).start())

s.close()
