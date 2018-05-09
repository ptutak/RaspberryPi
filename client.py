#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 12:12:08 2018

@author: ptutak
"""

import socket

HOST = '192.168.0.199' # Enter IP or Hostname of your server
PORT = 12000 # Pick an open Port (1000+ recommended), must match the server port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

#Lets loop awaiting for your input
while True:
    command = input('Enter your command: ')
    s.send(command.encode())
    reply = s.recv(1024).decode()
    if reply == 'Terminate':
        break
    print(reply)