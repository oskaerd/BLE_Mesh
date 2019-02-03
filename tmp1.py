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
from collections import deque

from mesh_packet import meshPacket, listToDict
from db_interface import database_interface

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

X = deque(maxlen=MAXLEN+1)
Y = deque(maxlen=MAXLEN+1)
YY = deque(maxlen=MAXLEN+1)

import math
i = 1

def animate(i):
    X.append(i)
    Y.append(math.cos(i*math.pi/10))
    YY.append(math.sin(i*math.pi/10))
    
    ax1.clear()
    ax1.plot(X, Y, '-.')
    ax1.plot(X, YY, '-.')
    

root = Tk.Tk()

label = Tk.Label(root,text="BLE Sensor Data").grid(column=0, row=0)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0,row=1)

ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), interval=25, blit=False)

Tk.mainloop()