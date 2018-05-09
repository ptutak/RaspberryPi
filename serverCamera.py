# -*- coding: utf-8 -*-

import socket
import picamera
import time

HOST = '192.168.0.199' # Server IP or Hostname
PORT_CAMERA = 13000 # Pick an open Port (1000+ recommended), must match the client sport
cameraSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    cameraSocket.bind((HOST, PORT_CAMERA))
except socket.error:
    print('Bind failed ')

recording=False
with picamera.PiCamera() as camera:
    camera.resolution(1024,768)
    camera.framerate(24)
try:
    cameraSocket.listen(5)
    print('Camera waiting for connection')
    (connection, address) = cameraSocket.accept()
    connection=connection.makefile('wb')
    print('Camera connected')
    camera.start_preview()
    time.sleep(2)
    camera.start_recording(connection,format='h264')
    recording=True
    while True:
        command=connection.recv(1024).decode()
        if command=='stop' and recording:
            camera.stop_recording()
            recording=False
        elif command=='start' and not recording:
            camera.start_recording()
            recording=True
        elif command=='quit':
            break
except Exception as e:
    print(e)
finally:
    if recording:
        camera.stop_recording()
    connection.close()