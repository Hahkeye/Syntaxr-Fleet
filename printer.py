import serial, threading, time, functools
from collections import deque

class Printer():
    def __init__(self, port=None, baud=None):
        self.port = port
        self.baud = baud
        self.printQueue = deque()
        self.printingThread = None
        self.listener = None
        self.printingPause = None
        self.printing = False
        self.alive = False
        self.needCommand = True
        self.lineNumber = 0
        self.totalLines = 0
        self.connection = None
        self.bedTemp = None
        self.exTemp = None
        #self.connect(port,baud)

    def connect(self):
        try:
            self.connection = serial.Serial(port=self.port,
                                            baudrate=self.baud, timeout=0.25, parity=serial.PARITY_ODD)
        #except serial.SerialException as e:
        except:
            print("Could not connect to the printer, please make sure its connected.")
            self.alive = False
        self.alive = True

    def disconnect(self):
        print("bye")
        self.connection.close()
        self.printing = False
        self.alive = False

    def execute(self, command):
        self.printQueue.appendleft(command)

    def load(self, file):
        with open(file, 'rb') as f:
            dat = f.read().decode()
            dat = dat.splitlines()
            for line in dat:
                if line[:1] != ";":
                    print(line)
                    line = line.split(";")
                    temp = "N{0} {1}".format(self.totalLines, line[0])
                    self.totalLines += 1
                    self.printQueue.append(temp)
        return True
                
    def start(self, gcode):
        self.printing = True #throw everything into print queue
        self.execute("N-1 M110")
        self.load(gcode)
        self.printingThread = threading.Thread(name="Printing Thread", target=self._print)
        self.printingThread.start()
        self.listener = threading.Thread(name="Listening Print therad", target=self._listen)
        self.listener.start()
        return True

    def pause(self):
        self.execute("M600 X0 Y0")
        self.printing = False
        self.printingPause = True
        self.printingThread.join()
        self.printingThread = None

    def resume(self):
        self.printing = True
        self.printingThread = threading.Thread(name="Printing Thread", target=self._print)
        self.printingThread.start()
    
    def progress(self):
        return (self.lineNumber, self.totalLines)

    def status(self):
        return (self.printing, self.bedTemp, self.exTemp)


#rework to support wifis
    def _send(self, command):
        command = "{0}*{1}\n".format(command, functools.reduce(lambda x, y: x ^ y, map(ord, command)))
        #print("SEND:", command)
        self.connection.write(bytes(command, 'utf-8'))
        self.lineNumber += 1

    def _readLine(self):
        return str(self.connection.readline().decode())
        #pass
    def _listen(self):
        while self.connection.is_open:
            line = self._readLine().split(" ")            
            if len(line) > 1:
                print(line)
                self.needCommand = True
                self.exTemp = line[2][1:]
                self.bedTemp = line[3][1:-2].strip()
                print("RECIVED: ", line)

    def _print(self):
        while len(self.printQueue) != 0:
            time.sleep(.001)
            if self.needCommand: #need to call finish when its over
                self.needCommand = False
                self._send(self.printQueue.popleft())
                #self
        self.printing = False
        # self.printingThread.join()
        self.printingThread = None
        print("Done printing")
        

#TODO: Need to close the thread when its done and overall fool proof it.