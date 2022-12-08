import socket
import time
import sys
esp_ip = "192.168.137.232"
esp_port = 54080

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
print("Connected!", addr)


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
for i in range(0, 37):
    raw_data.append(0)
center = 3
y_pos = np.array([0,-0.5,0.5,1,0.5,2,1.5,1,0,-1,-1.5,-1,-0.5,1.5,1,0,-1,-1.5,-2,-2.5,-2,2.5,3,2.5,2,1.5,0.5,-0.5,-1.5,2,1.5,0.5,-0.5,-1.5,-2,-2.5,-3])
x_pos = np.array([0,-0.866025404,-0.866025404,0,0.866025404,0,-0.866025404,-1.732050808,-1.732050808,-1.732050808,-0.866025404,0,0.866025404,0.866025404,1.732050808,1.732050808,1.732050808,0.866025404,0,-0.866025404,-1.732050808,0.866025404,0,-0.866025404,-1.732050808,-2.598076211,-2.598076211,-2.598076211,-2.598076211,1.732050808,2.598076211,2.598076211,2.598076211,2.598076211,1.732050808,0.866025404,0])
cur_nA = np.zeros(37)
sum_cur = 0
center_x = 0
center_y = 0
def str_to_arr():
    global sum_cur, center_x, center_y
    sum_cur = 0
    center_x = 0
    center_y = 0
    for i in range(0, 37):
        cur_nA[i] = (int(raw_data[i]) - 100000)/ 2000
        sum_cur += cur_nA[i]
        center_x += cur_nA[i] * x_pos[i]
        center_y += cur_nA[i] * y_pos[i]
    center_x /= sum_cur
    center_y /= sum_cur

def currentMap(xp, yp, current, cx, cy):
    ax1 = fig.add_subplot(1,1,1)    # 子图设置(x，y, No.)
    ax1.axis('off')    # 无边框
    im = ax1.scatter(cx, cy, s = 150, c = 'r', marker = 'o')
    im = ax1.scatter(xp, yp, s = 1600, c = current, cmap = "Blues", alpha = 0.6, marker = "H")
    cbar = ax1.figure.colorbar(im, ax=ax1)
    cbar.ax.set_ylabel("On-off ratio", rotation=-90, va="bottom")
    plt.ylim((-6, 6))
    plt.xlim((-6, 6))
    ax = plt.gca()
    ax.set_aspect(1)

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
    print(cur_nA)
    plt.ioff()
    plt.clf()
    currentMap(x_pos, y_pos, cur_nA, center_x, center_y)
    plt.pause(0.1)

socket_tcp.close()
