import rpyc

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



def fooFunc():
    return "foo"

def test1Func():
    return "test1"    
def test2Func():
    return "test2"

c = rpyc.connect("localhost", 2986)
#print(rpyc.discover("MASTER"))
print(c.root.get_service_name())
print(c.root.get_service_aliases())
print(c.root.bar(test2Func))
x = input("Stall")