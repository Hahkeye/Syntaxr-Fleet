#!/usr/bin/env python3
import subprocess,socket,time,os,sys,printer,clientSocket,threading

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
        self.name=name
        self.ptype=ptype
        self.volume=volume
        self.id=42
        self.taskMaster = clientSocket.talk(HOST, PORT)
        try:
            self.printLink = printer.Printer(PPORT, BUAD)
        except:
            print("Failed to start printer connection will try again when its important")

    def main(self):
        try:
            self.taskMaster.connect()
            #time.sleep(10)
        except:
            print("Failed to connect to host, please make sure host is runing")
            sys.exit()
        #self.taskMaster.connect()
        self.printLink.connect()
        while self.printLink.alive:
        #while True:
            print(threading.enumerate())
            if self.taskMaster.check():
                task = self.taskMaster.getMsg()
                if task[:10] == "startPrint":
                    target = task[11:]
                    print("starting task: ",target)
                    # try:
                    #     if os.path.exists("{0}".format(target)):#change this to linux
                    #         print(self.printLink.start("{0}".format(target)))#change to prints file "prints\{0}".format(target)
                    # except:
                    #     print("specified file not found")
                    print(self.printLink.start("C:\\Users\\reali\source\\repos\\Syntaxr-Fleet\\{0}".format(target)))#change to prints file "prints\{0}".format(target)

            time.sleep(7)
            print(self.printLink.progress())


            #x=input('asdasda')

p = Printer("TestPrinter","FDM",(120, 120, 120))
p.main()