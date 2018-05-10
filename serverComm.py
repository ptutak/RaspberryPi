# -*- coding: utf-8 -*-

import socket
import sys
HOST = 'raspberry' # Server IP or Hostname
PORT_COMM = 12000 # Pick an open Port (1000+ recommended), must match the client sport
commSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    commSocket.bind((HOST, PORT_COMM))
except socket.error:
    print('Bind or connection failed')
    sys.exit(-1)
try:
    commSocket.listen(5)
    print('Command socket awaiting messages')
    (connection, addr) = commSocket.accept()
    print('Connected')
    while True:
        command = connection.recv(1024).decode()
        if command == 'Hello':
            connection.send('Hello there!'.encode())
        elif command == 'quit':
            break
except Exception as e:
    print(e)
finally:
    connection.close()
