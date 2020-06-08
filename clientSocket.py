import sys, socket, time, os, logging


class talk(object):
    def __init__(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hostIp = ip
        self.port = port
        self.last = None
        self.alive = False
    def getMsg(self):
        try:
            data = self.socket.recv(1024).decode()
            print("datat recived: ",data)
            return data
        except ConnectionResetError as e:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.alive = False
        except OSError as e:
            pass
    def getFile(self, dat):
        name = dat[12:].split("\\")
        name = name[len(name)-1]
        f = open("C:\\Users\\reali\source\\repos\\Syntaxr-Fleet\\printss\\"+name,"wb")
        while True:
            l = self.socket.recv(1024)
            try:
                if l.decode().endswith('EOFX') == True: break
            except:
                pass
            f.write(l)
        f.close()
        return True
    def connect(self, info):#Connects to server and does port nogetiation to its correct port
        try:
            self.socket.connect((self.hostIp, self.port))
            self.socket.sendall('printShake {0}'.format(info).encode())
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
        time.sleep(1)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.hostIp, int(data[5:])))
    def send(self, msg):
        self.socket.sendall(msg.encode())
    def disconnect(self):
        print(self.socket)
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()