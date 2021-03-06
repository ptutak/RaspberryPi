#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 12:12:08 2018

@author: ptutak
"""

import socket
import tkinter as tk
import time
import subprocess
HOST = '192.168.0.199'
PORT_COMMAND = 12000
HOST = input('ip host (default 192.168.0.199):')
if HOST=='':
    HOST='192.168.0.199'

print('host: ',HOST)

PORT_COMMAND = input('comm port (default 12000):')
if PORT_COMMAND=='':
    PORT_COMMAND=12000
else:
    PORT_COMMAND=int(PORT_COMMAND)
    
print('comm port:',PORT_COMMAND)
class Controls(tk.Frame):
    def __init__(self,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.parent=parent
        self.cameraProcess=None
        self.commandSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commandSocket.connect((HOST,PORT_COMMAND))
        self.yScroll=tk.Scrollbar(self,orient=tk.VERTICAL)
        self.yScroll.grid(row=0,column=4,sticky=tk.N+tk.S)
        self.infoStr=tk.StringVar()
        self.info=tk.Listbox(self,yscrollcommand=self.yScroll.set,listvariable=self.infoStr)
        self.info.grid(row=0,column=0,columnspan=4,sticky=tk.N+tk.S+tk.W+tk.E)
        self.leftButton=tk.Button(self,text='-')
        self.leftButton.grid(row=1,column=0)
        self.leftButton.bind('<Button-1>',self.minusButtonAction)
        self.rightButton=tk.Button(self,text='+')
        self.rightButton.grid(row=1,column=1)
        self.rightButton.bind('<Button-1>',self.plusButtonAction)
        self.startCameraButton=tk.Button(self,text='Start Camera')
        self.startCameraButton.grid(row=1,column=2)
        self.startCameraButton.bind('<Button-1>',self.startCameraButtonAction)
        self.stopCameraButton=tk.Button(self,text='Stop Camera')
        self.stopCameraButton.grid(row=1,column=3)
        self.stopCameraButton.bind('<Button-1>',self.stopCameraButtonAction)
        self.exitButton=tk.Button(self,text='Exit')
        self.exitButton.grid(row=1,column=4)
        self.exitButton.bind('<Button-1>',self.exitButtonAction)
    def minusButtonAction(self,event):
        self.commandSocket.send('servo left'.encode())
    def plusButtonAction(self,event):
        self.commandSocket.send('servo right'.encode())
    def startCameraButtonAction(self,event):
        self.commandSocket.send('startCam'.encode())
        port=int.from_bytes(self.commandSocket.recv(1024),'little')
        time.sleep(0.5)
        vlcRunArgs=['vlc','tcp/h264://'+str(HOST)+':'+str(port)]
        self.cameraProcess=subprocess.Popen(vlcRunArgs)
    def stopCameraButtonAction(self,event):
        self.commandSocket.send('stopCam'.encode())
        if self.cameraProcess:
            self.cameraProcess.terminate()
            self.cameraProcess=None
    def exitButtonAction(self,event):
        self.commandSocket.send('quit'.encode())
        if self.cameraProcess:
            self.cameraProcess.terminate()
        self.parent.destroy()

if __name__=='__main__':
    root=tk.Tk()
    controls=Controls(root)
    controls.pack()
    root.mainloop()