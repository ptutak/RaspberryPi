# -*- coding: utf-8 -*-

import socket
import sys
import picamera
import time
import threading
HOST = '192.168.0.199' # Server IP or Hostname
PORT_COMM = 12000 # Pick an open Port (1000+ recommended), must match the client sport
PORT_CAMERA = 13000

class CameraThread(threading.Thread):
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.cameraSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cameraSocket.bind((HOST, PORT_CAMERA))
        self.recording=False
        self.camera=picamera.PiCamera()
    def run(self):
        try:
            self.camera.resolution=(640,480)
            self.cameraSocket.listen(5)
            print('Camera waiting for connection')
            (self.connection, address) = self.cameraSocket.accept()
            connectionFile=self.connection.makefile('wb')
            print('Camera connected')
            #camera.start_preview()
            self.camera.start_recording(connectionFile,format='h264',quality=23)
            self.recording=True
            while self.recording:
                time.sleep(60)
        except Exception as e:
            print(e)
            print('hello')
            if self.recording:
                self.camera.stop_recording()
        finally:
            self.connection.close()
    def stopCamera(self):
        if self.recording:
            self.recording=False
            self.camera.stop_recording()
            self.connection.close()
            print('Camera waiting for connection')
            (self.connection,address) = self.cameraSocket.accept()


class CommandThread(threading.Thread):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.commSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commSocket.bind((HOST, PORT_COMM))
    def run(self):
        self.commSocket.listen(5)
        print('Command socket awaiting messages')
        (connection, addr) = commSocket.accept()
        print('Connected')
        try:
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

if __name__=='__main__':
    cameraT=CameraThread()
    commandT=CommandThread()
    cameraT.start()
    commandT.start()