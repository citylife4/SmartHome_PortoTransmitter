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

    while 1:
        condition.acquire()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_address = ('', 4662)
        logging.info('waiter_receive_socket - Starting receiver socket up on %s port %s' % server_address)
        sock.bind(server_address)
        # Listen for incoming connections
        sock.listen(1)
        connection, client_address = sock.accept()

        try:
            logging.info('waiter_receive_socket - Received connection from ' + client_address[0])
            # Receive the data in small chunks and retransmit it
            data = connection.recv(16)
            logging.info('waiter_receive_socket - Received %s' % data)
            ip_file = open("ip_file.txt", "w")
            ip_file.write(client_address[0])
            ip_file.close()
            condition.notify()
            connected = True
            condition.release()

        finally:
            # Clean up the connection.
            logging.info('waiter_receive_socket - Cleaning the connection')
            connection.close()
            sock.close()
            time.sleep(1000)
            connected = False


def send_socket(condition, lol, threadName):
    global connected

    time.sleep(random.randrange(2, 5))  # Sleeps for some time.
    logging.info('send_socket - aquiring lock')
    # condition.acquire()
    logging.info('send_socket - Waiting for connection %s' % connected)

    with condition:
        while not connected:
            condition.wait()

    logging.info('send_socket - Connected %s' % connected)

    if connected:
        sock_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_send.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Connect the socket to the port where the server is listening
        ip_file = open("ip_file.txt", "r")
        client_address = ip_file.read()
        ip_file.close()

        server_address = (client_address, 45321)
        logging.info('send_socket - Connecting Raspberry to %s on %s' % server_address)
        sock_send.connect(server_address)
        try:
            message = "open"
            sock_send.sendall(message.encode('utf-8'))
            data_door = sock_send.recv(1024)
            logging.info('send_socket - Received %s ' % data_door)
        finally:
            sock_send.close()
