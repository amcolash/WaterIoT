from __future__ import division
import spidev
import time
import RPi.GPIO as GPIO
import signal
import sys

# Define "enable" for the sensor
SENSOR_PIN = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.OUT)

# Set up ctrl-c handler
# Gracefully quit on Ctrl-C and reset GPIO
def signal_handler(signal, frame):
  print(' Ctrl+C pressed, closing WaterPi')
  GPIO.output(SENSOR_PIN, GPIO.LOW)
  GPIO.cleanup()
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Set up SPI connection
def bitstring(n):
  s = bin(n)[2:]
  return '0'*(8-len(s)) + s

def read(adc_channel=0, spi_channel=0):
  conn = spidev.SpiDev(0, spi_channel)
  conn.max_speed_hz = 1200000 # 1.2 MHz
  cmd = 128
  if adc_channel:
    cmd += 32
  reply_bytes = conn.xfer2([cmd, 0])
  reply_bitstring = ''.join(bitstring(n) for n in reply_bytes)
  reply = reply_bitstring[5:15]
  return int(reply, 2) / 2**10

# Turn on the sensor
GPIO.output(SENSOR_PIN, GPIO.HIGH)

while True:
    print read()
    time.sleep(0.1)
