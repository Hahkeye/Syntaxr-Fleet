#!/usr/bin/env python3
import socket, os, time, threading, sys, json, logging
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
    def __init__(self, sock, add, name=None, drive=None, volume=(0, 0, 0)):
        self.socket = sock
        self.address = add
        self.name = name
        self.drive = drive
        self.volume = volume
        self.gcodes = list()
        self.progress = (0, 0)
        self.temps = (0, 0)
        self.status = (False, False)
    def setStatus(self, stat):
        self.status = stat
    # def string(self):
    #     return "{0} {1} {2} {3}".format(self.name, self.drive, self.volume, self.status)
    def string(self):
        return "{0} | Active:{1}".format(self.name, self.status[0])
    def send(self, message):
        self.socket.sendall(message.encode())
        return "sent"
    # def stop(self):
    #     self.send("stop")
    def fileTransfer(self, file):
        logging.info("Starting file transfer to {0}".format(self.name))
        # try:
        #     self.socket.sendall('fileTransfer {0}'.format(file))
        #     time.sleep(1)
        #     with open(file, 'rb') as f:
        #         fileData = f.read()
        #         self.socket.sendall(fileData)
        #         time.sleep(1)
        #         self.socket.sendall('EOFX'.encode())
        #     f.close()
        #     return "Upload complete"
        # except:
        #     return "Upload failed"
        
        self.socket.sendall('fileTransfer {0}'.format(file).encode())
        time.sleep(1)
        with open(file, 'rb') as f:
            fileData = f.read()
            self.socket.sendall(fileData)
            time.sleep(1)
            self.socket.sendall('EOFX'.encode())
        f.close()
        return "Upload complete"


def _listner():
    global THRPRT,LISTNER
    logging.info("Client Listener started.")
    LISTNER = socket.create_server(address=(HOST, PORT), family=socket.AF_INET)
    sock, address = LISTNER.accept()
    data = sock.recv(1024).decode()
    #print("DATA recived: ", data)
    if data[:10] == HANDSHAKE:
        logging.info("New Client connecting. ip: {0} port: {1}".format(address, sock))
        THRPRT += 1
        #print("Swaping to port ", THRPRT)#FIX LISTNEr THreadthat you broke
        sock.sendall("port {0}".format(THRPRT).encode())
        details = json.loads(data[10:])
        print("Details:  ", details)
        clientThread = threading.Thread(name='clientHandling', target=_clientHandler, args=(HOST, THRPRT, details), daemon=True)
        clientThread.start()
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        LISTNER = None



def _clientHandler(host, port, details):#Might need to thread out both listner and send
    logging.info("Starting a client handler on IP:{0} Port:{1}".format(host, port))
    _refresh()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(1)
        sock, address = s.accept()
        c = Client(sock, address, details[0], details[1], details[2])
        CLIENTS.append(c)
        print("calling intial status")
        sock.sendall("status".encode())
        while True:
            try:
                data = sock.recv(1024)
                data = data.decode()
            except:
                _kill(c)
                break
            print("data from {0} recieved: {1}".format(c,data))
            if data[:6] == "status":                 # rework status to include every thing
                stat = json.loads(data[7:])
                print("status recieved:", stat[0])
                c.status = stat[0][0]
                #print("Statis: ", stat[0][0])
                c.temps = stat[0][1]
                #print("Temps: ", stat[0][2])
                c.progress = stat[0][2]
                #print("Progress: ", stat[0][2])
                c.gcodes = stat[1]
                if c.status[0] is False:
                    AVIABLE.append(c)
                
    except:
        _kill(c)
        # sys.exit()

def _kill(client):
    logging.info("Client has disconnected, removing from lists")
    # try:
    #     client.socket.shutdown(socket.SHUT_RDWR)
    #     client.socket.close()
    #     CLIENTS.remove(client)
    # except:
    #     logging.warning("Failed to disconnect a client and remove it from clients. ")
    client.socket.shutdown(socket.SHUT_RDWR)
    client.socket.close()
    CLIENTS.remove(client)


    try:  
        AVIABLE.index(client)
        AVIABLE.remove(client)
    except:
        logging.warning("Failed to disconnect a client and remove it from aviable list.")
def _refresh():
    #logging.info("refreshing listernet thread because of a connection.")
    LISTNER = threading.Thread(name='listner', target=_listner, daemon=True)
    LISTNER.start()



def main():
    global LISTNER
    logging.basicConfig(filename='./logs/server.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info("Master server starting")
    while True:
        if LISTNER is None:
            #time.sleep(5)
            #print("First time start of listener")
            #LISTNER = 5e
            _refresh()
        time.sleep(1)
        #print(threading.enumerate())
        

#main()
# elif selcmd[:12] == 'transferFile':
#             print("attemping to transfer file")
#             selected.send(selcmd.encode())
#             print(fileTransfer(selected, str(selcmSd[13:])))