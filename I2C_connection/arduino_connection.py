import smbus

from db_interaction import insert_porto_door
from run import bus
import time
from run import ser
from I2C_connection.I2C_sniffer import sniffer
import pigpio

SDA=3
SCL=2
I2C_ADDR=9

def i2c(id, tick):
   global pi

   s, b, d = pi.bsc_i2c(I2C_ADDR)

   if b:

      print(d[:-1])


def application_arduino_checker(condition, lol, threadName):
    # Respond to BSC slave activity

    while 1 :
        time.sleep(0.01)
        read = ""
        while ser.in_waiting:  # Or: while ser.inWaiting():
            read = ser.readline().decode('utf-8')
            print(read)
            if "manualy" in read:
                print("man")
                insert_porto_door(1)
            if "remotaly" in read :
                print("re")
                insert_porto_door(0)
