#!/usr/bin/env python3
import subprocess,socket,time,os

# IP and Port config
HOST = 'localhost'
PORT = 2986
#

#TODO setup config
#TODO setup unquie printer id's



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall('printShake'.encode())
print("Connection to server created")
while True:
    data = s.recv(1024)
    #print(data.decode())
    decData=data.decode()
    if decData[:4] == "port":
        print("Swapping to assinged port ",data[5:])
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        time.sleep(4)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = int(data[5:])
        s.connect((HOST,port))
    elif decData == "quit":
        break
    elif decData == "cd":
        print("POGGERS")
    elif decData[:12]=='transferFile':
        print("transfering file to: ",decData[13:])
        g = open(decData[13:], 'w')
        while True:
            l = s.recv(1024)
            try:
                if l.decode() == 'EOFX': 
                    break
            except: 
                pass
            g.write(l.decode())
        g.close()
        s.sendall('EOFX'.encode())
    # else:
    #     proc = subprocess.Popen(data.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    #     stdoutput = proc.stdout.read() + proc.stderr.read()
    #     stdoutput.decode()
    #     s.sendall(stdoutput)
    #s.sendall('EOFX'.encode())
s.close()