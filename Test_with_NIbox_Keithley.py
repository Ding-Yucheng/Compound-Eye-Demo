import time, socket, csv, niswitch, pyvisa, ipympl
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from pathlib import Path
import matplotlib as mpl
from matplotlib import ticker, cm
from itertools import islice
from IPython import display

UDP_IP = '127.0.0.2'
UDP_Port = 9100


def keiread(fileName):
    kei.write("smu.measure.read()")
    curr = (kei.query("print(defbuffer1.readings[defbuffer1.endindex])"))
    return curr

def scan():
    global sum_cur, center_x, center_y
    sum_cur = 0
    center_x = 0
    center_y = 0
    for j in range(0,37): #Loop multiplexer
        thisChannel = "ch"+str(j)
        mux[0].connect(channel1=thisChannel, channel2='com0')
        curr = keiread(fileName)
        data = np.array(["{:.2f}".format(time.time()),0,j,float(curr)])
        raw_data[j] = float(curr)
        sum_cur += raw_data[j]
        center_x += raw_data[j] * x_pos[j]
        center_y += raw_data[j] * y_pos[j]
        mux[0].disconnect(channel1=thisChannel, channel2='com0')
    center_x *= 3
    center_y *= 3
    center_x /= sum_cur
    center_y /= sum_cur

def currentMap(xp, yp, current, cx, cy):
    ax1 = fig.add_subplot(1,1,1)
    ax1.axis('off')
    im = ax1.scatter(cx, cy, s = 150, c = 'r', marker = 'o')
    im = ax1.scatter(xp, yp, s = 1600, c = current, cmap = "Blues", alpha = 0.6, marker = "h")
    cbar = ax1.figure.colorbar(im, ax=ax1)
    cbar.ax.set_ylabel("Current", rotation=-90, va="bottom")
    plt.ylim((-6, 6))
    plt.xlim((-6, 6))
    ax = plt.gca()
    ax.set_aspect(1)
 
#isnt initial
rm = pyvisa.ResourceManager()
intList = rm.list_resources()
print(intList)
kei = rm.open_resource(intList[0]) #'USB0::0x05E6::0x2450::04472599::keiR')
print(kei.query("*IDN?"))

#Functions
timestr = time.strftime("%Y%m%d_%H%M%S")
folder = 'data'
fileName = folder+"/eEye_"+timestr+".csv"
Path(folder).mkdir(parents=True, exist_ok=True)
def write_csv(fileName,data):
    with open(fileName, 'a') as outfile:
        writer = csv.writer(outfile,  lineterminator='\n')
        writer.writerow(data)

timestr = time.strftime("%Y%m%d_%H%M%S")
folder = 'data'
fileName = folder+"/IR_"+"on"+timestr+".csv"
#initializing NI box
mux=[]
mux.append(niswitch.Session(resource_name="PXI1Slot3_2"))
print('PXI-mux init ok')

mux[0].reset()
time.sleep(1)

x_pos = np.array([-1.5,-0.5,0.5,1.5,2,2.5,3,2.5,2,1.5,0.5,-0.5,-1.5,-2,-2.5,-3,-2.5,-2,-1,0,1,1.5,2,1.5,1,0,-1,-1.5,-2,-1.5,-0.5,0.5,1,0.5,-0.5,-1,0])
y_pos = np.array([-2.598076211,-2.598076211,-2.598076211,-2.598076211,-1.732050808,-0.866025404,0,0.866025404,1.732050808,2.598076211,2.598076211,2.598076211,2.598076211,1.732050808,0.866025404,0,-0.866025404,-1.732050808,-1.732050808,-1.732050808,-1.732050808,-0.866025404,0,0.866025404,1.732050808,1.732050808,1.732050808,0.866025404,0,-0.866025404,-0.866025404,-0.866025404,0,0.866025404,0.866025404,0,0])
raw_data = np.zeros(37)
sum_cur = 0
center_x = 0
center_y = 0
mpl.use('TkAgg') # if no plot window
fig = plt.figure(figsize = (10, 8))

while True:
    scan()
    plt.ioff()
    plt.clf()
    currentMap(x_pos, y_pos, raw_data, center_x, center_y)
    plt.pause(0.1)

