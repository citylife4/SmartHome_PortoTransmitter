#!flask/bin/python

import logging
import datetime
import os
import sqlite3
import socket
import sys
import threading
from Socket import socket_connection
import RPi.GPIO as GPIO           # import RPi.GPIO module

sqlite_file = '/home/jdv/Project/SmartHome_Webserver/homedash/Database/database.db'

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

basedir = os.path.abspath(os.path.dirname(__file__))


class ReceiveThread(threading.Thread):
    def __init__(self, threadID, name, condition, connected):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.condition = condition
        self.connected = connected

    def run(self):
        logging.info("Thread Function - Starting " + self.name)
        socket_connection.waiter_receive_socket(self.condition, self.connected, self.name)
        logging.info("Thread Function - Exiting " + self.name)


class SendThread(threading.Thread):
    def __init__(self, threadID, name, condition, connected):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.condition = condition
        self.connected = connected

    def run(self):
        pass
        #logging.info("Thread Function - Starting " + self.name)
        #socket_connection.send_socket(self.condition, self.connected, self.name)
        #logging.info("Thread Function - Exiting " + self.name)


class HelperThread(threading.Thread):
    def __init__(self, threadID, name, condition, connected):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.condition = condition
        self.connected = connected

    def run(self):
        pass
        logging.info("Thread Function - Starting " + self.name)
        socket_connection.application_socket_connection(self.condition, self.connected, self.name)
        logging.info("Thread Function -Exiting " + self.name)


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
    sender_thread = SendThread(2, "Thread-send", condition, connected)
    helper_thread = HelperThread(3, "Thread-send", condition, connected)

    # Start new Threads
    logging.info("Main - Receiving Thread")
    receiver_thread.start()
    logging.info("Main - Sending Thread")
    sender_thread.start()
    logging.info("Main - Helper Thread")
    helper_thread.start()

if __name__ == "__main__":
    main()
