import sys,socket,time


class talk(object):
    def __init__(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hostIp = ip
        self.port = port
        self.last = None
        self.new = None
        self.alive = False
    def getMsg(self):
        try:
            return self.socket.recv(1024).decode()
        except ConnectionResetError as e:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.alive = False
    def connect(self):#Connects to server and does port nogetiation to its correct port
        try:
            self.socket.connect((self.hostIp, self.port))
            self.socket.sendall('printShake'.encode())
            self.alive = True
        except socket.error as e:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return
        data = self.getMsg()
        print(data)
        print("Swapping to port ", data[5:])
        #self.port = int(data[5:])
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        time.sleep(2)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.hostIp, int(data[5:])))
    def check(self):
        data = self.getMsg()
        if data != self.last:
            self.new = data
            self.last = self.new
            return True
        return False
    def send(self, msg):
        self.socket.sendall(msg.encode())
    def disconnect(self):
        print(self.socket)
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()