#!/usr/bin/env python3
import socket,os,time,threading,sys,pickle,json
from helper import menu
# Socket configuration

HOST = '0.0.0.0'
PORT = 2986
LISTNER = None
THRPRT = PORT
CLIENTS = list()
HANDSHAKE = "printShake"
PRINTERS = list()
AVIABLE = list()
#TODO setup unquie printer id's or unqiue connection id's from


class Client(object):
    def __init__(self, sock, add, name = None, drive = None, volume = (0,0,0)):
        self.socket = sock
        self.address = add
        self.name = name
        self.drive = drive
        self.volume = volume
        self.status = (False, None, None)
    def setStatus(self, stat):
        self.status = stat
    def string(self):
        return "{0} {1} {2} {3}".format(self.name, self.drive, self.volume, self.status)




def _listner():
    global THRPRT,LISTNER
    #print("Listner Starting")
    LISTNER = socket.create_server(address=(HOST, PORT), family=socket.AF_INET)
    LISTNER.listen(1)
    sock, address = LISTNER.accept()
    data = sock.recv(1024).decode()
    #print("DATA recived: ", data)
    if data[:10] == HANDSHAKE:
        print("printer connecting")
        THRPRT += 1
        #print("Swaping to port ", THRPRT)#FIX LISTNEr THreadthat you broke
        sock.sendall("port {0}".format(THRPRT).encode())
        details = json.loads(data[10:])
        clientThread = threading.Thread(name='clientHandling', target=_clientHandler, args=(HOST, THRPRT, details), daemon=True)
        clientThread.start()
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        LISTNER = None
        
        
        
       
def _clientHandler(host, port, details):
    _refresh()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(1)
        sock, address = s.accept()
        c = Client(sock, address, details[0], details[1], details[2])
        CLIENTS.append(c)
        #print("calling intial status")
        sock.sendall("status".encode())
        while True:
            try:
                data = sock.recv(1024)
                data = data.decode()
            except:
                _kill(c)
                break
            #print("data from client reived: ", data)
            if data[:6] == "status":
                stat = json.loads(data[7:])
                #print("status recieved:", stat[0])
                c.status = stat
                if c.status[0] is False:
                    AVIABLE.append(c)
                menu(CLIENTS, AVIABLE)
            # if data != "EOFX" or data != '':
            #     print("Client ", host[0], ": ", data)
    except:
        _kill(c)
       # sys.exit()

def _kill(client):
    print("Closing a client of sorts")
    try:
        print("removing from client from client list")
        client.socket.shutdown(socket.SHUT_RDWR)
        client.socket.close()
        CLIENTS.remove(client)
    except:
        print("failed because its probaly was already attmeped")
    try:
        print("removing client from aviable")
        AVIABLE.index(client)
        AVIABLE.remove(client)
    except:
        pass
    menu(CLIENTS, AVIABLE)
def _refresh():
    #print("refreshing listner")
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
        #print("First time start of listener")
        _refresh()
    
    menu(CLIENTS, AVIABLE)
    choice = input(": ")
    #choice = 69
    if choice == "1":
        choice2 = input("Enter id: ")
        choice3 = input("enter Command: ")
        CLIENTS[int(choice2)].socket.sendall(choice3.encode())
    if choice == "2":
        choice2 = input("Enter id: ")
        CLIENTS[int(choice2)]
    if choice == "3":
        menu(CLIENTS, AVIABLE)
        print("CLIENTS:                         ",len(CLIENTS))
        print("LISTNEr: ",LISTNER)
# elif selcmd[:12] == 'transferFile':
#             print("attemping to transfer file")
#             selected.send(selcmd.encode())
#             print(fileTransfer(selected, str(selcmd[13:])))