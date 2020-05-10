import rpyc

class MasterService(rpyc.Service):
   # ALIASES = ["Master","ReportingServer"]
    def on_connect(self, conn):
        print("Client Connected to server",conn)
        print("Number of clients",t.clients)
        pass
    def on_disconnect(self,conn):
        print("Client Disconnected to server",conn)
        pass
    def exposed_test(self):
        return "Poggers"

    def exposed_bar(self,func):
        return func() + "bar"

    exposed_var = 10

    # while True:
    #     x=input("Stall")


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(MasterService(), port=2986)
    t.start()
    