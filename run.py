#!flask/bin/python

import datetime
import os
import sqlite3
import sys


from Thread_package.thead_classes import *
from Arduino import arduino_connection
from webserver_connection.webserver_connection import WebserverConnection

sqlite_file = '/home/jdv/Project/SmartHome_Webserver/app/Database/database.db'

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

basedir = os.path.abspath(os.path.dirname(__file__))


def configuration():
    now = datetime.datetime.now()
    # logging.basicConfig(level=logging.DEBUG, filename="/home/jdv/logfiles/logfile_" + now.strftime("%Y_%m_%d") + ".log",
    #                    filemode="a+",
    #                    format="%(asctime)-15s %(levelname)-8s %(threadName)-9s) %(message)s")

    logging.basicConfig(level=logging.DEBUG)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    ip_file = open("/home/jdv/Project/SmartHome_transmitter/tmp/ip_name.bin", "r+")


class Transmitter:

    def __init__(self):
        configuration()
        logging.info("Main - Starting Server")

        # for RPI version 1, use "bus = smbus.SMBus(0)"

        receiver_thread = ReceiveThread('', 4662)
        sender_thread = SendThread()
        helper_thread = WebserverConnection()
        arduino_thread = arduino_connection.ArduinoThead()

        # Start new Threads
        logging.info("Main - Receiving Thread")
        receiver_thread.start()
        logging.info("Main - Sending Thread")
        sender_thread.start()
        logging.info("Main - WebserverConnection Thread")
        helper_thread.start()
        logging.info("Main - arduino Thread")
        arduino_thread.start()


if __name__ == "__main__":
    transmitter = Transmitter()
