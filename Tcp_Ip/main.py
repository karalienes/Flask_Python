#!/usr/bin/env python

import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 9090
BUFFER_SIZE = 1024
MESSAGE = "startCamera\r\n"
MESSAGE_Byte = bytes(MESSAGE, 'UTF-8')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE_Byte)
data = s.recv(BUFFER_SIZE)
s.close()

print("received data:", data)
