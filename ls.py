import threading
import time
import random
import socket
import os
import sys
from threading import Thread
import traceback


def ls():

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 44444

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

    ts1Hn = sys.argv[2]
    ts1Port = int(sys.argv[3]) if len(sys.argv) > 1 else 22222
    ts2Hn = sys.argv[4]
    ts2Port = int(sys.argv[5]) if len(sys.argv) > 1 else 33333

    active = True
    print("[S]: Spawned new client thread")

    timeout1 = False
    timeout2 = False;


    while active:
        data = connection.recv(1024).strip() #from client
        # print("[S]: data: " + data)
        if(data == ""):
            # print("data is empty")
            connection.close()
            active = False
            print("[S]: Killed client thread")

        if data:
            print("[S]: Incoming data: " + data)
            #print("[S]: Outgoing data: " + data + "hello")

            try: #create ts1 socket
                cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("[C]: Client socket created")
            except socket.error as err:
                print('[C]: socket open error: {} \n'.format(err))
                exit()

            if ts1Hn == "local":
                host_addr = socket.gethostbyname(socket.gethostname())
            else:
                host_addr = socket.gethostbyname(ts1Hn)
            #print "[C]: Using localhost"
            server_binding = (host_addr, ts1Port)
            cs.connect(server_binding)
            cs.sendall(data)
            cs.settimeout(5.0)
            data_from_server_ts1=""

            try:
                data_from_server_ts1 = cs.recv(1024)  # Receive data from the server
                timeout1 = False
                print "recieved from ts1 " + data_from_server_ts1
                #connection.sendall(data_from_server_ts1)
            except socket.timeout as e:
                print "time out error occured! - ts1"
                timeout1 = True
                #connection.sendall("timeout occured")



            try:
                cs2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error as err:
                exit()

            if ts2Hn == "local":
                host_addr2 = socket.gethostbyname(socket.gethostname())
            else:
                host_addr2 = socket.gethostbyname(ts2Hn)

            server_binding2 = (host_addr2,ts2Port)
            cs2.connect(server_binding2)
            cs2.sendall(data)
            cs2.settimeout(5.0)
            data_from_server_ts2=""

            try:
                data_from_server_ts2 = cs2.recv(1024)
                timeout2 = False
                print "recieved from ts2 "+data_from_server_ts2
            except socket.timeout as e:
                print "timeout ts2"
                timeout2 = True


            if timeout2 and timeout1:
                connection.sendall(data + " - ERROR: HOST NOT FOUND")
            elif timeout2:
                print "sending " + data_from_server_ts1
                connection.sendall(data_from_server_ts1)
            else:
                print "sending "+data_from_server_ts2
                connection.sendall(data_from_server_ts2)





if __name__ == "__main__":
    t1 = threading.Thread(name='ls', target=ls)
    t1.start()
