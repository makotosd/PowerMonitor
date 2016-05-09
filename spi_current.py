#!/usr/bin/env python

import time
import sys
import spidev
from datetime import datetime
import math

R = 20      ## Register
baseV = 430 ## base voltage
N = 2000    ## number of coil loop

spi = spidev.SpiDev()
spi.open(0,0)

def readAdc(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

def getVolt():
    s = 0
    n = 10000

    for i in range(n):
      data = readAdc(0);
      s += (data - baseV)^2

    return math.sqrt(float(s)/n)

if __name__ == '__main__':
    try:

        i = 0
        while True:
            now=datetime.now()
            current = readAdc(0)

            print("{:d}, ".format(i)),
            print datetime.now().strftime("%Y/%m/%d %H:%M:%S"), 
            print(", {:8.3f} ".format(current))

            i+=1

    except KeyboardInterrupt:
        spi.close()
        sys.exit(0)



