import rpyc
from collections import deque

class MasterService(rpyc.Service):
   # ALIASES = ["Master","ReportingServer"]
    class exposed_MonitorAndDispatch(object):
        def __init__(self):
            self.printers = None
            self.freePrinters = 0
            self.workingPrinters = 0
            self.jobs = deque()
            


    def on_connect(self, conn):
        print("Client Connected to server",conn)
        #print(conn)
        #print("Number of clients",t.clients)
        pass
    def on_disconnect(self,conn):
        print("Client Disconnected to server",conn)
        pass
    def exposed_test(self):
        return "Poggers"

    def exposed_bar(self,func):
        return func() + "bar"

    # def sendprint(self, code):
    #     pass
    exposed_var = 10
    # while True:
    #     x=input("Stall")


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(MasterService(), port=2986)
    t.start()
    