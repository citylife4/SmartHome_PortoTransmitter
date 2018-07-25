#!flask/bin/python

import logging
import datetime
import os
import sqlite3
import socket
import sys
import threading


import RPi.GPIO as GPIO           # import RPi.GPIO module
import smbus

from Thread_package.thead_classes import *
import serial

sqlite_file = '/home/jdv/Project/SmartHome_Webserver/homedash/Database/database.db'

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

basedir = os.path.abspath(os.path.dirname(__file__))

bus = smbus.SMBus(1)

ser = serial.Serial('/dev/ttyAMA0', 4800, timeout=0, rtscts=True)

def configuration():
    now = datetime.datetime.now()
    logging.basicConfig(level=logging.DEBUG, filename="/home/jdv/logfiles/logfile_" + now.strftime("%Y_%m_%d") + ".log",
                        filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(threadName)-9s) %(message)s")

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    ip_file = open("/home/jdv/ip_name.bin", "r+")

    GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD


def main():
    configuration()
    logging.info("Main - Starting Server")
    condition = threading.Condition()
    connected = False

    # for RPI version 1, use "bus = smbus.SMBus(0)"

    receiver_thread = ReceiveThread(1, "Thread-rec", condition, connected)
    sender_thread   = SendThread(2, "Thread-send", condition, connected)
    helper_thread   = HelperThread(3, "Thread-send", condition, connected)
    arduino_thread  = Arduino_thead(4, "Thread-send", condition, connected)
    porto_thread    = Porto_Door_thead(5, "Thread-porto", condition, connected)

    # Start new Threads
    logging.info("Main - Receiving Thread")
    receiver_thread.start()
    logging.info("Main - Sending Thread")
    sender_thread.start()
    logging.info("Main - Helper Thread")
    helper_thread.start()
    logging.info("Main - arduino Thread")
    arduino_thread.start()
    logging.info("Main - Porto Thread")
    porto_thread.start()


if __name__ == "__main__":
    main()
