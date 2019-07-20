import serial
import time
import logging
from threading import Thread

from Arduino.arduino_parser import arduino_parser

# change this

arduino_ser = serial.Serial('/dev/serial0',
                            baudrate=4800,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS,
                            timeout=1)


class ArduinoThead(Thread):
    def __init__(self):
        super(ArduinoThead, self).__init__()

    def run(self):
        logging.info("Thread Function - Starting " + self.name)
        while 1:
            time.sleep(0.01)
            while arduino_ser.in_waiting:  # Or: while ser.inWaiting():
                read_serial = arduino_ser.readline().decode("utf-8")
                arduino_parser(read_serial)

