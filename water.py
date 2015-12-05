#!/usr/bin/env python

from time import sleep  # Allows us to call the sleep function to slow down our loop
import RPi.GPIO as GPIO # Allows us to call our GPIO pins and names it just GPIO
import time
import signal
import sys
import auth
import twitter

GPIO.setmode(GPIO.BCM)  # Set's GPIO pins to BCM GPIO numbering
INPUT_PIN = 23          # Sets our input pin, in this case 23
GPIO.setup(INPUT_PIN, GPIO.IN)  # Set our input pin to be an input

OUTPUT_PIN = 24         # Set the hygrometer to a GPIO (keep it off most of the time)
GPIO.setup(24, GPIO.OUT)

twitter_api = twitter.Api(consumer_key=auth.consumer_key,
                  consumer_secret=auth.consumer_secret,
                  access_token_key=auth.access_token_key,
                  access_token_secret=auth.access_token_secret)

lastMessage = 0        # last time (in secs since epoch) that a notification was sent

# Gracefully quit on Ctrl-C and reset GPIO
def signal_handler(signal, frame):
  print(' Ctrl+C pressed, closing WaterPi')
  GPIO.cleanup()
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Create a function to run when the input is high
def inputLow(channel):
  global lastMessage
  global twitter_api
#  if (time.time() - lastMessage > 86400):
  if (time.time() - lastMessage > 3):
    lastMessage = time.time()
    #twitter_api.PostUpdate("Looks like I am pretty thirsty right now @amcolash should feed me soon :)")

# Wait for the input to go high (no water), run the function when it does
GPIO.add_event_detect(INPUT_PIN, GPIO.RISING, callback=inputLow, bouncetime=200)

# Start a loop that never ends
while True:
  # Turn on voltage for the hygrometer for 5 seconds to check if there is any water
  GPIO.output(24, True)
  sleep(5);

  # Turn off voltage pin for 60 minutes to prevent wear
  # GPIO.output(24, False)
  # sleep(3600)
