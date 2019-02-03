from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as Tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

import socket
import os
import sys
import _thread
import atexit 
import datetime
import random
from collections import deque

from mesh_packet import meshPacket, listToDict
from db_interface import database_interface, database_filename
from db_interface import db_insert_query

style.use('dark_background')

fig = plt.Figure()
ax1 = fig.add_subplot(111)

x = np.arange(0, 2*np.pi, 0.01)        # x-array

MAXLEN = 20
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

# delete old data on startup
try:
    os.remove(database_filename)
    print('Old data removed')
except:
    pass

X = deque(maxlen=MAXLEN+1)
Y = deque(maxlen=MAXLEN+1)
YY = deque(maxlen=MAXLEN+1)

import math
i = 1

def animate(i):
    measurement_db = database_interface()
    X.append(i)
    i+=1
    Y = []
    YY = []

    graph_data = measurement_db.getData()
    for meas in graph_data:
        Y.append(meas[1])
        YY.append(meas[1] + float(random.randrange(-20, 20, 1))/10)
    print(X)
    print(Y)
    ax1.clear()
    ax1.plot(X, Y, '-.')
    ax1.plot(X, YY, '-.')

def server(dummy):
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

root = Tk.Tk()

label = Tk.Label(root,text="BLE Sensor Data").grid(column=0, row=0)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0,row=1)

ani = animation.FuncAnimation(fig, animate, interval=1000*REFRESH_RATE, blit=False)

if __name__=="__main__":
    th_server = _thread.start_new_thread(server, ('server',))
    Tk.mainloop()
    while True:
        pass