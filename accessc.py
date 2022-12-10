<<<<<<< HEAD
"""My attempt at an access control system."""
=======
#!/usr/bin/python3

# Ram
# 10 sep 2022
# My attempt at an access control system.
>>>>>>> 742df707e8599e1fb998443156cee286c718a1ec


from adafruit_pn532.spi import PN532_SPI
import board
import busio
from crontab import CronTab
from datetime import datetime
from digitalio import DigitalInOut
import logging
import mysql.connector
import os
import os.path
import RPi.GPIO as GPIO
from sh import tail
import sys
import time

logfile = "accessc.log"
os.system("clear")
logsize = os.path.getsize(logfile)
print(f"The {logfile} size is {logsize} bytes")
time.sleep(3)
<<<<<<< HEAD
=======


>>>>>>> 742df707e8599e1fb998443156cee286c718a1ec
logging.basicConfig(
    filename=logfile,
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="!B7!v0??",
    database="codedb",
)
mycursor = mydb.cursor()


def menu():
    """Main menu"""
    print(
        """Choose an option:
    1. Add User & Cards")
    2. Delete User & Card")
    3. Test lock")
    4. Schedules")
    5. View Live Log")
    6. Quit"""
    )


def user_add():
    """Add user and associate a card with then and save to db.csv"""
    first_name = input("Enter First name: ").lower()
    if first_name == "":
        print("Name can not be blank")
        time.sleep(3)
        return
    else:
        print(first_name)
        time.sleep(1)

    last_name = input("Enter last name: ").lower()
    if first_name == "":
        print("Name can not be blank")
        time.sleep(3)
        return
    else:
        print(last_name)
        time.sleep(1)

    logging.info(f"{first_name, last_name} was entered.")
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    cs_pin = DigitalInOut(board.D5)
    pn532 = PN532_SPI(spi, cs_pin, debug=False)
    pn532.SAM_configuration()
    print("Waiting for NFC card...")
    time.sleep(1)

    while True:
        uid = pn532.read_passive_target(timeout=0.5)
        if not uid:
            continue
        else:
            print("Found card with UID:", [hex(i) for i in uid])
            card = [hex(i) for i in uid]
            time.sleep(2)
        now = datetime.now()
        today = now.strftime("%d/%m/%Y %H:%M")

<<<<<<< HEAD
=======
        mydb = mysql.connector.connect(
            host="localhost", user="root", password="!B7!v0??", database="codedb"
        )

        mycursor = mydb.cursor()

>>>>>>> 742df707e8599e1fb998443156cee286c718a1ec
        print("Connected")
        time.sleep(1)
        print(card)
        print(today)
        time.sleep(1)

        try:
            sql = (
                "INSERT INTO accessc (first, last, card, created, active) VALUES "
                + f"('{first_name}', '{last_name}', '{card}', '{today}', '{today}')"
            )
            mycursor.execute(sql)
        except Exception as e:
            print(e)
            logging.info(f"{e}")
            time.sleep(2)
            os.system("clear")
            break
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        logging.info(f"{first_name, last_name} and card have been written to database.")
        time.sleep(2)
        os.system("clear")
        break


<<<<<<< HEAD
def delete_user():
    mycursor.execute("SELECT first, last FROM accessc")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    name = input("To delete a user, enter their first name> ")
    sql = f"DELETE FROM accessc WHERE first = ('{name}')"
    mycursor.execute(sql)
    mydb.commit()
    logging.info(f"{name} has been deleted from database")
    print(f"{mycursor.rowcount} record(s) deleted")
    time.sleep(3)
=======
def delete():
    """delete user and card function"""
    print("Enter users name")
    name = input("> ")
>>>>>>> 742df707e8599e1fb998443156cee286c718a1ec


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
    note = input("Note ex.unlock schedule> ")
    unlock_time = input("Unlock time ex.13:30> ")
    lock_time = input("Lock time ex.9:15> ")
    # take users time input and split it
    unlock_hour, unlock_minute = unlock_time.split(":")
    lock_hour, lock_minute = lock_time.split(":")

    with CronTab(user="accessc") as cron:
        # pulse to unlock
        job = cron.new(command="python3 ~/Documents/pulseulock.py")
        job.set_comment(note)
        job.hour.on(unlock_hour)
        job.minute.on(unlock_minute)
        # pulse to lock
        job = cron.new(command="python3 ~/Documents/pulselock.py")
<<<<<<< HEAD
        job.set_comment(note)
        job.hour.on(lock_hour)
        job.minute.on(lock_minute)
=======
        job.hour.on(Htime)
        job.minute.on(Mtime)
>>>>>>> 742df707e8599e1fb998443156cee286c718a1ec
    cron.write()
    print("Job has been scheduled")
    logging.info(f"{unlock_time, lock_time} unlock/lock schedule set.")
    time.sleep(3)


def log():
    """Logging function that shows a live view logs to accessc.log. It uses ctrl+c to
    exit the live view."""
    try:
        while True:
            for line in tail("-f", logfile, _iter=True):
                print(line)
    except KeyboardInterrupt:
        os.system("clear")
        return


def main():
    """Main loop to choose an option like adf user and card, view live logs..."""
    while True:
        os.system("clear")
<<<<<<< HEAD
        menu()
        number = input(">  ")
        if number == "1":
            time.sleep(2)
            os.system("clear")
            user_add()
            os.system("clear")
        if number == "2":
            print("You choose to delete a user and card")
            time.sleep(2)
            os.system("clear")
            delete_user()
        if number == "3":
            print("Test lock")
            time.sleep(2)
            os.system("clear")
            lock()
        if number == "4":
            print("schedule")
            time.sleep(2)
            os.system("clear")
            schedule()
        if number == "5":
            print("View live log")
            print("Ctl+c will exit live log")
            time.sleep(4)
            os.system("clear")
            log()
        if number == "6":
            print("Exiting")
            time.sleep(2)
            os.system("clear")
            sys.exit(0)
        print("Choose a correct number.")
        time.sleep(2)
        os.system("clear")


if __name__ == "__main__":
    main()
=======
        user_add()
        os.system("clear")
    if number == "2":
        print("You choose to delete a user and card")
        time.sleep(2)
        os.system("clear")
    if number == "3":
        print("Test lock")
        time.sleep(2)
        os.system("clear")
        lock()
    if number == "4":
        print("schedule")
        time.sleep(2)
        os.system("clear")
        schedule()
    if number == "5":
        print("View live log")
        print("Ctl+c will exit live log")
        time.sleep(4)
        os.system("clear")
        log()
    if number == "6":
        print("Exiting")
        time.sleep(2)
        os.system("clear")
        sys.exit(0)
    print("Choose a correct number.")
    time.sleep(2)
    os.system("clear")
>>>>>>> 742df707e8599e1fb998443156cee286c718a1ec
