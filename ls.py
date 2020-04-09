import threading
import time
import random
import socket
import os
import sys
from threading import Thread
import traceback


def rs():

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 50788
    port = 44444

    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()
    server_binding = ('', port)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    print("[S] Listening on port: ", ss.getsockname()[1])

    while True:
        connection, addr = ss.accept()
        t = 1
        print ("[S]: Got a connection request from a client at {}".format(addr))
        try:
            Thread(target=client_t, args=(
                connection, t)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()
    ss.close()




def client_t(connection, t):
    active = True
    print("[S]: Spawned new client thread")
    while active:
        data = connection.recv(1024).strip()
        # print("[S]: data: " + data)
        if(data == ""):
            # print("data is empty")
            connection.close()
            active = False
            print("[S]: Killed client thread")

        if data:
            print("[S]: Incoming data: " + data)
            #print("[S]: Outgoing data: " + data + "hello")
            try:
                cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("[C]: Client socket created")
            except socket.error as err:
                print('[C]: socket open error: {} \n'.format(err))
                exit()

            host_addr = socket.gethostbyname(socket.gethostname())
            print "[C]: Using localhost"
            server_binding = (host_addr, 22222)
            cs.connect(server_binding)
            cs.sendall(data)
            data_from_server = cs.recv(1024)  # Receive data from the server
            print("[C]: Data received: {}".format(data_from_server.decode('utf-8')))


            connection.sendall(data_from_server)

# If there is a match, sends the entry as a string:
# Hostname IPaddress A
# If there is no match, RS sends the string:
# TSHostname - NS



if __name__ == "__main__":
    t1 = threading.Thread(name='rs', target=rs)
    t1.start()
