import socket
import time

from mesh_packet import meshPacket, meshPacketTestCase

packets = []

# create test data
test = meshPacket(meshPacketTestCase().getRandomData())

print(test.dictToBytesArray())


try:
    client_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_fd = client_fd.connect(('127.0.0.1', 3000))

    while True:
        client_fd.send( test.dictToBytesArray() )
        # update random values
        test.updateValues()
        time.sleep(5)
except KeyboardInterrupt:
    print('bb')
    client_fd.close()