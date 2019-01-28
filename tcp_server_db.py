import sqlite3
import socket
import sys
from mesh_packet import meshPacket, listToDict

HOST = '127.0.0.1'
PORT = 3000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))

db_insert_query = ''

s.listen(10)
print('Socket listening ')

conn, addr = s.accept()
print( 'Connected to ' + addr[0] + ':' + str(addr[1]) )

while True:
    data = conn.recv(1024)
    if len(data) > 0:
        # receive data and depending on opcode use proper table in db 
        measure = meshPacket(listToDict(data))

        # insert into database

    else:
        conn.close()
        s.close()
        print('Closing')
        sys.exit(1)