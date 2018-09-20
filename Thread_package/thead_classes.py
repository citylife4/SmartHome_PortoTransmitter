import logging
import threading

from Arduino import arduino_connection
from Socket import socket_connection
from gpio_funcs import gpio_func


class ReceiveThread(threading.Thread):
    def __init__(self, threadID, name, condition, connected):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.condition = condition
        self.connected = connected

    def run(self):
        logging.info("Thread Function - Starting " + self.name)
        socket_connection.waiter_receive_socket(self.condition, self.connected, self.name)
        logging.info("Thread Function - Exiting " + self.name)


class SendThread(threading.Thread):
    def __init__(self, threadID, name, condition, connected):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.condition = condition
        self.connected = connected

    def run(self):
        pass
        #logging.info("Thread Function - Starting " + self.name)
        #socket_connection.send_socket(self.condition, self.connected, self.name)
        #logging.info("Thread Function - Exiting " + self.name)


class HelperThread(threading.Thread):
    def __init__(self, threadID, name, condition, connected):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.condition = condition
        self.connected = connected

    def run(self):
        pass
        logging.info("Thread Function - Starting " + self.name)
        socket_connection.application_socket_connection(self.condition, self.connected, self.name)
        logging.info("Thread Function -Exiting " + self.name)


class Arduino_thead(threading.Thread):
    def __init__(self, threadID, name, condition, connected):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.condition = condition
        self.connected = connected

    def run(self):
        pass
        logging.info("Thread Function - Starting " + self.name)
        arduino_connection.application_arduino_checker(self.condition, self.connected, self.name)
        logging.info("Thread Function -Exiting " + self.name)


class Porto_Door_thead(threading.Thread):
    def __init__(self, threadID, name, condition, connected):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.condition = condition
        self.connected = connected

    def run(self):
        pass
        logging.info("Thread Function - Starting " + self.name)
        gpio_func.Porto_door_checker()
        logging.info("Thread Function -Exiting " + self.name)