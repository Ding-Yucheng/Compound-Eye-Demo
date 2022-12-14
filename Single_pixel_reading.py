import time
from machine import ADC
from machine import Pin

sampling_interval_us = 1000

print ('\r\n\r\nTello Python3 Demo.\r\n')

A0 = Pin(26, Pin.OUT)
A1 = Pin(25, Pin.OUT)
A2 = Pin(33, Pin.OUT)
A3 = Pin(32, Pin.OUT)
M1 = Pin(27, Pin.OUT)
M2 = Pin(14, Pin.OUT)
M3 = Pin(13, Pin.OUT)
PD_Cur = ADC(Pin(36, Pin.IN), atten = ADC.ATTN_6DB)

M1.value(1)
M2.value(0)
M3.value(0)
A0.value(0)
A1.value(0)
A2.value(1)
A3.value(1)
while True: 
    print(PD_Cur.read_uv())
    time.sleep_us(sampling_interval_us)
