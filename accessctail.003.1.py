import os
import subprocess
import time
#from pythontail import tail
#from pathlib import Path

def button1():
    os.system('clear')
    print("Hello World")
    time.sleep(2)
    main()

def button2():
    os.system('clear') 
    print("yo yo")
    time.sleep(2)
    main()

def main():
    number = None
    while number != "3":
        os.system('clear')
        print("")
        print("1. Button1")
        print("2. Button2")
        print("3. Exit")
        print("")
        print("Access Log:")
        subprocess.run("tail -n4 accessc.log", shell=True)
        time.sleep(1)
        number = input("> ")
        os.system('clear')
        if number == "1":
            button1()
        elif number == "2":
            button2()
        elif number != "3":
            os.system('clear')
            continue
    exit()

if __name__ == "__main__":
    main()

