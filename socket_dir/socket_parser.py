import struct
import logging
from sqlite3 import DatabaseError
import db_interaction as db

from socket_dir.socket_connection import ip_filename


def h_noop(data):
    print("Not Implemented Received: {}".format(data))

def h_update_ip(data):
    print("h_update_ip")
    print(data)
    ip_address = data.pop(0)
    with open(ip_filename, "w") as ip_file:
        ip_file.write(ip_address)

    return '_'.join(data)

def h_update_status(data):
    print("h_update_status")
    print(data)
    distance = data.pop(0)
    status = data.pop(0)
    if status == "True" or status == "False":
        conn = db.insert_state(status)
        if conn is None:
            raise DatabaseError("Could not get connection")
    else:
        logging.error("Error not implemented - status missing")
    return '_'.join(data)

handlers = {
    "ip" : h_update_ip,
    "st" : h_update_status
}

def rasp_parser(data):
    while len(data)>=2:
        packet_id = data[0:2]
        if packet_id not in handlers:
            data = data[1:]
        else:
            data_list = list(filter(None,data[2:].split('_')))
            data = handlers.get(packet_id, h_noop)(data_list)