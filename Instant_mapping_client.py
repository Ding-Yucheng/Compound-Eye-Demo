import socket
import time
import sys
esp_ip = "192.168.137.16"
esp_port = 80

print("Starting socket: TCP...")
addr = (esp_ip, esp_port)
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        print("Connecting to server @ %s:%d..." %(esp_ip, esp_port))
        socket_tcp.connect(addr)
        break
    except Exception:
        print("Can't connect to server,try it latter!")
        time.sleep(1)
        continue
print("Connected!")

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
import time
from matplotlib import ticker, cm
from itertools import islice
import math


fig = plt.figure(figsize = (10, 8))
raw_data = []
for i in range(0, 48):
    raw_data.append(0)
pos = np.array([0,0,0,1])
center = 3
speed = np.array([0.1,0.4,0.7,1])
yposition = np.array([-2.598,-2.598,-2.598,-2.598,-1.732,-1.732,-1.732,-1.732,-1.732,-0.866,-0.866,-0.866,-0.866,-0.866,-0.866,0,0,0,0,0,0,0,0.866,0.866,0.866,0.866,0.866,0.866,1.732,1.732,1.732,1.732,1.732,2.598,2.598,2.598,2.598])
xposition = np.array([-1.5,-0.5,0.5,1.5,-2,-1,0,1,2,-2.5,-1.5,-0.5,0.5,1.5,2.5,-3,-2,-1,0,1,2,3,-2.5,-1.5,-0.5,0.5,1.5,2.5,-2,-1,0,1,2,-1.5,-0.5,0.5,1.5])
mask = np.array([19,12,13,20,26,21,14,8,7,6,11,18,25,27,32,31,30,24,17,10,5,28,22,15,9,4,3,2,1,33,37,36,35,34,29,23,16])
mask2 = np.array([37,36,35,34,33,25,26,27,28,29,30,31,32,24,23,22,21,20,19,18,17,9,10,11,12,13,14,15,16,8,7,6,5,4,3,2,1])
cur_nA = np.zeros(37)
def str_to_arr():
    for i in range(0, 37):
        cur_nA[mask[i] - 1] = int(raw_data[mask2[i] - 1])/ 2000

def currentMap(xp, yp, current):
    ax1 = fig.add_subplot(1,1,1)    # 子图设置(x，y, No.)
    ax1.axis('off')    # 无边框
    im = ax1.scatter(xp,yp,s = 1600, c = current, cmap = "Blues", alpha = 0.6, marker = "h")
    cbar = ax1.figure.colorbar(im, ax=ax1)
    cbar.ax.set_ylabel("On-off ratio", rotation=-90, va="bottom")
    plt.ylim((-6, 6))
    plt.xlim((-6, 6))
    ax = plt.gca()
    ax.set_aspect(1)
    ##plt.show()

while True:
    msg = 'next'
    print('next')
    socket_tcp.send(msg.encode('utf-8'))
    rmsg = socket_tcp.recv(8192)
    print(rmsg.decode('utf-8'))
    msg = 'wait'
    socket_tcp.send(msg.encode('utf-8'))
    str_data = (rmsg.decode('utf-8'))[3:-3]
    raw_data = str_data.split('.')
    str_to_arr()
    plt.ioff()
    plt.clf()
    print(cur_nA[15])
    currentMap(xposition, yposition, cur_nA)
    plt.pause(0.1)

socket_tcp.close()

