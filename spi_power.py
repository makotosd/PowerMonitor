# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
## SLEEP時間とループ数の調整
##   - Sleep = 0.001[sec]では、10000回計測に約13秒。
##     つまり、769samples/sec = 15[samples]/20[msec]
##     このときCPU負荷は0.3くらい
##   - Sleep = 0.002[sec]では、10000回計測に約22秒
##     つまり、9.1[samples]/20[msec]
##     このときCPU負荷は0.15くらい。

import time
import sys
import spidev
from datetime import datetime
import math
import milkcocoa.milkcocoa as milkcocoa
import socket

#############################################################

R     = 136              ## [Ohm]
Vavg  = 439              ## base voltage
N     = 2000             ## number of coil loop
Vfs   = 3.3              ## Full Scale Voltage
FS    = 1024.0           ## Full Scale
Scale = float(Vfs) / FS  ## voltage vs ditital scale

spi = spidev.SpiDev()
spi.open(0,0)

#############################################################
def readAdc(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

def getADC():
    s = 0.0
    n = 10000  ## 16  [sec]

    for i in range(n):
      data = readAdc(0);
      s = s + (data - Vavg)**2
      #time.sleep(0.001) ## sleep 1[ms]
      time.sleep(0.002) ## sleep 2[ms]

    return math.sqrt(float(s)/n)

#############################################################
REMOTE_SERVER = "mlkcca.com"
def is_connected():
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(REMOTE_SERVER)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False

#############################################################

if __name__ == '__main__':
    try:

        while True:
            now=datetime.now()
            current = (getADC() * Scale) * N / R

            print datetime.now().strftime("%Y/%m/%d %H:%M:%S"), 
            print(", {:8.3f} ".format(current))

            if is_connected():
              try: 
                milkcocoaClient = milkcocoa.Milkcocoa.connectWithApiKey("woodinxbh8ig", "HFFDBBDFANGNBJJB", "iSBiAcPdAJDnfaiSkdAEEGOSZajbGVXnALUbBCDT", useSSL=False)
                datastore = milkcocoaClient.datastore("PowerMonitor")
                datastore.push({"current_v100":current})
              except:
                print "# NoConnectionException"

            else:
              print "# NoConnection"
            
            
    except KeyboardInterrupt:
        spi.close()
        sys.exit(0)

######################################################################
