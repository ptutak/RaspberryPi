# -*- coding: utf-8 -*-

import socket

HOST = '192.168.0.199' # Server IP or Hostname
PORT_COMM = 12000 # Pick an open Port (1000+ recommended), must match the client sport
commSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
try:
    commSocket.bind((HOST, PORT_COMM))
except socket.error:
    print('Bind failed ')
try:
    commSocket.listen(5)
    print('Command socket awaiting messages')
    (connection, addr) = commSocket.accept()
    print('Connected')
    while True:
        data = connection.recv(1024).decode()
        if data == 'Hello':
            reply = 'Hello there!'
        elif data == 'This is important':
            reply = 'OK, I have done the important thing you have asked me!'
    
        #and so on and on until...
        elif data == 'quit':
            connection.send('Terminate'.encode())
            break
        else:
            reply = 'Unknown command'
        # Sending reply
        connection.send(reply.encode())
    connection.close() # Close connections
except Exception as e:
    print(e)
    connection.close()
