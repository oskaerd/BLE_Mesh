import sqlite3
import socket
import sys

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
        print(list(data))
    else:
        conn.close()
        print('Closing')
        sys.exit(1)