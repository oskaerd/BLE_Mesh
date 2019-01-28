import sqlite3
import socket
import sys
import os
import atexit

from mesh_packet import meshPacket, listToDict

''' Clean-up at exit '''
def exit_handler(server_fd, client_fd, db_conn):
    print('atexit')
    server_fd.close()
    client_fd.close()
    db_conn.close()

database_name = 'measurements.db'
db_insert_query = 'INSERT INTO measurements VALUES ('
db_create_table_cmd = 'CREATE TABLE measurements \
                (dev_id integer, temp real, humidity real, pressure real, \
                lux real, battery integer)'

# delete old data on startup
if os.path.isfile(database_name):
   os.remove(database_name)
   print('Old data removed')

measures_db = sqlite3.connect(database_name)

# create table measurements
measures_db.execute(db_create_table_cmd)

HOST = '127.0.0.1'
PORT = 3000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))

s.listen(10)
print('Socket listening ')

conn, addr = s.accept()
print( 'Connected to ' + addr[0] + ':' + str(addr[1]) )

atexit.register(lambda: exit_handler(s, conn, measures_db))

while True:
    data = conn.recv(1024)
    if len(data) > 0:
        # receive data and depending on opcode use proper table in db 
        measure = meshPacket(listToDict(data))
        measure.printValues()
        query = db_insert_query + measure.prepareDbQuery()
        query = query[:-2] + ')'
        print(query)
        # insert into database
        measures_db.execute(query)
        measures_db.commit()
    else:
        print('Closing')
        sys.exit(1)