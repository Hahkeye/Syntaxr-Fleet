import os,time

class cli(object):
    OFFSET = 1

    def __init__(self,id=0,soc=None):
        self.id=id
        self.soc=soc





def menu(clients):
    print("Clients")
    print("----------------------------")
    if len(clients)==0: print("none")
    else:
        for c in clients:
            print(c)
    print("----------------------------")
    print("Options:\n")
    print("Select: 1")
    print("Disconnect: 2")
    print("Get Free Printers: 3")