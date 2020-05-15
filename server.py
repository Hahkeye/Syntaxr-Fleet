#!/usr/bin/env python3
import socket,os,time,threading,sys
# Socket configuration

HOST = '0.0.0.0'
PORT = 2986
MAIN = False
THRPRT = PORT
CLIENTS = {}
#TODO setup unquie printer id's


def _main():
    print("-----------------------------rEEEEEEEEEEEEEEEEEEEEEEEEEEOPEN")
    global THRPRT, MAIN
    c = socket.create_server(address=(HOST,PORT), family=socket.AF_INET)
    c.listen(1)
    sock, address = c.accept()
    data = sock.recv(1024)
    print("\nData: ",data.decode())
    if data.decode() == 'printShake':
        print("new incomiing connection")
        THRPRT += 1
        sock.sendall("port {0}".format(THRPRT).encode())
        workThread = threading.Thread(name='workerThread', target=_clientHandler, args=(HOST, THRPRT), daemon=True)
        workThread.start()
        time.sleep(1)
        sock.shutdown(socket.SHUT_RDWR)
        print("Closeing scoket")
        sock.close()
        print("setting main")
        MAIN = False
        sys.exit()

def _clientHandler(host,port):
    global CLIENTS
    try:
        print("Spinning off client thread")
        print("Binding client to: ",host)
        print("Binding client to port: ",port)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.bind((host, port))
        client.listen(1)
        sock, address = client.accept()
        CLIENTS[address[1]] = sock
        while True:
            try:
                data= sock.recv(1024)
            except:
                _kill(sock,address)
                sys.exit()
        
        print("Exiting client handler. ",port)
        if data != "EOFX" or data!='':
            print("Client ",host[0],": ",data)
    except:
        _kill(sock,address)
        sys.exit()

def _kill(scoket,address):
    global CLIENTS
    if CLIENTS.get(address):
        CLIENTS[address].shutdown(socket.SHUT_RDWR)
        CLIENTS[address].close()
        CLIENTS.pop(address)

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

def menu():
    print("THREADS ACTIVE: ",threading.active_count())
    print("Threads: ",threading.enumerate())
    print("\nClients: ")
    print(CLIENTS)
    print("------------------------------------")
    print("Exit: 0")
    print("Select: 1")
while True:
    if MAIN is False:
        MAIN = threading.Thread(name='main', target=_main, daemon=True)
        MAIN.start()
        MAIN = True
    
    menu()
    command = input("\nEnter command: ")
    if int(command) == 0:
        sys.exit()
    elif int(command) == 2:
        print(CLIENTS)
    elif int(command) == 1:
        selection = input("Enter the ip of the client")
        selected = CLIENTS.get(int(selection))
        print("selecing client: ",selected)
        selcmd = input("Enter command:")
        if selcmd == 'cd':
            selected.sendall(selcmd.encode())
            pass
        elif selcmd[:12] == 'transferFile':
            print("attemping to transfer file")
            selected.send(selcmd.encode())
            print(fileTransfer(selected, str(selcmd[13:])))
        