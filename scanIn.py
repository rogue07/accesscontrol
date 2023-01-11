import os
import mysql.connector
import logging
import board
import busio
import time
from digitalio import DigitalInOut
from datetime import datetime
from adafruit_pn532.spi import PN532_SPI


now = datetime.now()
today = now.strftime("%d/%m/%Y %H:%M")
   
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="!B7!v0??",
    database="codedb"
    )
mycursor = mydb.cursor()



spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=False)

pn532.SAM_configuration()
print("Waiting for NFC card...")

while True:
    uid = pn532.read_passive_target(timeout=0.5)
    if uid is None:
        continue
    print("Found card with UID:", [hex(i) for i in uid])
    usercard = [hex(i) for i in uid]
    
    mycursor.execute(f'SELECT EXISTS(SELECT * FROM accessc WHERE card = "{usercard}") as OUTPUT')
    myresult = mycursor.fetchone()
    print(myresult)
    time.sleep(5)
    if myresult == (1,):
        print("Card/User accepted")
        time.sleep(5)
    else:
        print("Failed access")
        time.sleep(5)
