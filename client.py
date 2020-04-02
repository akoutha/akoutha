import threading
import time
import random
import sys
import socket


def client():
    hostname = sys.argv[1]
    rsPort = int(sys.argv[2])
    tsPort = int(sys.argv[3])
    connectTS = 0  # check to see if TS server is connected or not
    tsHostname = ""
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

    server_binding = (host_addr, rsPort)
    cs.connect(server_binding)

    with open("PROJI-HNS.txt") as fp:
        line = fp.readline()  # get first line
        line = line.strip()  # remove spaces
        file = open("RESOLVED.txt", "w+")
        while line:
            print "[C]: Data sent: " + line
            cs.sendall(line)  # send to rs
            data_from_server = cs.recv(1024)  # Receive data from the server
            print("[C]: Data received: {}".format(
                data_from_server.decode('utf-8')))
            dataList = data_from_server.split()  # split data from server

            # print dataList

            if dataList[2] == "A":  # if available
                file.write(data_from_server+"\n")
                print "[C]: wrote onto file - RS"
            else:  # check TS if not available
                print "[C]: no match in rs table, checking TS table"
                tsHostname = dataList[0]

                if dataList[0] == "localhost":
                    tsHostname = socket.gethostname()
                else:
                    tsHostname = dataList[0]

                if connectTS == 0:  # initial connection to TS
                    # print "intial TS connect"
                    connectTS = connectTs(tsHostname, tsPort)

                connectTS.sendall(line)  # send to ts
                data_from_server = connectTS.recv(1024)  # recv from ts

                print("[C]: Data received from TS server: {}".format(
                    data_from_server.decode('utf-8')))
                dataList = data_from_server.split()

                if dataList[2] == "A":
                    file.write(data_from_server+"\n")
                    print "[C]: wrote onto file - TS"
                else:  # not found in any server
                    print "[C]: No match in TS - ERROR"
                    file.write(data_from_server+"\n")

            line = fp.readline()  # move next line

    cs.close()
    if connectTS!=0 :
        connectTS.close()
    exit()


def connectTs(host, tsPort):
    try:
        tcs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Connect to TS")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))

    host_addr = socket.gethostbyname(host)

    # connect to the server on local machine
    server_binding = (host_addr, tsPort)
    tcs.connect(server_binding)
    return tcs


if __name__ == "__main__":
    t2 = threading.Thread(name='client', target=client)
    t2.start()
    print("Done.")
