#!/usr/bin/python3

# Ramon Persaud
# 10 sep 2022
# My attempt at an access control system.

import logging
import os
import subprocess
import time
import mysql.connector
import RPi.GPIO as GPIO
import keyboard
import select
import tkinter as tk
from tkinter import ttk
from adafruit_pn532.spi import PN532_SPI
from digitalio import DigitalInOut
from sh import tail
from PIL import ImageTk, Image
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from crontab import CronTab


# Set up logging to accessc.log
logging.basicConfig(
    filename="accessc.log",
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


# Create a class for the GUI
class AccessControlGUI:
    def __init__(self, master):
        self.master = master
        master.title("Access Control System")

        # Create menu buttons
        self.add_user_button = Button(
            master,
            text="Add User & Cards",
            command=self.add_user,
            width=20,
            height=2,
        )
        self.delete_user_button = Button(
            master,
            text="Delete User & Card",
            command=self.delete_user,
            width=20,
            height=2,
        )
        self.test_lock_button = Button(
            master,
            text="Test Lock",
            command=self.test_lock,
            width=20,
            height=2,
        )
        self.schedule_button = Button(
            master,
            text="Schedules",
            command=self.schedule,
            width=20,
            height=2,
        )
        self.view_log_button = Button(
            master,
            text="View Live Log",
            command=self.view_log,
            width=20,
            height=2,
        )
        self.emergency_button = Button(
            master,
            text="Emergency",
            command=self.emergency,
            width=20,
            height=2,
        )
        self.view_user_info_button = Button(
            master,
            text="View User Info",
            command=self.view_user_info,
            width=20,
            height=2,
        )
        self.quit_button = Button(
            master,
            text="Quit",
            command=master.quit,
            width=20,
            height=2,
        )

        # Add buttons to layout
        self.add_user_button.grid(row=0, column=0)
        self.delete_user_button.grid(row=0, column=1)
        self.test_lock_button.grid(row=1, column=0)
        self.schedule_button.grid(row=1, column=1)
        self.view_log_button.grid(row=2, column=0)
        self.emergency_button.grid(row=2, column=1)
        self.view_user_info_button.grid(row=3, column=0)
        self.quit_button.grid(row=3, column=1)


# loginto mariadb server
def mariadb(self):
    mydb = mysql.connector.connect(
    host="localhost",
    user="accessc",
    password="abcd",
    database="codedb"
    )
#    mycursor = mydb.cursor()
    return mydb


# Function for adding user and associated card
def add_user(self):
    print("")
    print("")
    mydb = mariadb()
    mycursor = mydb.cursor()
    
    fname = input('Enter First name: ').lower()
    if fname == '':    
        print("Name can not be blank")
        return
    else:
        print(fname)

    lname = input('Enter last name: ').lower()
    if fname == '':    
        print("Name can not be blank")
        time.sleep(1)
    else:
        print(lname)
        
    mycursor.execute(f'SELECT * FROM accessc WHERE first="{fname}" AND last="{lname}"')
    result = mycursor.fetchone()
    print(result)
    if not result:
        print("User's name is unique")
        logging.info(f'{fname, lname} was entered.')
        time.sleep(1)
    else:
        print("User already exists!")
        time.sleep(2)
        os.system('clear')
        user_add()

    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    cs_pin = DigitalInOut(board.D5)
    pn532 = PN532_SPI(spi, cs_pin, debug=False)
    pn532.SAM_configuration()
    print("Waiting for NFC card...")
    time.sleep(1)

    while True:
        time.sleep(1.2)
        uid = pn532.read_passive_target(timeout=0.5)
        if uid is None:
            continue
        else:
            print("Found card with UID:", [hex(i) for i in uid])
            newCard = [hex(i) for i in uid]
            
        now = datetime.now()
        today = now.strftime("%d/%m/%Y %H:%M")

        mydb = mariadb()    
        mycursor = mydb.cursor()

        print("Connected")
        print(newCard)
        print(today)

        mycursor.execute(f'SELECT EXISTS(SELECT * FROM accessc WHERE card = "{newCard}") as OUTPUT')
        myresult = mycursor.fetchone()[0]
        if myresult == 1:
            print("Card has already been issued")
            time.sleep(2)
            os.system("clear")
            return 
        else:
            sql = f'INSERT INTO accessc (first, last, card, creation, access) VALUES ("{fname}", "{lname}", "{newCard}", "{today}", "{today}")'
            mycursor.execute(sql)
            time.sleep(2) 
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        logging.info(f'{fname, lname} and card have been written to database.')
        time.sleep(2)
        os.system('clear')
        return
        
        


def delete_user(self):
        # Implement function
    return
    # Function for toggling relay to manually open/close lock
def test_lock(self):
        # Implement function
    return
    # Function for creating a schedule using cron
    
# Toggling relay to open and close the lock manually
def lock(self):
    logging.info("Lock has been manually triggered.")
    os.system('python3 unlock.py')
    return    
    
    
def schedule(self):
        # Implement function
    return
    # Function for viewing live log
def view_log(self):
        # Implement function
    return
    # Function for emergency lockdown of the lock
def emergency(self):
        # Implement function
    return
    # Function for viewing data in all tables
def view_user_info(self):
    return


def main():
    # Create the main window
    window = tk.Tk()
    window.title("Access Control System")
    window.geometry("400x200")

    # Add a label for the menu
    label_menu = tk.Label(window, text="Choose an option:")
    label_menu.pack(pady=10)

    # Add the menu options
    button_add_user = ttk.Button(window, text="Add User & Cards", command=add_user)
    button_add_user.pack(pady=5)

    button_delete_user = ttk.Button(window, text="Delete User & Card", command=delete_user)
    button_delete_user.pack(pady=5)

    button_test_lock = ttk.Button(window, text="Test Lock", command=test_lock)
    button_test_lock.pack(pady=5)

    button_schedules = ttk.Button(window, text="Schedules", command=schedule)
    button_schedules.pack(pady=5)

    button_view_log = ttk.Button(window, text="View Live Log", command=view_log)
    button_view_log.pack(pady=5)

    button_emergency = ttk.Button(window, text="Emergency", command=emergency)
    button_emergency.pack(pady=5)

    button_view_users = ttk.Button(window, text="View User Info", command=view_user_info)
    button_view_users.pack(pady=5)

    button_quit = ttk.Button(window, text="Quit", command=window.quit)
    button_quit.pack(pady=10)

    # Start the event loop
    window.mainloop()


if __name__ == "__main__":
    main()



