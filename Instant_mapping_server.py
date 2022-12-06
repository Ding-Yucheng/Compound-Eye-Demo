"""
MicroPython on ESP32
"""
import usocket as socket
import time
from machine import ADC
from machine import Pin
from machine import ADC
import network
import esp
esp.osdebug(None)
import gc
gc.collect()

ssid = 'MyESP32'
password = '12345678'
host_ip = '192.168.137.16'
host_port = 80
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
PD_Cur = ADC(Pin(36, Pin.IN), atten=ADC.ATTN_11DB)
pd_data = []
sarr = ''
for i in range(0, 37):
    pd_data.append(0)


def scan():
    for i in range(4, 41):
        mux = i / 16
        pixel = i % 16
        M1.value(0)
        M2.value(0)
        M3.value(0)
        if mux == 0:
            M1.value(1)
        elif mux == 1:
            M2.value(1)
        elif mux == 2:
            M3.value(1)
        A0.value(1 & (pixel >> 0))
        A1.value(1 & (pixel >> 1))
        A2.value(1 & (pixel >> 2))
        A3.value(1 & (pixel >> 3))
        time.sleep_us(10)
        cache = 0
        for j in range (0, 50):
            cache += PD_Cur.read_uv()
            time.sleep_us(10)
            
        pd_data[i - 4] = int(cache / 50)
        ## connect to ground
        M1.value(0)
        M2.value(0)
        M3.value(1)
        A0.value(1)
        A1.value(1)
        A2.value(1)
        A3.value(1)
        time.sleep_ms(10)
        

def list_to_str():
    global sarr
    sarr = 'str'
    for i in range(0,37):
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
            conn.send(sarr.encode('utf-8'))
        else:
            time.sleep_us(100)
        continue

