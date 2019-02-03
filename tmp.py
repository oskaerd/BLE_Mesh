import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import atexit

import sqlite3
import socket
import os
import sys
import _thread
from collections import deque

from mesh_packet import meshPacket, listToDict
from db_interface import database_interface
from db_interface import database_filename, db_create_table_cmd, db_insert_query

th_server = False

X = deque(maxlen=20)

REFRESH_RATE = 1
HOST = '127.0.0.1'
PORT = 3000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))

s.listen(10)
print('Socket listening ')

conn, addr = s.accept()
print( 'Connected to ' + addr[0] + ':' + str(addr[1]) )

style.use('dark_background')

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

def window_cls_handle(evt):
    sys.exit(2)

fig.canvas.mpl_connect('close_event', window_cls_handle)

i=0

def animate(i):
    measurements_db = database_interface()
    X.append(i)
    i+=1
    graph_data = []
    xs = X
    ys = []
    yss = []
    graph_data = measurements_db.getData()
    yss=ys
    yss = [i +1 for i in yss]

    ax1.clear()
    ax1.plot(xs, ys, '.-')
    ax1.plot(xs, yss, '.-')
    measurements_db.closeConn()

def server(dummy):
    # delete old data on startup
    if os.path.isfile(database_filename):
        os.remove(database_filename)
        print('Old data removed')

    measurements_db = database_interface()

    # create table measurements
    measurements_db.newTable('measurements')
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
            measurements_db.writeData(query)
            measurements_db.commit()
        else:
            print('Closing')
            sys.exit(1)

def onClose(conn, s):
    conn.close()
    s.close()

if __name__=="__main__":
    atexit.register(lambda: onClose(conn, s))
    th_server = _thread.start_new_thread(server, ('server',))
    ani = animation.FuncAnimation(fig, animate, interval=1000*REFRESH_RATE)
    plt.show()

    while True:
        pass
