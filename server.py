# -*- coding: utf-8 -*-

import socket
import sys
import picamera
import time
import threading
HOST = '192.168.0.199'
PORT_COMM = 12000
PORT_CAMERA = 13000

class CameraThread(threading.Thread):
    def __init__(self,camera, port,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.cameraSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cameraSocket.bind((HOST, port))
        self.recording=threading.Condition()
        self.camera=camera
    def run(self):
        rec=False
        try:
            self.cameraSocket.listen(5)
            print('Camera waiting for connection')
            (self.connection, address) = self.cameraSocket.accept()
            connectionFile=self.connection.makefile('wb')
            print('Camera connected')
            self.camera.start_recording(connectionFile,format='h264',quality=25)
            rec=True
            print('Camera started recording')
            self.recording.acquire()
            self.recording.wait()
            self.recording.release()
            self.camera.stop_recording()
            rec=False
        finally:
            if rec:
                self.camera.stop_recording()
            self.connection.close()
            print('Camera stopped')
    def stopCamera(self):
        self.recording.acquire()
        self.recording.notify_all()
        self.recording.release()

class CommandThread(threading.Thread):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.commSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commSocket.bind((HOST, PORT_COMM))
        self.camera=picamera.PiCamera()
        self.camera.resolution=(640,480)
        self.camera.framerate=25
    def run(self):
        self.commSocket.listen(5)
        print('Command socket awaiting messages')
        (self.connection, addr) = self.commSocket.accept()
        print('Connected')
        port=0
        try:
            while True:
                command = self.connection.recv(1024).decode()
                if command == 'startCam':
                    if not self.cameraThread:
                        self.cameraThread=CameraThread(self.camera,PORT_CAMERA+port)
                        self.connection.send((PORT_CAMERA+port).to_bytes(2,'little'))
                        port+=1
                        if port==1000:
                            port=0
                        self.cameraThread.start()
                elif command == 'stopCam':
                    if self.cameraThread:
                        self.cameraThread.stopCamera()
                        self.cameraThread=None
                elif command == 'quit':
                    break
        except Exception as e:
            print(e)
        finally:
            self.connection.close()
            print('Command stopped')

if __name__=='__main__':
    commandT=CommandThread()
    commandT.start()