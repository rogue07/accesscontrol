import RPi.GPIO as GPIO
import time
import logging

#logging.basicConfig(filename="accessc.log", level=logging.INFO) 
logging.basicConfig(filename="accessc.log", format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S') 
 

logging.info('Unlocked via schedule')
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.HIGH)
#time.sleep(15)
#GPIO.output(12, GPIO.LOW)
#GPIO.cleanup()
