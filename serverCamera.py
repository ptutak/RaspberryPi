# -*- coding: utf-8 -*-

import socket
import picamera
import time

HOST = '192.168.0.199'
PORT_CAMERA = 13000
cameraSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    cameraSocket.bind((HOST, PORT_CAMERA))
except socket.error:
    print('Bind failed ')
else:
    
    recording=False
    camera=picamera.PiCamera()
    try:
        camera.resolution=(640,480)
        cameraSocket.listen(5)
        print('Camera waiting for connection')
        (connection, address) = cameraSocket.accept()
        connectionFile=connection.makefile('wb')
        print('Camera connected')
        #camera.start_preview()
        #time.sleep(2)
        camera.start_recording(connectionFile,format='h264',quality=23)
        recording=True
        while recording:
            pass
    except BrokenPipeError as e:
        print(e)
        print('hello')
        if recording:
            camera.stop_recording()
    finally:
        connection.close()
