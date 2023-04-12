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
from tkinter import messagebox
from crontab import CronTab
import logging


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
        
        # Add buttons to layout
        self.add_user_button.grid(row=0, column=0)
        

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
        return

    # Check if user already exists
    mydb = mariadb()
    mycursor = mydb.cursor()
    mycursor.execute(f'SELECT * FROM accessc WHERE first="{fname}" AND last="{lname}"')
    result = mycursor.fetchone()


    if not result:
        logging.info(f'{fname}, {lname} was entered.')
        time.sleep(1)
        os.system('clear')
        add_user(master)
    else:
        messagebox.showerror("Error", "User already exists!")
        time.sleep(2)
        os.system('clear')
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
                add_user(master)
        else:
                print("User already exists!")
                time.sleep(2)
                os.system('clear')
                add_user(master)
         
         
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
    
    # Start the event loop
    window.mainloop()


if __name__ == "__main__":
    main()             

