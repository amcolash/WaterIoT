#!/usr/bin/env python

from __future__ import division # treat all division as non-integer division (remainders)

import mraa
import time
import signal
import sys
import auth
import twitter
import json

# Path to use for web server / checkout and data
PATH='/home/root/WaterIoT/'

# Define "enable" for the sensor
SENSOR = 0
OUTPUT = 13
sensor_pin = mraa.Gpio(OUTPUT)
input_pin = mraa.Aio(SENSOR)

# Set up min/max for normal plat - this defines range of values
MIN = 0.75
MAX = 0.971
MAGIC_NUMBER = pow(MAX - MIN, -1)

NUMBER_OF_SAMPLES = 200

twitter_api = twitter.Api(consumer_key=auth.consumer_key,
                  consumer_secret=auth.consumer_secret,
                  access_token_key=auth.access_token_key,
                  access_token_secret=auth.access_token_secret)

lastMessage = 0        # last time (in secs since epoch) that a notification was sent

# Gracefully quit on Ctrl-C and reset GPIO
def signal_handler(signal, frame):
  print(' Ctrl+C pressed, closing WaterPi')
  sensor_pin.write(0)
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Create a function to run when the input is high
def sendMessage():
  global lastMessage
  global twitter_api
  if (time.time() - lastMessage > 86400):
    lastMessage = time.time()
    twitter_api.PostUpdate('Looks like I am pretty thirsty right now, @amcolash should feed me soon :)')

# Start a loop that never ends
while True:
  # Turn on voltage for the hygrometer
  sensor_pin.write(1)
  time.sleep(0.5)

  average = 0
  # Check for 10 seconds, every 100ms - average the result
  for i in range(1, NUMBER_OF_SAMPLES):
   value = 1.0 - min(input_pin.readFloat() * MAGIC_NUMBER, 1)
   average += (value - average) / i
   time.sleep(0.05)

  print('average: ' + str(average))

  # If dry, tweet at user
  if (average < 0.35):
    sendMessage()

  # Open the json file
  with open(PATH + 'public/data.json') as f:
    data = json.load(f)

  # Get time/date
  # timestamp = time.strftime('%x %X %Z')
  timestamp = int(round(time.time() * 1000))

  # Append to the temp json object
  data.update({timestamp : average})

  # Write changes to the file
  with open(PATH + 'public/data.json', 'w') as f:
    json.dump(data, f, sort_keys=True, indent=2)

  # Turn off voltage pin for 30 minutes to prevent wear
  sensor_pin.write(0)
  time.sleep(1800)
