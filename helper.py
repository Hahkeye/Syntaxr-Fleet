import os,time, threading, server


def menu(clients, free):
    # print("\nNumber of threads: ",threading.activeCount())
    # print("Threads: ",threading.enumerate(),"\n")
    print("Clients")
    print("----------------------------")
    if len(clients)==0: print("none")
    else:
        for c in clients:
            print(clients.index(c)+1,": ",c.string())
    print("----------------------------\n")
    print("Free Clients")
    print("----------------------------")
    if len(free)==0: print("none")
    else:
        for f in free:
            print(f.string())
    #print(free)
    print("----------------------------\n")
    b = set(clients) - set(free)
    print("Busy Clients")
    print("----------------------------")
    if len(b)==0: print("none")
    else:
        for be in b:
            print(be.string())
    print("\nOptions:\n")
    print("Select: 1")
    print("Disconnect: 2")
    #print("Get Free Printers: 3")]
