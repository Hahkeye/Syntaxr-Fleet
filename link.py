import serial, threading, queue, time

class link():
    def __init__(self, port = None, baud = None):
        self.port = port
        self.baud = baud
        self.printQueue = queue.Queue()
        self.printingThread = None
        self.printing = False
        self.alive = False
        self.lineNumber = 0
        self.connection = None
        self.connect(port,baud)

    def connect(self, port, baud):
        try:
            self.connection = serial.Serial(port=self.port,
                                            baudrate=self.baud, timeout=0.25, parity=serial.PARITY_ODD)
            # self.connection.close()
            # self.connection.parity = serial.PARITY_NONE
            # self.connection.open()
        except serial.SerialException as e:
            print("Could not connect ",e)
            self.alive = False
        self.alive = True


    def disconnect(self):
        print("bye")
        self.connection.close()
        self.printing = False
        self.alive = False


    def send(self,command,line):
        prefix = "N",line," ",command
        self.connection.write(bytes(command+"\n",'utf-8'))
        pass

    def excute(self,command):
        self.printQueue.put_nowait(command)
        pass

    def start(self):
        self.printing=True #throw everything into print queue
        self._send("M110",-1)
        self.printingThread = threading.Thread(target = self._print)
        self.printingThread.start()
        return True

    def _send(self, command, line):
        prefix = "N", line, " ",command
        self.connection.write(bytes(command+"\n", 'utf-8'))   
    def _readLine(self):
        line = self.connection.readline()
        return line

    def _print(self, resuming= False):
        print("starting print")
        while not self.printQueue.empty():
            time.sleep(.001)
            self.lineNumber+=1
            self._send(self.printQueue.get_nowait(), self.lineNumber)
            self.printQueue.task_done()
        self.disconnect()

connection = link('COM6',115200)
#connection.send("G28",-1)
code=open("test.gcode","r")
lines = code.readlines()
code.close()
print("read from: ",connection._readLine())
for i in lines:
    print(i)
    connection.printQueue.put(i)
connection.start()
#TODO: Need to close the thread when its done and overall fool proof it.