import threading
import time
import random
import socket
import os
import sys
from threading import Thread
import traceback

def ts():

    table = []
    populateDNSTable(table)
    # printDNSTable(table)

    while True:
        try:
            ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("[S]: Server socket created")
        except socket.error as err:
            print('socket open error: {}\n'.format(err))
            exit()
        port = int(sys.argv[1]) if len(sys.argv) > 1 else 22222
        #port = 22222
        server_binding = ('', port)
        ss.bind(server_binding)
        ss.listen(1)
        host = socket.gethostname()
        print("[S]: Server host name is {}".format(host))
        localhost_ip = (socket.gethostbyname(host))
        print("[S]: Server IP address is {}".format(localhost_ip))
        print('[S]: listening on port:', ss.getsockname()[1])
        while True:

            connection, addr = ss.accept()
            print ("[S]: Got a connection request from a client at {}".format(addr))
            try:
                Thread(target=client_t, args=(
                    connection, table)).start()
            except:
                print("Thread did not start.")
                traceback.print_exc()
        ss.close()


def client_t(connection, table):
    active = True
    print("[S]: Spawned new client thread")
    while active:
        data = connection.recv(1024).strip()
        if(data == ""):
            connection.close()
            active = False
            print("[S]: Killed client thread")

        if data:
            print("[S]: Incoming data: " + data)
            result = findIP(data, table)
            print("[S]: Outgoing data: " + result)

            if result:
                print "data sent!"
                connection.sendall(result)
            else:
                continue

# If there is a match, sends the entry as a string:
# Hostname IPaddress A
# If there is no match, RS sends the string:
# TSHostname - NS
def findIP(hostname, table):
    found = False
    ns = ""
    for row in table:
        for item in row:
            if item.lower() == "NS".lower():
                ns = row[0]+" " + row[1]+" "+row[2]
            if hostname.lower() == item.lower():
                found = True
                entry = row[0]+" " + row[1]+" "+row[2]
                return entry
    # Not found. return ns record
    #if not found:
        #return "NS"
    return ns


def populateDNSTable(table):
    with open("PROJ2-DNSTS1.txt") as f:
        for line in f:
            inner_list = [elt.strip() for elt in line.split(' ')]
            table.append(inner_list)


def printDNSTable(table):
    for row in table:
        for val in row:
            print '{:4}'.format(val),
        print


if __name__ == "__main__":
    t1 = threading.Thread(name='ts', target=ts)
    t1.start()
