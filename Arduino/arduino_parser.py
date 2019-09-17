import logging
import struct
import time
from db_interaction import insert_porto_door

SERVER_QUEUE = []
CLIENT_QUEUE = []


# For now Porto arduino is kinda simple
def h_noop(data):
    return data


def h_door_belt(data):
    insert_porto_door("door_open")
    return data


def h_remote_belt(data):
    insert_porto_door("opening_remotaly")
    return data


handlers = {
    "manualy": h_door_belt,
    "1_0_1_21_1": h_remote_belt
}


def arduino_parser(data):
    logging.info("arduino_parser - received:" + data)
    data_list = list(filter(None, data.strip().split('_')))
    if data_list[1] == '0':
        if data_list[3] == '2' and data_list[4] == '1':
            insert_porto_door("opening_remotaly")
        if data_list[3] == '4' and data_list[4] == '1':
            insert_porto_door("door_open")