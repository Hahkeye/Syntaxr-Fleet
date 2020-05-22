#!/usr/bin/env python3
import subprocess,socket,time,os,sys,printer,clientSocket,threading,pickle,json

# IP and Port config
HOST = 'localhost'
PORT = 2986
#
#Printer Connection Config
# PPORT = '/dev/ttyACM0'
# BUAD = 115200
PPORT = 'COM6'
BUAD = 115200
#



#TODO setup config
#TODO setup unquie printer id's

class Printer(object):
    def __init__(self, name, ptype, volume=(0, 0, 0)):
        self.name = name
        self.ptype = ptype
        self.volume = volume
        self.idle = True
        self.id = 42
        self.taskMaster = clientSocket.talk(HOST, PORT)
        try:
            self.printLink = printer.Printer(PPORT, BUAD)
        except:
            print("Failed to start printer connection will try again when its important")

    def main(self):
        while True: #make sure it cant do anything with out having a connecto to the host and the printer
            try:
                if not self.printLink.alive: self.printLink.connect()
            except:
                print("Failed To connect to printer, please check usb connection")
            try:
                if not self.taskMaster.alive: self.taskMaster.connect()
            except:
                print("Failed to connect to host, please make sure host is runing")
            time.sleep(5)
            #while self.taskMaster.alive:
            while self.taskMaster.alive and self.printLink.alive:
                self.idle = self.printLink.printing
                task = self.taskMaster.getMsg()
                if task is not None:
                    print("New message recieved from master: ",task)
                    if task[:10] == "startPrint":
                        print("Starting Print")
                        target = task[11:]
                        # try:
                        #     if os.path.exists("{0}".format(target)):#change this to linux
                        #         print(self.printLink.start("{0}".format(target)))#change to prints file "prints\{0}".format(target)
                        # except:
                        #     print("specified file not found")
                        #self.idle = False
                        print(self.printLink.start("C:\\Users\\reali\source\\repos\\Syntaxr-Fleet\\{0}".format(target)))#change to prints file "prints\{0}".format(target)
                    elif task[:6] == "status":
                        print("Sending status")
                        self.taskMaster.send("status "+json.dumps(self.printLink.status()))
                    elif task[:5] == "pause":
                        print("Pausing print")
                        self.printLink.pause()
                    task = None
                #time.sleep(1)
if __name__ == "__main__":
    p = Printer("TestPrinter", "FDM", (120, 120, 120))
    p.main()