#!/usr/bin/env python3
import time,os,sys,printer,clientSocket,json

# IP and Port config
HOST = 'localhost'
PORT = 2986
#
#Printer Connection Config
# PPORT = '/dev/ttyACM0'
# BUAD = 115200
PPORT = 'COM4'
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
        self.gcodes = list()
        self.taskMaster = clientSocket.talk(HOST, PORT)
        try:
            self.printLink = printer.Printer(PPORT, BUAD)
        except:
            print("Failed to start printer connection will try again when its important")

    def status(self):
        print("Sending status")
        self.taskMaster.send("status "+json.dumps((self.printLink.status(),self.prints())))

    def pause(self):
        print("Pauseing print")
        self.printLink.pause()

    def stop(self):
        print("stopping")#this still needs to be impletmetned in printer.py
        self.printLink.stop()

    def resume(self):
        print("resuming")
        self.printLink.resume()

    def prints(self):
        print(os.getcwd())
        self.gcodes = os.listdir("C:\\Users\\reali\source\\repos\\Syntaxr-Fleet\\prints")
        return self.gcodes

    def ftp(self, name):
        if self.taskMaster.getFile(name):
            self.status()
        

    def main(self):
        while True: #make sure it cant do anything with out having a connecto to the host and the printer
            try:
                if not self.printLink.alive: self.printLink.connect()
            except:
                print("Failed To connect to printer, please check usb connection")
            try:
                if not self.taskMaster.alive: self.taskMaster.connect(json.dumps((self.name, self.ptype, self.volume)))
            except:
                print("Failed to connect to host, please make sure host is runing")
            time.sleep(3)
            # print("w")
            #while True:
            #while self.taskMaster.alive:
            print("Tasko Master: ",self.taskMaster.alive," PrinEEt link:", self.printLink.alive)
            while self.taskMaster.alive and self.printLink.alive:
                #print("loops")
                #print("Task: {0} Print: {1}".format(self.taskMaster.alive,self.printLink.alive))
                task = self.taskMaster.getMsg()#rework getmsg 
                if task is not None:
                    print("New message recieved from master: ", task)
                    #time.sleep(5)
                    if task[:10] == "startPrint":
                        print("Starting Print")
                        target = task[11:]
                        print(target)
                        print(self.printLink.start("C:\\Users\\reali\source\\repos\\Syntaxr-Fleet\\prints\\{0}".format(target)))#change to prints file "prints\{0}".format(target)
                    elif task[:6] == "status":
                        self.status()
                    elif task[:5] == "pause":
                        self.pause()
                    elif task[:5] == "stop":
                        self.stop()
                    elif task[:6] == "resume":
                        self.resume()
                    elif task[:12] == "fileTransfer":
                        self.ftp(task[12:])


                    task = None
                #print("Task: {0} Print: {1}".format(self.taskMaster.alive,self.printLink.alive))
                #time.sleep(1)
                # self.status()  
            print("Exited")
if __name__ == "__main__":
    p = Printer("Ender5 Pro", "FDM", (200, 200, 320))
    p.main() 