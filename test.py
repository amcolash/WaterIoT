#!/usr/bin/python

import spidev
import time
import os

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

# Define delay between readings
delay = 0.1

average = 0
count = 0

while True:

  channel_0 = ReadChannel(0)

  count += 1
  average += (channel_0 - average) / count

  # converted = (channel_0 - 350) / 1020.0
  # Print out results
  print(channel_0)
  # print(average)


  # Wait before repeating loop
  time.sleep(delay)
