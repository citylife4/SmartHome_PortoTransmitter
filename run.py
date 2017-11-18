#!flask/bin/python

import logging
import datetime
import os
import sqlite3
import socket
import sys
import threading
from Socket import socket_connection

sqlite_file = '/home/jdv/Project/SmartHome_Webserver/database.db'

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
        logging.info("Starting " + self.name)
        socket_connection.waiter_receive_socket(self.condition, self.connected, self.name)
        logging.info("Exiting " + self.name)


class SendThread(threading.Thread):
    def __init__(self, threadID, name, condition, connected):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.condition = condition
        self.connected = connected

    def run(self):
        logging.info("Starting " + self.name)
        socket_connection.send_socket(self.condition, self.connected, self.name)
        logging.info("Exiting " + self.name)


def configuration():
    now = datetime.datetime.now()
    logging.basicConfig(level=logging.DEBUG, filename="/home/jdv/logfiles/logfile_" + now.strftime("%Y_%m_%d") + ".log",
                        filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(threadName)-9s) %(message)s")
    stderrLogger = logging.StreamHandler()
    stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
    logging.getLogger().addHandler(stderrLogger)
    logging.getLogger().addHandler(logging.StreamHandler())

    ip_file = open("/home/jdv/ip_name.bin", "r+")


def main():
    configuration()
    logging.info("Starting Server")
    condition = threading.Condition()
    connected = False

    thread1 = ReceiveThread(1, "Thread-rec", condition, connected)
    thread2 = SendThread(2, "Thread-send", condition, connected)

    # Start new Threads
    logging.info("Receiving Thread")
    thread1.start()
    logging.info("Sending Thread")
    thread2.start()


if __name__ == "__main__":
    main()
