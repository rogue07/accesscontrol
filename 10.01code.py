#!/usr/bin/python3

#Ram
#rogue7.ram@gmail.com
#My attempt at an access co trol system.


import logging
import os 
import time
import sys
import csv
import board
import busio
import glob
import pandas as pd
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI


#Logs
import logging

#logging.basicConfig(filename='code.log', filemode='a+', level=logging.INFO format='%(name)s - %(levelname)s - %(message)s')
logging.basicConfig(filename='code.log', level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')
#logging.info("Logging test...")
#logging.info("The program is working as expected")
#logging.warning("The program may not function properly")
#logging.error("The program encountered an error")
#logging.critical("The program crashed")


#Global variables

#name = input('Enter user: \n')

#Main menu
def menu():
    print("     Choose an option: ")
    print("     1. Add User & Cards")
    print("     2. Delete User & Card")
    print("     3. View Live Log")
    print("     4. Quit")


#Add user and associate card with that user
#Variables spi, cs_pin and p352 need to be there.
def user_add():
#    print("Enter user")
#    name = input(">  ")
    name = input('Enter user: \n')
    print(name)
    with open(r'db.csv', 'r') as file:
        content = file.read()
        if name in content:
            print(name,'exists')
            time.sleep(5)
            os.system('clear')
            user_add()
        else:
            print(name, 'does not exist')
            time.sleep(5)
#def card_add():
            spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
            cs_pin = DigitalInOut(board.D5)
            pn532 = PN532_SPI(spi, cs_pin, debug=False)
            pn532.SAM_configuration()
            print("Waiting for NFC card...")
      
            while True:
                uid = pn532.read_passive_target(timeout=0.5)
                print(".", end="")
                if uid is None:
                    continue
#|        logging.info(f"Found card with UID:,", [hex(i) for i in uid])
                card = [hex(i) for i in uid]
                with open(r'db.csv', 'r') as file:
                    content = file.read()
                    if ('card') in content:
                        print('string exist')
                        time.sleep(5)
                    else:
                        print('string does not exist')
                        time.sleep(5)

                        data = [name, card]
                        with open('db.csv', 'a+', encoding='UTF8') as f:
#            writer.writerow(header)
                            writer = csv.writer(f, delimiter =',')
                            writer.writerow(data)
 #           logging.info('Saved to database.')
                        break





def delete():
    print("Enter users name")
    name = input("> ")




# Main loop/
while True:
    menu()
    number = input(">  ")
#    logging.info('%s In the menu the admin choose', number)

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
        print("View live log")
        time.sleep(2)
        os.system('clear')
    elif number == "4":
        print("Exiting")
        time.sleep(2)
        os.system('clear')
#        logging.info('Exit was choosen, goodbye')
        quit()
 #   elif number == ".+":
#        print("Choose a correct number.")
#        time.sleep(2)
#        os.system('clear')
