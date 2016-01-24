from bluetooth import *
import BTaddr

bd_addr = BTaddr.iPhone6SP
try:
    sock = BluetoothSocket(RFCOMM)
    sock.connect((bd_addr, port)) # Parentheses!
    print("Initial connection")
    conn = 1
except  BluetoothError as bt:
    print('Cannot connect to host' + str(bt))
    exit(0)

