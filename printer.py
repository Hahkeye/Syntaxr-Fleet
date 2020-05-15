import serial, threading, time, functools
from collections import deque

class Printer():
    def __init__(self, port=None, baud=None):
        self.port = port
        self.baud = baud
        # self.id = "abvsads"
        self.printQueue = deque()
        self.printingThread = None
        self.listener = None
        self.printingPause = None
        self.printing = False
        self.alive = False
        self.needCommand = True
        self.lineNumber = 0
        self.totalLines = 11
        self.connection = None
        self.bedTemp=None
        self.exTemp=None
        #self.connect(port,baud)

    def connect(self):
        try:
            self.connection = serial.Serial(port=self.port,
                                            baudrate=self.baud, timeout=0.25, parity=serial.PARITY_ODD)
        except serial.SerialException as e:
            print("Could not connect ", e)
            self.alive = False
        self.alive = True

    def disconnect(self):
        print("bye")
        self.connection.close()
        self.printing = False
        self.alive = False

    # def excute(self,command):
    #     self.printQueue.put_nowait(command)
    def execute(self,command):
        self.printQueue.appendleft(command)

    def start(self):
        self.printing=True #throw everything into print queue
        self.execute("N-1 M110")
        self.printingThread = threading.Thread(target = self._print)
        self.printingThread.start()
        self.listener = threading.Thread(target = self._listen)
        self.listener.start()
        return True

    def pause(self):
        self.printing = False
        self.printingPause = True
        self.printingThread.join()
        self.printingThread = None

    def resume(self):
        self.printing = True
        self.printingThread = threading.Thread(target = self._print)
        self.printingThread.start()
    
    def progress(self):
        return self.lineNumber//self.totalLines


#Rework send command to include checksum
    def _send(self,command):
        command = "{0}*{1}\n".format(command, functools.reduce(lambda x, y: x ^ y, map(ord, command)))
        print("SEND:", command)
        self.connection.write(bytes(command, 'utf-8'))
        self.lineNumber += 1

    # def _send(self, command):
    #     check = functools.reduce(lambda x, y: x ^ y, map(ord, command))
    #     prefix = "N{0} {1} ".format(self.lineNumber,command)
    #     command=""+prefix+"*{0}\n".format(check)
    #     print("Sending comannd: ", command)
    #     self.connection.write(bytes(command, 'utf-8'))
    #     self.lineNumber += 1

    def _readLine(self):
        return str(self.connection.readline())
        #pass
    def _listen(self):
        while self.connection.is_open:
            line = self._readLine()
            if line != "b''":
                self.needCommand = True
                print("RECIVED: ", line[2:len(line)-3])


    # def _print(self, resuming=False):
    #     print("starting 3d print\n")
    #     while not self.printQueue.empty():
    #         time.sleep(.001)
    #         if self.needCommand:
    #             self.needCommand = False
    #             self._send(self.printQueue.get_nowait())
    #             self.printQueue.task_done()

    def _print(self):
        while len(self.printQueue)!=0:
            time.sleep(.001)
            if self.needCommand:
                self.needCommand = False
                self._send(self.printQueue.popleft())
                #self

# connection = Printer('COM6',115200)
# connection.connect()
# #connection.send("G28",-1)
# code=open("test.gcode","r")
# lines = code.readlines()
# code.close()
# #print("read from: ",connection._readLine())
# x=0
# for i in lines:
#     connection.printQueue.append("N{0} {1}".format(x, i.strip()))
#     x+=1
# connection.start()
# time.sleep(5)
# print("Intrupting command")
# x = input()

#TODO: Need to close the thread when its done and overall fool proof it.