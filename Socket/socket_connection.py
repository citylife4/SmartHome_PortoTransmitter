
import socket
import os
import subprocess
import re
import time
import logging
import smbus

from sqlite3 import DatabaseError
import rs485 as RS485
import RPi.GPIO as GPIO           # import RPi.GPIO module
from time import sleep
import serial

import db_interaction as db
import threading

connected = False

LOCALHOST = "127.0.0.1"
INTERNAL_PORT = 54897

# This is the address we setup in the Arduino Program
# Slave Address 1
address = 0x04

# create the connection and check if something is getting through
def waiter_receive_socket(condition, lol, threadName):

    # Bind the socket_connection to the port
    global connected
    connected = False

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('', 4662)
    logging.info('waiter_receive_socket - Starting receiver socket_connection up on %s port %s' % server_address)
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
                logging.warning("IP received %s" % client_address[0])
                connected = False
                ip_file = open("/home/jdv/ip_file.txt", "w")
                ip_file.write(client_address[0])
                ip_file.close()
                connected = True
            elif "status" in data:
                logging.warning("Receiving state %s" % data)
                status = data.split("_")[3]
                if status == "True" or status == "False":
                    conn = db.insert_state(status)
                    if conn is None:
                        raise DatabaseError("Could not get connection")
                else:
                    logging.error("Error not implemented - status missing")

        finally:
            # Clean up the connection.
            logging.info('Cleaning the connection')
            connection.close()

    # For shits and gigles
    sock.close()


def send_socket(condition, lol, threadName):
    global connected

    # time.sleep(random.randrange(2, 5))  # Sleeps for some time.
    logging.info('Aquiring lock')
    # condition.acquire()
    logging.info('Waiting for connection %s' % connected)

    # TODO: check how to make with conditions....
    while not connected:
        time.sleep(10)

    #with condition:
    #    condition.wait_for(connected)

    logging.info('Connected %s' % connected)
    #now check if there is someting to send
    while 1:
        if connected:
            sock_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_send.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Connect the socket_connection to the port where the server is listening
            ip_file = open("ip_file.txt", "r")
            client_address = ip_file.read()
            ip_file.close()

            server_address = (client_address, 45321)
            logging.info('Connecting Raspberry to %s on %s' % server_address)
            sock_send.connect(server_address)
            try:
                message = "open"
                sock_send.sendall(message.encode('utf-8'))
                data_door = sock_send.recv(1024).decode()
                logging.info('Received %s ' % data_door)
            finally:
                sock_send.close()


def application_socket_connection(condition, lol, threadName):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((LOCALHOST, INTERNAL_PORT))
    logging.info('Waiting for internal Aplication')
    while True:
        server.listen(1)
        clientConnection, clientAddress = server.accept()
        print("Connected clinet :", clientAddress)
        data = clientConnection.recv(1024)
        print("From Client :", data.decode())

        #TODO change this

        i = "1"
        bus = smbus.SMBus(1)
        bus.write_word_data(0x04, 0x00, int(i))

        for device in range(128):
            try:
                bus.read_byte(device)
                print(hex(device))
            except:  # exception if read_byte fails
                pass


        '''
        ser = serial.Serial('/dev/ttyAMA0', 19200, timeout=0, rtscts=True)

        rs485 = RS485.SerialWrapper(ser)
        packet = "ola".encode()

        GPIO.setup(18, GPIO.OUT)
        GPIO.output(18, 1)  # set GPIO24 to 1/GPIO.HIGH/True
        sleep(0.5)
        rs485.sendMsg(packet)
        sleep(0.5)
        GPIO.output(18, 0)  # set GPIO24 to 0/GPIO.LOW/False
        GPIO.cleanup(18)

        print("Done")

        timeout = time.time() + 10 # 5 minutes from now
        while True:
            state = ser.readline()
            print(state)

            if rs485.update():
                packet = rs485.getPacket()
                print(len(packet), " bytes received\n".encode())
                print(packet)
                break
            elif time.time() > timeout:
                break

        print("Break")
        '''