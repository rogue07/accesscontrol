import logging
import os
import subprocess
import time
from datetime import datetime

import mysql.connector
import RPi.GPIO as GPIO
import board
import busio
import select
import keyboard
from adafruit_pn532.spi import PN532_SPI
from crontab import CronTab
from digitalio import DigitalInOut
from sh import tail
import tkinter as tk
from tkinter import ttk, messagebox


# Log to accessc.log
logging.basicConfig(filename="accessc.log", format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')


# Create a class for the GUI
class AccessControlGUI:
    def __init__(self, master):
        self.master = master
        master.title("Access Control System")

        # Create menu buttons
        self.add_user_button = tk.Button(
            master,
            text="Add User & Cards",
            command=self.add_user,
            width=20,
            height=2,
        )
        self.delete_button = tk.Button(
            master,
            text="Delete user & card",
            command=self.delete,
            width=20,
            height=2,
        )
        # Add buttons to layout
        self.add_user_button.grid(row=0, column=0)
        self.delete_button.grid(row=0, column=0)

# log into mariadb server
def mariadb():
    mydb = mysql.connector.connect(
        host="localhost",
        user="accessc",
        password="abcd",
        database="codedb"
    )
    return mydb



def add_user(master):
    dialog = tk.Toplevel(master)
    dialog.title("Add User")
    label = tk.Label(dialog, text="Enter user's first and last name:")
    label.pack(padx=10, pady=10)
    entry1 = tk.Entry(dialog, width=30)
    entry1.pack(padx=10, pady=5)
    entry2 = tk.Entry(dialog, width=30)
    entry2.pack(padx=10, pady=5)
    button = tk.Button(dialog, text="Enter", command=lambda: get_input(dialog, entry1, entry2, master))
    button.pack(padx=10, pady=5)

def get_input(dialog, entry1, entry2, master):
    fname = entry1.get().lower()
    lname = entry2.get().lower()

    if fname == '' or lname == '':
        messagebox.showerror("Error", "Name cannot be blank.")
        dialog.destroy()
        add_user()

    # Check if user already exists
    mydb = mariadb()
    mycursor = mydb.cursor()
    mycursor.execute(f'SELECT * FROM accessc WHERE first="{fname}" AND last="{lname}"')
    result = mycursor.fetchone()

    if not result:
        logging.info(f'{fname}, {lname} was entered.')
        time.sleep(1)
        os.system('clear')
        dialog.destroy()
        # add_user(master)
    else:
        messagebox.showerror("Error", "User already exists!")
        time.sleep(2)
        os.system('clear')
        dialog.destroy()
        add_user(master)

    # Check if user already exists
    mycursor.execute(f'SELECT * FROM accessc WHERE first="{fname}" AND last="{lname}"')
    result = mycursor.fetchone()
    print(result)
    if not result:
        print("User's name is unique")
        logging.info(f'{fname}, {lname} was entered.')
        time.sleep(1)
        os.system('clear')
        dialog.destroy()
        add_user(master)
    else:
        print("User already exists!")
        time.sleep(2)
        os.system('clear')
        add_user(master)

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
                add_user()
            else:
                sql = f'INSERT INTO accessc (first, last, card, creation, access) VALUES ("{fname}", "{lname}", "{newCard}", "{today}", "{today}")'
                mycursor.execute(sql)
                time.sleep(2)
                mydb.commit()
                print(mycursor.rowcount, "record inserted.")
                logging.info(f'{fname, lname} and card have been written to database.')
                time.sleep(2)
                os.system('clear')



def delete():
	print("Hello world")
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
    button_add_user = ttk.Button(window, text="Add User & Cards", command=lambda: add_user(window))
    button_add_user.pack(pady=5)
    button_delete = ttk.Button(window, text="Delete User & Cards", command=lambda: 
delete(window))
    button_delete.pack(pady=5)    
    # Start the event loop
    window.mainloop()


if __name__ == "__main__":
    main()             
 
