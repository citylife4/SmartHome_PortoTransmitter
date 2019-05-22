import logging

import RPi.GPIO as GPIO
import time
import sys

from db_interaction import insert_porto_door


def Porto_door_checker():
    # Set Broadcom mode so we can address GPIO pins by number.
    GPIO.setmode(GPIO.BCM)

    # This is the GPIO pin number we have one of the door sensor
    # wires attached to, the other should be attached to a ground pin
    DOOR_SENSOR_PIN = 18

    # Initially we don't know if the door sensor is open or closed...
    isOpen = None
    oldIsOpen = None

    # Clean up when the user exits with keyboard interrupt
    def cleanupLights(signal, frame):
        GPIO.cleanup()
        sys.exit(0)

    # Set up the door sensor pin.
    GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    try:
        while True:
            oldIsOpen = isOpen
            isOpen = GPIO.input(DOOR_SENSOR_PIN)

            if isOpen and (isOpen != oldIsOpen):
                logging.info("Porto_door_checker - Door was opened")
                insert_porto_door('door_open')

            elif isOpen != oldIsOpen:
                logging.info("Porto_door_checker - Door was closed!")

            time.sleep(0.1)

    except KeyboardInterrupt:
        # here you put any code you want to run before the program
        # exits when you press CTRL+C
        print("\n")  # print value of counter

    except:
        # this catches ALL other exceptions including errors.
        # You won't get any error messages for debugging
        # so only use it once your code is working
        logging.error("Other error or exception occurred!")

    finally:
        GPIO.cleanup()  # this ensures a clean exit
