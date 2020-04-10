import threading
import time
import random
import sys
import socket


def client():

    hostname = sys.argv[1]
    lsPort = int(sys.argv[2])

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

    server_binding = (host_addr, lsPort)
    cs.connect(server_binding)

    with open("PROJ2-HNS.txt") as fp:
        line = fp.readline()  # get first line
        line = line.strip()  # remove spaces
        file = open("RESOLVED.txt", "w+")
        while line:
            cs.sendall(line)
            data_from_server = cs.recv(1024)  # Receive data from the server
            print("[C]: Data received: {}".format(data_from_server.decode('utf-8')))
            file.write(data_from_server+"\n")

            line = fp.readline()




if __name__ == "__main__":
    t2 = threading.Thread(name='client', target=client)
    t2.start()
    print("Done.")
