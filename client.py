#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 12:12:08 2018

@author: ptutak
"""

import socket
import cv2
import tkinter as tk
import numpy as np
import subprocess

HOST = '192.168.0.199' # Enter IP or Hostname of your server
PORT_COMMAND = 12000 # Pick an open Port (1000+ recommended), must match the server port
PORT_CAMERA = 13000
#commandSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#commandSocket.connect((HOST,PORT_COMMAND))

#cameraSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#cameraSocket.connect((HOST,PORT_CAMERA))

vlcRunArgs=['vlc','tcp/h264://192.168.0.199:13000']
subprocess.call(vlcRunArgs)


class Controls(tk.Frame):
    def __init__(self,*args,**kwargs):
        super(*args,**kwargs)
        self.yScroll=tk.Scrollbar(self,orient=tk.VERTICAL)
        self.yScroll.grid(row=0,column=4,sticky=tk.N+tk.S)
        self.infoStr=tk.StringVar()
        self.info=tk.Listbox(self,yscrollcommand=self.yScroll.set,listvariable=self.infoStr)
        self.info.grid(row=0,column=0,columnspan=4,sticky=tk.N+tk.S+tk.W+tk.E)
        self.leftButton=tk.Button(self,text='Left')
        self.leftButton.grid(row=1,column=0)
        self.rightButton=tk.Button(self,text='Right')
        self.rightButton.grid(row=1,column=1)
        self.startCameraButton=tk.Button(self,text='Start Camera')
        self.startCameraButton.grid(row=1,column=2)
        self.stopCameraButton=tk.Button(self,text='Stop Camera')
        self.stopCameraButton.grid(row=1,column=3)
        self.exitButton=tk.Button(self,text='Exit')
        self.exitButton.grid(row=1,column=4)
