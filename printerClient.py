#import printrun
class Printer(object):
    def __init__(self, name, printerType, printVolume):
        self.name = name
        self.printerType = printerType
        self.printVolume = printVolume #x,y,z
        self.currentFile = None
        self.numberOfCommans=0
        self.precentDone=0



    def out(self):
        return "Name: ",self.name," Type: ",self.printerType," Volume: ",self.printVolume

    def startPrint(self,gcode):
        for line in gcode:
            pass#send to printer
        pass
        #pronterface to supply gcode commands
    def ternimal(self):
        #pronterface termnial
        pass




p = Printer("Ender5","FDM",(120, 120, 120))
print(p.name)
print(p.printVolume)
print(p.printerType)
print(p.out())