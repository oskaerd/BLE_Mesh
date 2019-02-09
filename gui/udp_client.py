import socket

UDP_IP = "192.168.0.38"
UDP_PORT = 9001
MESSAGE = "Hello, World!"


sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(bytes(MESSAGE, 'ascii'), (UDP_IP, UDP_PORT))