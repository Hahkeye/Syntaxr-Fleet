from printer import Printer
import time
p = Printer('COM4', 115200)
#print(b'e,\xeb\xe9T\x14J\xb9i\x172\x85iK'.decode())
# test1 = " Last Updated: 2019-10-28 | Author: Ender-5 Pro".encode('utf-8')
# test2 = "Compiled: Oct 28 2019".encode('utf-8')
# test3 = "Free Memory: 10461  PlannerBufferBytes: 1232".encode('utf-8')
# print(test1)
# print(test2)
# print(test3)
# print(test1.decode())
# print(test2.decode())
# print(test3.decode())
# print(test)
p.connect()
time.sleep(4)
p.start("test.gcode")
while True:
    x = input("Enter Command: ")
    p.execute(x)
    
