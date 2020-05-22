#!/usr/bin/env python3
import socket,os,time,threading,sys,pickle,json
from helper import menu
# Socket configuration

HOST = '0.0.0.0'
PORT = 2986
LISTNER = None
THRPRT = PORT
CLIENTS = {}
HANDSHAKE = "printShake"
PRINTERS = list()
AVIABLE = list()
#TODO setup unquie printer id's or unqiue connection id's from

BAR = None


def _listner():
    global THRPRT, MAIN, BAR
    print("Attemping connection")
    c = socket.create_server(address=(HOST, PORT), family=socket.AF_INET)
    c.listen(1)
    sock, address = c.accept()
    data = sock.recv(1024)
    if data.decode() == HANDSHAKE:
        print("printer connecting")
        print("port hand off")
        THRPRT += 1
        sock.sendall("port {0}".format(THRPRT).encode())
        print("worker hand off")
        workThread = threading.Thread(name='workerThread', target=_clientHandler, args=(HOST, THRPRT), daemon=True)
        workThread.start()
        time.sleep(1)
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        sys.exit()
       

def _clientHandler(host, port):
    global CLIENTS
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.bind((host, port))
        client.listen(1)
        sock, address = client.accept()
        CLIENTS[address[1]] = (sock,False)
        _refresh()
        while True:
            try:
                data = sock.recv(1024)
                data = data.decode()
            except:
                _kill(address[1])
                sys.exit()
            print("data from client reived: ", data)
            if data[:6] == "status":
                stat = json.loads(data[7:])
                print("status recieved:", stat[0])
            if data != "EOFX" or data != '':
                print("Client ", host[0], ": ", data)
    except:
        _kill(address)
        sys.exit()

def _kill(address):
    global CLIENTS
    if CLIENTS.get(address):
        CLIENTS[address].shutdown(socket.SHUT_RDWR)
        CLIENTS[address].close()
        CLIENTS.pop(address)
    menu(CLIENTS)
def _refresh():
    print("refreshing listner")
    global LISTNER
    menu(CLIENTS)
    LISTNER = threading.Thread(name='listner', target=_listner, daemon=True)
    LISTNER.start()


def fileTransfer(sock, file):
    try:
        with open(file, 'rb') as f:
            fileData = f.read()
            sock.sendall(fileData)
            time.sleep(1)
            sock.sendall('EOFX'.encode())
        f.close()
        return "Upload complete"
    except:
        return "Upload failed"

while True:
    if LISTNER is None:
        print("First time start of listener")
        _refresh()
    menu(CLIENTS)

    choice = input(": ")
    if choice == "1":
        choice2 = input("Enter id: ")
        choice3 = input("enter Command: ")
        CLIENTS[int(choice2)].sendall(choice3.encode())
    if choice == "2":
        choice2 = input("Enter id: ")
        CLIENTS[int(choice2)]
# elif selcmd[:12] == 'transferFile':
#             print("attemping to transfer file")
#             selected.send(selcmd.encode())
#             print(fileTransfer(selected, str(selcmd[13:])))