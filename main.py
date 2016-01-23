#!/usr/bin/env python
import socket

HOST, PORT = "127.0.0.1", 7777

def main():
    # Initialize microphone here

    # Initialize SoundHound here

    # Initialize network connection here
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket (SOCK_STREAM means a TCP socket)
    try:
        sock.connect((HOST, PORT))
    except:
        print("Could not connect to server!")
        exit(-1)

    # Main update loop
    running = True
    while running == True:
        # Process incoming sound here

        # Send the result to iPhone
        data = "this is test data"

        try:
            data = raw_input("Input data to send to server: ")
        except KeyboardInterrupt:
            print("Ctrl+C pressed. Client terminating...")
            running = False

        sock.sendall(bytes(data + "\n"))
    
    # Shutdown network connection
    sock.close()

    # Shutdown SoundHound

    # Shutdown microphone

if __name__ == '__main__':
    main()
