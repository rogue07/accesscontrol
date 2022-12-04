#!/usr/bin/python3

#Ram
#10 sep 2022
#rogue7.ram@gmail.com
#My attempt at an access control system.


import logging
import os 
import time
import sys
import board
import busio
import subprocess
import select
import keyboard
import mysql.connector
import RPi.GPIO as GPIO
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI
from sh import tail
from datetime import datetime
from crontab import CronTab

import os.path

# file to check
logfile = 'accessc.log'

os.system('clear')
sz = os.path.getsize(logfile)
print(f'The {logfile} size is', sz, 'bytes')
time.sleep(3)


# log to accessc.log
logging.basicConfig(filename="accessc.log", format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')


#logging.basicConfig(filename="accessc.log", level=logging.INFO)

#Main menu
def menu():
    print("     Choose an option: ")
    print("     1. Add User & Cards")
    print("     2. Delete User & Card")
    print("     3. Test lock")
    print("     4. Schedules")
    print("     5. View Live Log")
    print("     6. Quit")


#add user and associate a card with then and save to db.csv
def user_add():
    fname = input('Enter First name: ').lower()
    if fname == '':    
        print("Name can not be blank")
        time.sleep(3)
        return
    else:
        print(fname)
        time.sleep(1)

    lname = input('Enter last name: ').lower()
    if fname == '':    
        print("Name can not be blank")
        time.sleep(3)
        return
    else:
        print(lname)
        time.sleep(1)

    logging.info(f'{fname, lname} was entered.')
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    cs_pin = DigitalInOut(board.D5)
    pn532 = PN532_SPI(spi, cs_pin, debug=False)
    pn532.SAM_configuration()
    print("Waiting for NFC card...")
    time.sleep(1)

    while True:
        uid = pn532.read_passive_target(timeout=0.5)
        if uid is None:
            continue
        else:
            print("Found card with UID:", [hex(i) for i in uid])
            card = [hex(i) for i in uid]
            time.sleep(2)

#        today = date.today()
#        today = datetime.now()
        now = datetime.now()
        today = now.strftime("%d/%m/%Y %H:%M")

        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="!B7!v0??",
        database="codedb"
        )

        mycursor = mydb.cursor()

        print("Connected")
        time.sleep(1)
        print(card)
        print(today)
        time.sleep(1)

        try:
            sql = f'INSERT INTO accessc (first, last, card, created, active) VALUES ("{fname}", "{lname}", "{card}", "{today}", "{today}")'
            mycursor.execute(sql)
        except Exception as e:
            print(e)
            logging.info(f'{e}')
            time.sleep(2)
            os.system('clear')
            break
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        logging.info(f'{fname, lname} and card have been written to database.')
        time.sleep(2)
        os.system('clear')
        break
    
# delete user and card functiin
def delete():
    print("Enter users name")
    name = input("> ")

def lock():
    logging.info("Lock has been manually triggered.")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(12, GPIO.OUT)
    GPIO.output(12, GPIO.HIGH)
    print("Lock is open")
    time.sleep(5)
    os.system("clear")
    GPIO.output(12, GPIO.LOW)
    print("Lock is closed")
    time.sleep(3)
    return


def schedule():
    # whats the frequency kenneth
    utime = input("Unlock time ex.13:30> ")
    ltime = input("Lock time ex.9:15> ")

    #take users time input and split it
    htime,mtime = utime.split(':')
    Htime,Mtime = ltime.split(':')

    with CronTab(user='accessc') as cron:
        # pulse to unlock
        job = cron.new(command='python3 ~/Documents/pulseulock.py')
        job.hour.on(htime)
        job.minute.on(mtime)
        # pulse to lock
        job = cron.new(command='python3 ~/Documents/pulselock.py')
        job.hour.on(Htime)
        job.minute.on(Mtime)
    cron.write()
    print("Job has been scheduled")
    logging.info(f'{utime, ltime} unlock/lock schedule set.')
    time.sleep(3)



#logginn function that shiwe a live view logs to accessc.log. It used ctl+c to exit the live view.
def log():
    try:
        while True:
            for line in tail("-f", "accessc.log", _iter=True):
                print(line)
    except KeyboardInterrupt:
        os.system('clear')
        return


# Main loop to choose an option like adf user and card, view live logs...
while True:
    os.system('clear')
    menu()
    number = input(">  ")
    if number == "1":
        time.sleep(2)
        os.system('clear')
        user_add()
        os.system('clear')
    elif number == "2":
        print("You choose to delete a user and card")
        time.sleep(2)
        os.system('clear')
    elif number == "3":
        print("Test lock")
        time.sleep(2)
        os.system('clear')
        lock()
    elif number == "4":
        print("schedule")
        time.sleep(2)
        os.system('clear')
        schedule()
    elif number == "5":
        print("View live log")
        print("Ctl+c will exit live log")
        time.sleep(4)
        os.system('clear')
        log()
    elif number == "6":
        print("Exiting")
        time.sleep(2)
        os.system('clear')
        quit()
    elif number == "_":
        print("Choose a correct number.")
        time.sleep(2)
        os.system('clear')
