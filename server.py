from socket import *
import socket
import threading
import logging
import time
import sys
import pytz
from datetime import datetime

class ProcessTheClient(threading.Thread):
        def __init__(self,connection,address):
                self.connection = connection
                self.address = address
                threading.Thread.__init__(self)

        def run(self):
                while True:
                        data = self.connection.recv(32)
                        if data and data.startswith(b"TIME") and data.endswith(b"\r\n"):
                                response = f"JAM {datetime.now(pytz.timezone('Asia/Jakarta')).strftime('%H:%M:%S')}\r\n".encode('utf-8')
                                logging.warning(f"[SERVER] sending {response} to {self.address}")
                                self.connection.sendall(response)
                        else:
                                self.connection.close()
                                break
                self.connection.close()

class Server(threading.Thread):
        def __init__(self):
                self.the_clients = []
                self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                threading.Thread.__init__(self)

        def run(self):
                self.my_socket.bind(('0.0.0.0', 45000))
                self.my_socket.listen(1)
                while True:
                        self.connection, self.client_address = self.my_socket.accept()
                        logging.warning(f"connection from {self.client_address}")
                        clt = ProcessTheClient(self.connection, self.client_address)
                        clt.start()
                        self.the_clients.append(clt)

def main():
        svr = Server()
        svr.start()

if __name__=="__main__":
        main()
