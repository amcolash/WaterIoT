#!/usr/bin/env python

import mraa
import time

try:
  x = mraa.Gpio(13)
  x.dir(mraa.DIR_OUT)
  x.write(1)
  time.sleep(1)
  y = mraa.Aio(0)

  z = y.readFloat()
  z = 1 - min(z * 1.1933, 1)
  print ("%.5f" % z)
  x.write(0)
except:
  print ("Are you sure you have an ADC?")
