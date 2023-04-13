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
            command=self.create_add_user_window,
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
        self.delete_button.grid(row=0, column=1)

    def create_add_user_window(self):
        self.add_user_window = tk.Toplevel(self.master)
        self.add_user_window.title("Add User")
        label = tk.Label(self.add_user_window, text="Enter user's first and last name:")
        label.pack(padx=10, pady=10)
        self.entry1 = tk.Entry(self.add_user_window, width=30)
        self.entry1.pack(padx=10, pady=5)
        self.entry2 = tk.Entry(self.add_user_window, width=30)
        self.entry2.pack(padx=10, pady=5)
        button = tk.Button(self.add_user_window, text="Enter", command=self.get_input)
        button.pack(padx=10, pady=5)

    def get_input(self):
        fname = self.entry1.get().lower()
        lname = self.entry2.get().lower()

        if fname == '' or lname == '':
            messagebox.showerror("Error", "Name cannot be blank.")
            self.add_user_window.destroy()
            self.create_add_user_window()

        # Check if user already exists
        mydb = mariadb()
        mycursor = mydb.cursor()
        mycursor.execute(f'SELECT * FROM accessc WHERE first="{fname}" AND last="{lname}"')
        result = mycursor.fetchone()

        if not result:
            logging.info(f'{fname}, {lname} was entered.')
            time.sleep(1)
            os.system('clear')
            self.add_user_window.destroy()
        else:
            messagebox.showerror("Error", "User already exists!")
            time.sleep(2)
            os.system('clear')
            self.add_user_window.destroy()
            self.create_add_user_window()

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



def delete(master):
    # Fetch all user names from database
    mydb = mariadb()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT first, last FROM accessc")
    user_list = mycursor.fetchall()

    # Display user list in a message box
    user_names = '\n'.join([f"{fname.capitalize()} {lname.capitalize()}" for fname, lname in user_list])
    messagebox.showinfo("User List", f"Select the user to delete:\n\n{user_names}")

    # Prompt the user to enter the name of the user to be deleted
    dialog = tk.Toplevel(master)
    dialog.title("Delete User")
    label = tk.Label(dialog, text="Enter the user's first and last name:")
    label.pack(padx=10, pady=10)
    entry1 = tk.Entry(dialog, width=30)
    entry1.pack(padx=10, pady=5)
    entry2 = tk.Entry(dialog, width=30)
    entry2.pack(padx=10, pady=5)
    button = tk.Button(dialog, text="Enter", command=lambda: delete_user(dialog, entry1, entry2, master))
    button.pack(padx=10, pady=5)

def delete_user(dialog, entry1, entry2, master):
    fname = entry1.get().lower()
    lname = entry2.get().lower()

    if fname == '' or lname == '':
        messagebox.showerror("Error", "Name cannot be blank.")
        dialog.destroy()
        delete()

    # Check if user exists
    mydb = mariadb()
    mycursor = mydb.cursor()
    mycursor.execute(f'SELECT * FROM accessc WHERE first="{fname}" AND last="{lname}"')
    result = mycursor.fetchone()

    if not result:
        messagebox.showerror("Error", "User does not exist!")
        time.sleep(2)
        os.system('clear')
        dialog.destroy()
        delete(master)
    else:
        # Prompt user to confirm deletion
        message = f"Are you sure you want to delete {fname.capitalize()} {lname.capitalize()}?"
        confirmed = messagebox.askyesno("Confirm Deletion", message)

        if confirmed:
            # Delete user from database
            mycursor.execute(f'DELETE FROM accessc WHERE first="{fname}" AND last="{lname}"')
            mydb.commit()
            logging.info(f'{fname.capitalize()}, {lname.capitalize()} has been deleted from the database.')
            messagebox.showinfo("Success", f"{fname.capitalize()} {lname.capitalize()} has been deleted from the database.")
            time.sleep(2)
            os.system('clear')
            dialog.destroy()
        else:
            dialog.destroy()
            delete(master)






       

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
 
