import logging
import os
import sys
from datetime import datetime
import pdb

import mysql.connector
import RPi.GPIO as GPIO
import keyboard
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)


# Log to accessc.log
logging.basicConfig(
    filename="accessc.log",
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

# loginto mariadb server
def mariadb():
    mydb = mysql.connector.connect(
    host="localhost",
    user="accessc",
    password="abcd",
    database="codedb"
    )
#    mycursor = mydb.cursor()
    return mydb
    
    
class AddUserWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fname_label = QLabel("First name:")
        self.fname_edit = QLineEdit()
        self.lname_label = QLabel("Last name:")
        self.lname_edit = QLineEdit()
        self.submit_button = QPushButton("Add user")

        layout = QVBoxLayout()
        layout.addWidget(self.fname_label)
        layout.addWidget(self.fname_edit)
        layout.addWidget(self.lname_label)
        layout.addWidget(self.lname_edit)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Access Control")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.menu_label = QLabel("Choose an option:")
        self.user_add_button = QPushButton("Add User & cards")

        layout = QVBoxLayout()
        layout.addWidget(self.menu_label)
        layout.addWidget(self.user_add_button)
        self.central_widget.setLayout(layout)

        self.user_add_button.clicked.connect(self.on_user_add_clicked)

    def on_user_add_clicked(self):
        add_user_widget = AddUserWidget(self)
        add_user_widget.submit_button.clicked.connect(self.on_add_user_submit_clicked)
        self.setCentralWidget(add_user_widget)

    def on_add_user_submit_clicked(self):
        fname = self.centralWidget().fname_edit.text().lower()
        lname = self.centralWidget().lname_edit.text().lower()

        if fname == "" or lname == "":
            return

        mydb = mariadb()
        mycursor = mydb.cursor()

        mycursor.execute(f'SELECT * FROM accessc WHERE first="{fname}" AND last="{lname}"')
        result = mycursor.fetchone()
        if not result:
            mycursor.execute(f'INSERT INTO accessc (first, last) VALUES ("{fname}", "{lname}")')
            mydb.commit()
            logging.info(f"{fname}, {lname} was entered.")
            self.setCentralWidget(self.central_widget)
        else:
            self.fname_edit.clear()
            self.lname_edit.clear()
            self.fname_edit.setFocus(Qt.OtherFocusReason)
            self.lname_edit.setFocus(Qt.OtherFocusReason)






def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

