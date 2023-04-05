
#!/usr/bin/python3

#Ramon Persaud
#10 sep 2022
#My attempt at an access control system.

import pdb
import logging
import os 
import os.path
import time
import sys
import board
import busio
import subprocess
import select
import keyboard
import mysql.connector
import RPi.GPIO as GPIO
import sys
import tkinter as tk
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QAction, QGridLayout, QLabel
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI
from sh import tail
from datetime import datetime
from crontab import CronTab



class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # set window title and size
        self.setWindowTitle('Access Control')
        self.setFixedSize(400, 300)

        # create central widget
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        # create grid layout
        layout = QGridLayout()
        centralWidget.setLayout(layout)

        # create menu bar
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('File')

        # create menu actions
        add_user_action = QAction('Add User & Cards', self)
        add_user_action.triggered.connect(self.add_user)

        delete_user_action = QAction('Delete User & Card', self)
        delete_user_action.triggered.connect(self.delete_user)

        test_lock_action = QAction('Test Lock', self)
        test_lock_action.triggered.connect(self.test_lock)

        schedules_action = QAction('Schedules', self)
        schedules_action.triggered.connect(self.schedules)

        view_log_action = QAction('View Live Log', self)
        view_log_action.triggered.connect(self.view_log)

        emergency_action = QAction('Emergency', self)
        emergency_action.triggered.connect(self.emergency)

        view_user_action = QAction('View User Info', self)
        view_user_action.triggered.connect(self.view_user)

        quit_action = QAction('Quit', self)
        quit_action.triggered.connect(self.quit)

        # add actions to file menu
        fileMenu.addAction(add_user_action)
        fileMenu.addAction(delete_user_action)
        fileMenu.addAction(test_lock_action)
        fileMenu.addAction(schedules_action)
        fileMenu.addAction(view_log_action)
        fileMenu.addAction(emergency_action)
        fileMenu.addAction(view_user_action)
        fileMenu.addAction(quit_action)

        # create buttons
        add_user_btn = QPushButton('Add User & Cards', self)
        add_user_btn.clicked.connect(self.add_user)

        delete_user_btn = QPushButton('Delete User & Card', self)
        delete_user_btn.clicked.connect(self.delete_user)

        test_lock_btn = QPushButton('Test Lock', self)
        test_lock_btn.clicked.connect(self.test_lock)

        schedules_btn = QPushButton('Schedules', self)
        schedules_btn.clicked.connect(self.schedules)

        view_log_btn = QPushButton('View Live Log', self)
        view_log_btn.clicked.connect(self.view_log)

        emergency_btn = QPushButton('Emergency', self)
        emergency_btn.clicked.connect(self.emergency)

        view_user_btn = QPushButton('View User Info', self)
        view_user_btn.clicked.connect(self.view_user)

        quit_btn = QPushButton('Quit', self)
        quit_btn.clicked.connect(self.quit)

        # add buttons to layout
        layout.addWidget(add_user_btn, 0, 0)
        layout.addWidget(delete_user_btn, 0, 1)
        layout.addWidget(test_lock_btn, 1, 0)
        layout.addWidget(schedules_btn, 1, 1)
        layout.addWidget(view_log_btn, 2, 0)
        layout.addWidget(emergency_btn, 2, 1)
        layout.addWidget(view_user_btn, 3, 0)
        layout.addWidget(quit_btn, 3, 1)

# define methods for menu actions
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
        pass




    def delete_user(self):
        pass

    def test_lock(self):
        pass

    def schedules(self):
        pass

   


# import your functions here

# create main window
root = tk.Tk()
root.title("Access Control System")

# create a label
label = tk.Label(root, text="Choose an option:")
label.pack()

# create buttons for each menu option
button1 = tk.Button(root, text="Add User & Cards", command=user_add)
button1.pack()

button2 = tk.Button(root, text="Delete User & Card", command=delete)
button2.pack()

button3 = tk.Button(root, text="Test lock", command=lock)
button3.pack()

button4 = tk.Button(root, text="Schedules", command=schedule)
button4.pack()

button5 = tk.Button(root, text="View Live Log", command=log)
button5.pack()

button6 = tk.Button(root, text="Emergency", command=emergency)
button6.pack()

button7 = tk.Button(root, text="View User Info", command=viewUsers)
button7.pack()

button8 = tk.Button(root, text="Quit", command=root.quit)
button8.pack()

# start the main event loop
root.mainloop()

