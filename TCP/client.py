import socket

HOST, PORT = "127.0.0.1", 7777
data = "this is test data"

    # Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data + "\n"))
    data = sock.recv(1024)
    print data

finally:
    sock.close()
