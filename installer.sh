#!/bin/bash

# Install all necessary packages & python libraries for access control
sudo apt update -y; sudo apt upgrade
sudo apt install mariadb-server \
    python3-pip \
    unixodbc-dev
pip3 install adafruit-circuitpython-pn532 \
    mysql-connector-python \
    python-crontab \
    mariadb \
    sh
pip3 install --upgrade adafruit-python-shell \
    setuptools