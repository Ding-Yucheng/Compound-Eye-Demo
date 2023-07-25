"""
MicroPython on ESP32
"""
import usocket as socket
import time
from machine import ADC
from machine import Pin
import network
import esp
esp.osdebug(None)
import gc
gc.collect()

# Sampling setting
sample_per_pixel = 200
reject_first_samples = 100
sampling_interval = 10 # in microseconds
waiting_time = 10 # in milliseconds
blank_sampling = 50

# Network setting
ssid = 'MyESP32'
password = '12345678'
host_ip = '192.168.137.232'
host_port = 54080

station = network.WLAN(network.STA_IF)
station.active(True)

while station.isconnected() == False:
    station.connect(ssid, password)
    pass

print('Connection successful')
print(station.ifconfig())

addr = socket.getaddrinfo(host_ip, host_port)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
conn, addr = s.accept()
print('listening on', addr)

A0 = Pin(26, Pin.OUT)
A1 = Pin(25, Pin.OUT)
A2 = Pin(33, Pin.OUT)
A3 = Pin(32, Pin.OUT)
M1 = Pin(27, Pin.OUT)
M2 = Pin(14, Pin.OUT)
M3 = Pin(13, Pin.OUT)
PD_Cur = ADC(Pin(36, Pin.IN), atten = ADC.ATTN_0DB)

sarr = ''
pd_data = []
for i in range(0, 37):
    pd_data.append(0)

def select_mux(m1, m2, m3):
    M1.value(m1)
    M2.value(m2)
    M3.value(m3)

def select_channel(a0, a1, a2, a3):
    A0.value(a0)
    A1.value(a1)
    A2.value(a2)
    A3.value(a3)

def scan():
    for i in range(4, 41):
        mux = i / 16
        pixel = i % 16
        if mux == 0:
            select_mux(1, 0, 0)
        elif mux == 1:
            select_mux(0, 1, 0)
        elif mux == 2:
            select_mux(0, 0, 1)
        select_channel(1 & (pixel >> 0), 1 & (pixel >> 1), 1 & (pixel >> 2), 1 & (pixel >> 3))
        time.sleep_ms(waiting_time)
        cache = 0
        for j in range (0, sample_per_pixel + reject_first_samples):
            if j >= reject_first_samples:
                cache += PD_Cur.read_uv()
            time.sleep_us(sampling_interval)
        pd_data[i - 4] = int(cache / sample_per_pixel)
        
        select_mux(0, 0, 1)
        select_channel(1, 0, 1, 0)
        for j in range (0, blank_sampling):
            time.sleep_us(sampling_interval)

        

def list_to_str():
    global sarr
    sarr = 'str'
    for i in range(0, 37):
        sarr += str(pd_data[i])
        sarr += '.'
    sarr += 'end'

print('\r\n\r\nTello Python3 Demo.\r\n')

while True:
    request = conn.recv(512)
    if len(request) > 0:
        print("Received:%s"%request)
        if request.decode('utf-8') == 'next':
            scan()
            list_to_str()
            print(sarr)
            conn.send(sarr.encode('utf-8'))
        else:
            time.sleep_us(100)
        continue
