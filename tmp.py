import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import atexit

import socket
import os
import sys
import _thread
from collections import deque

from mesh_packet import meshPacket, listToDict

database_filename = 'measurements.db'
db_read_query_head = 'SELECT *'
db_read_values = 'dev_id, temp, humidity, pressure, lux, battery)'
db_read_query_tail = ' from measurements'
db_create_table_cmd = 'CREATE TABLE measurements \
                (dev_id integer, temp real, humidity real, pressure real, \
                lux real, battery integer)'
db_insert_query = 'INSERT INTO measurements VALUES ('
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

def animate(i):
    measurements_db = sqlite3.connect(database_filename)

    graph_data = []
    xs = []
    ys = []
    yss = []
    graph_data = measurements_db.execute(db_read_query_head + db_read_query_tail)
    graph_data = graph_data.fetchall()

    i=0
    for meas in graph_data:
        xs.append(i)
        i+=1
        ys.append(meas[1])
    yss=ys
    yss = [i +1 for i in yss]

    ax1.clear()
    ax1.plot(xs, ys, '.-')
    ax1.plot(xs, yss, '.-')
    measurements_db.close()

def server(dummy):
    # delete old data on startup
    if os.path.isfile(database_filename):
        os.remove(database_filename)
        print('Old data removed')

    measurements_db = sqlite3.connect(database_filename)

    # create table measurements
    measurements_db.execute(db_create_table_cmd)
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
            measurements_db.execute(query)
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