import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
import time
from matplotlib import ticker, cm
from itertools import islice
import math


fig = plt.figure(figsize = (10, 8))

pos = np.array([0,0,0,1])
center = 3
speed = np.array([0.1,0.4,0.7,1])
yposition = np.array([-2.598,-2.598,-2.598,-2.598,-1.732,-1.732,-1.732,-1.732,-1.732,-0.866,-0.866,-0.866,-0.866,-0.866,-0.866,0,0,0,0,0,0,0,0.866,0.866,0.866,0.866,0.866,0.866,1.732,1.732,1.732,1.732,1.732,2.598,2.598,2.598,2.598])
xposition = np.array([-1.5,-0.5,0.5,1.5,-2,-1,0,1,2,-2.5,-1.5,-0.5,0.5,1.5,2.5,-3,-2,-1,0,1,2,3,-2.5,-1.5,-0.5,0.5,1.5,2.5,-2,-1,0,1,2,-1.5,-0.5,0.5,1.5])
data1 = np.array([0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,2,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0])
data2 = np.array([0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,2,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0])
data3 = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,2,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0])
data4 = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,2,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0])
data = np.array([data1, data2, data3, data4])
def currentMap(xp,yp, current):
    ax1 = fig.add_subplot(1,1,1)    # 子图设置(x，y, No.)
    ax1.axis('off')    # 无边框
    im = ax1.scatter(xp,yp,s = 1600, c = current, cmap = "autumn", alpha = 0.6, marker = "h")
    cbar = ax1.figure.colorbar(im, ax=ax1)
    cbar.ax.set_ylabel("On-off ratio", rotation=-90, va="bottom")
    plt.ylim((-6, 6))
    plt.xlim((-6, 6))
    ax = plt.gca()
    ax.set_aspect(1)
    ##plt.show()

old = time.time()
plt.ion()
plt.clf()
for t in range(0, 100000):
    spd = speed[round(center)]
    now = time.time()
    center -= spd *(now - old)
    up = math.ceil(center)
    down = math.floor(center)
    dt = (1 - up + center) * data[up] + (1 - center + down) * data[down]
    plt.ioff()
    plt.clf()
    currentMap(xposition,yposition,dt)
    old = now
    plt.pause(0.1)
    if center < 0:
        break
