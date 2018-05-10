#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 12:12:08 2018

@author: ptutak
"""

import socket
import tkinter as tk
HOST = 'raspberry' # Enter IP or Hostname of your server
PORT_COMMAND = 12000 # Pick an open Port (1000+ recommended), must match the server port
PORT_CAMERA = 13000
commandSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
commandSocket.connect((HOST,PORT_COMMAND))
import cv2
cap = cv2.VideoCapture(HOST)

while True:
  ret, frame = cap.read(HOST+':'+str(PORT_CAMERA)+'/')
  cv2.imshow('Video', frame)

  if cv2.waitKey(1) == 27:
    exit(0)

class Controls(tk.Frame):
    def __init__(self,*args,**kwargs):
        super(*args,**kwargs)
        self.upButton=tk.Button(self,text='Up')
        self.downButton=tk.Button(self,text='Down')
        self.startCameraButton=tk.Button(self,text='Start Camera')
        self.stopCameraButton=tk.Button(self,text='Stop Camera')
        self.exitButton=tk.Button(self,text='Exit')
