import socket
import time

from mesh_packet import meshPacket, meshPacketTestCase

packets = []

test = meshPacket(meshPacketTestCase().getRandomData())

print(test.dictToBytesArray())

test.updateValues()

# client_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server_fd = client_fd.connect(('127.0.0.1', 3000))

# while True:
#     client_fd.send(bytes([7]))
#     time.sleep(5)

# print('bb')
# server_fd.close()
# client_fd.close()