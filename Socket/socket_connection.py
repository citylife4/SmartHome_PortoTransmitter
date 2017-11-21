import fcntl
import struct
import socket
import time
import logging
import random

import threading

connected = False


# create the connection and check if something is getting through
def waiter_receive_socket(condition, lol, threadName):
    # Bind the socket to the port
    global connected
    connected = False

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('', 4662)
    logging.info('waiter_receive_socket - Starting receiver socket up on %s port %s' % server_address)
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(1)
    while 1:
        connection, client_address = sock.accept()
        # condition.acquire()
        try:
            logging.info('Received connection from ' + client_address[0])
            # Receive the data in small chunks and retransmit it
            data = connection.recv(1024).decode()
            logging.info('Received %s' % data)
            if "IP" in data:
                logging.warning("IP received")
                connected = False
                ip_file = open("ip_file.txt", "w")
                ip_file.write(client_address[0])
                ip_file.close()
                connected = True
            elif "status" in data:
                logging.warning("Not Implemented %s" % data)

        finally:
            # Clean up the connection.
            logging.info('Cleaning the connection')
            connection.close()

    # For shits and gigles
    sock.close()