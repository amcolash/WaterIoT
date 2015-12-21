#!/usr/bin/env python

import RPi.GPIO as GPIO # Allows us to call our GPIO pins and names it just GPIO
import time
import signal
import sys
import auth
import twitter
import json
from __future__ import division
import spidev

# Define "enable" for the sensor
SENSOR_PIN = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.OUT)

twitter_api = twitter.Api(consumer_key=auth.consumer_key,
                  consumer_secret=auth.consumer_secret,
                  access_token_key=auth.access_token_key,
                  access_token_secret=auth.access_token_secret)

lastMessage = 0        # last time (in secs since epoch) that a notification was sent

# Gracefully quit on Ctrl-C and reset GPIO
def signal_handler(signal, frame):
  print(' Ctrl+C pressed, closing WaterPi')
  GPIO.output(SENSOR_PIN, GPIO.LOW)
  GPIO.cleanup()
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Create a function to run when the input is high
def sendMessage():
  global lastMessage
  global twitter_api
  if (time.time() - lastMessage > 86400):
    lastMessage = time.time()
    twitter_api.PostUpdate("Looks like I am pretty thirsty right now, @amcolash should feed me soon :)")

# Convert bit string to something usable
def bitstring(n):
  s = bin(n)[2:]
  return '0'*(8-len(s)) + s

# Read from SPI
def read(adc_channel=0, spi_channel=0):
  global conn
  cmd = 128
  if adc_channel:
    cmd += 32
  reply_bytes = conn.xfer2([cmd, 0])
  reply_bitstring = ''.join(bitstring(n) for n in reply_bytes)
  reply = reply_bitstring[5:15]
  return int(reply, 2) / 2**10

# Start a loop that never ends
while True:
  # Turn on voltage for the hygrometer
  GPIO.output(SENSOR_PIN, GPIO.HIGH)

  # Set up SPI connection
  conn = spidev.SpiDev(0, 0)
  conn.max_speed_hz = 1200000 # 1.2 MHz

  average = 0
  # Check for 10 seconds, every 100ms - average the result
  for i in range(1,100):
   value = 1.0 - max(0, read() - 0.4)
   average += (value - average) / i
   time.sleep(0.1)

  # Clean up SPI connection
  conn.close()

  # If average < 0.25 (dry), tweet at user
  sendMessage()

  # Open the json file
  with open('/home/pi/WaterPi/public/data.json') as f:
    data = json.load(f)

  # Get time/date
  timestamp = time.strftime('%x %X %Z')

  # Append to the temp json object
  data.update({timestamp : average})

  # Write changes to the file
  with open('/home/pi/WaterPi/public/data.json', 'w') as f:
    json.dump(data, f, sort_keys=True, indent=2)

  # Turn off voltage pin for 30 minutes to prevent wear
  GPIO.output(SENSOR_PIN, GPIO.LOW)
  sleep(1800)
