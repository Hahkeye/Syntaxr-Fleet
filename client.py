import rpyc,pickle



from os import path

class Printer(object):
    def __init__(self, name, printerType, printVolume):
        self.name = name
        self.printerType = printerType
        self.printVolume = printVolume #x,y,z
        self.currentFile = None
        self.numberOfCommands=0
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
def switchStateFunc(state):
    pass


printer = None
def save():
    with open('printer.pickle', 'wb') as f:
        print("Saving")
        pickle.dump(printer, f, pickle.HIGHEST_PROTOCOL)

def load():
    if(path.exists("printer.pickle")):
        with open('printer.pickle','rb') as f:
            printer=pickle.load(f)
        return True
    return False

def new():#implement first time setup
    pass

def main():
    if not load():
        new()
    

#printer = Printer("Ender5","FDM",(120, 120, 120))
c = rpyc.connect("localhost", 2986)
states=[3]
states[0]="terminal"
states[1]="print"
states[2]="report"

#print(rpyc.discover("MASTER"))
print(c.root.get_service_name())
print(c.root.get_service_aliases())
print(c.root.bar(test1Func))
print(printer.out())
x = input("Save y/n?")

if x == "y":
    save()