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
        self.bedTemp = 0
        self.targetBedTemp = 0
        self.exTemp = 0
        self.targetExTemp = 0

    def connect(self):
        try:
            self.connection = serial.Serial(port=self.port,
                                            baudrate=self.baud, timeout=0.25, parity=serial.PARITY_NONE)
            self.listener = threading.Thread(name="Listening Print therad", target=self._listen) # if this doesnt work on linux change to parity work around
            self.listener.start()
        #except serial.SerialException as e:
        except:
            print("Could not connect to the printer, please make sure its connected.")
            self.alive = False
        self.alive = True

    def disconnect(self):
        self.connection.close()
        self.printing = False
        self.alive = False

    def execute(self, command):
        if self.printing:
            self.printQueue.appendleft(command)
            print("addding to queue")
        else:
            print("Executing imediatly: ",command)
            self._send(command)

    def load(self, file):
        print("loading printer queue")
        with open(file, 'rb') as f:
            dat = f.read().decode()
            dat = dat.splitlines()
            for line in dat:
                if line[:1] != ";":
                    line = line.split(";")
                    if "M109" in line:
                        self.targetExTemp = line[5:]
                    if "M190" in line:
                        self.targetBedTemp = line[5:]
                    self.totalLines += 1
                    self.printQueue.append(line[0])
        return True
                
    def start(self, gcode):
        self.printing = True
        self.load(gcode)
        self.execute("M110")
        self.execute("M75")
        self.printingThread = threading.Thread(name="Printing Thread", target=self._print)
        self.printingThread.start()
        return True

    def pause(self):
        if self.printing:
            self.execute("M76")
            self.execute("M600 X0 Y0")
            self.printing = False
            self.printingPause = True
            self.printingThread.join()
            self.printingThread = None

    def stop(self): #fix this stuff
        if self.printing or self.printingPause:
            self.printing = False
            
            print("stopping the pring job")
            self.execute("M0 Stopping Print")
            print("stopping command sent")
            self.execute("M77")
            print("Stopping timer")
            self.execute("M109 S0")
            self.execute("M190 S0")
            self.execute("M84")
            self.execute("G28 X0 Y0")
            print("homing")
            self.execute("M108")
            self.lineNumber=0
            #self.printingThread.join()
            print("ending print thread")
            #self.printingThread = None

    def resume(self):
        if self.printingPause:
            self.execute("M75")
            self.printing = True
            self.printingPause = False
            self.printingThread = threading.Thread(name="Printing Thread", target=self._print)
            self.printingThread.start()
    
    def progress(self):
        return (self.lineNumber, self.totalLines)

    def status(self):# add M78 m31
        return (self.printing, self.printingPause), (self.bedTemp, self.exTemp), (self.lineNumber, self.totalLines)


#rework to support wifis
    def _send(self, command):
        command = "N{0} {1}".format(self.lineNumber, command)
        command = "{0}*{1}\n".format(command, functools.reduce(lambda x, y: x ^ y, map(ord, command)))
        print("SEND:", command)
        self.connection.write(bytes(command, 'utf-8'))
        self.lineNumber += 1
        
        

    def _readLine(self):
        return self.connection.readline().decode()

    def _listen(self):
        #last = None
        while self.connection.is_open:
            try:
                line = self._readLine().strip()
                if len(line) >= 1:
                    if "busy" in line:
                        #print("busy")
                        pass
                    if line[0] == "T":
                        line = line.split(" ")
                        #print(line)
                        self.bedTemp = line[2].split(":")[1]
                        #print("\nBed Temp: ", self.bedTemp)
                        self.exTemp = line[0].split(":")[1]
                        #print("Extruder Temp: ", self.exTemp)
                        continue
                    elif self.printing and "ok" in line: #add tempature polling
                        self.needCommand = True
                        #print("getting new command")
                    #print("line o: ",line[0])
                    print("RECIVED: ", line)
            except:
                print("Errror in reading the printer ")
                self.alive = False

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