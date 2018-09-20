
import socket
import time
import logging
from sqlite3 import DatabaseError
from time import sleep
import db_interaction as db
from run import ser

connected = False

LOCALHOST = "127.0.0.1"
INTERNAL_PORT = 54897

# This is the address we setup in the Arduino Program
# Slave Address 1
address = 0x04


class TCPsocket:

    def __init__(self, sock=None, server_address=None):
        if socket is None:
            self.sock = socket.socket(
                socket.AF_INET
                , socket.SOCK_STREAM
            )
            self.sock.setsockopt(
                socket.SOL_SOCKET
                , socket.SO_REUSEADDR
                , 1
            )
            self.bind(server_address)
        else:
            self.sock = sock

    def __del__(self):
        self.sock.close()

    def bind(self, server_address):
        self.sock.bind(server_address)
        self.sock.listen(1)

    def connection(self):
        connection , client_address = self.sock.accept()
        try:
            data = connection.recv(1024).decode()
        finally:
            connection.close()

    def protocol(self, data):
        return {
            'IP' : 'x',
        }.get(data, 'problem')


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
        else:
            while not connected:
                time.sleep(10)
                print("Waiting for connection")


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

        i = "a"
        a = "~zwxc"
        b = "c"


        packet = "1".encode()
        ser.write(packet)
        sleep(1)