import struct
import time
from db_interaction import insert_porto_door

SERVER_QUEUE = []
CLIENT_QUEUE = []

# For now Porto arduino is kinda simple
#def h_noop(data):
#    return data
#
#def h_door_belt(data):
#    insert_porto_door(1)
#    return data
#
#def h_remote_belt(data):
#    insert_porto_door(0)
#    return data
#
#handlers = {
#    "manualy"  : h_door_belt,
#    "remotaly" : h_remote_belt
#}



def arduino_parser(data):
    if "opening" in data:
        insert_porto_door(data)
    print(data)

