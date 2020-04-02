import threading
import time
import random
import sys
import socket


def client():

    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('[C]: socket open error: {} \n'.format(err))
        exit()

    if hostname == "local":
        host_addr = socket.gethostbyname(socket.gethostname())
        print "[C]: Using localhost"
    else:
        host_addr = socket.gethostbyname(hostname)

    server_binding = (host_addr, 55555)
    cs.connect(server_binding)
    query = sys.argv[1]
    cs.sendall(query)
    data_from_server = cs.recv(1024)  # Receive data from the server
    print("[C]: Data received: {}".format(data_from_server.decode('utf-8')))
