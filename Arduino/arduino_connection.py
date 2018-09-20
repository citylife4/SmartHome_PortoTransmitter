from db_interaction import insert_porto_door
import time
from run import ser


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
