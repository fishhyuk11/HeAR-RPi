#!/usr/bin/env python
import json
import socket
import sys

import houndify
import sys
import alsaaudio as alsa
import audioop
import time

HOST, PORT = "127.0.0.1", 7777

# Constants used for mic input
CHANNELS = 1
RATE = 16000
FORMAT = alsa.PCM_FORMAT_S16_LE
FRAMESIZE = 1024

# Soundhound's client info
CLIENT_KEY = 'arunIHMyBqoARiGLn-sbdxuZNRRqBlafShVkTIDi6WNf7q0t-AsQAtWog8iga92FI99z8IuA6OUJxC1OUCNc-A=='
CLIENT_ID = 'LdOQEtUzBrsZRMt4fEDnLw=='

def main(argv):
    if len(argv) < 1:
        print('main.py <server ip address>')
        sys.exit(2)
    else:
        HOST = argv[0]

    # Initialize microphone here
    miccards = alsa.cards()
    micnum = len(miccards)
    mic = [alsa.PCM(alsa.PCM_CAPTURE,alsa.PCM_NORMAL,cards[i]) for i in range(micnum)]
    for i in range(micnum):
        mic[i].setchannels(CHANNELS)
        mic[i].setrate(RATE)
        mic[i].setformat(FORMAT)
        mic[i].setperiodsize(FRAMESIZE)

    # Initialize SoundHound here
    # Listener for the mic input
    class MyListener(houndify.HoundListener):
        def onPartialTranscript(self, transcript):
            if transcript != "":
                print "Partial transcript: " + transcript
        def onFinalResponse(self, response):
            responseStr = str(response)
            splitString = responseStr.split("'")
            for i in range(len(splitString)):
                if splitString[i] == 'Transcription':
                    print "Final response:" + splitString[i+2]
                    # print "Final response: " + str(response)  
        def onTranslatedResponse(self, response):
                    print "Translated response: " + response
        def onError(self, err):
                    print "ERROR"

    client = houndify.StreamingHoundClient(CLIENT_KEY, CLIENT_ID)
    ## Pretend we're at SoundHound HQ.  Set other fields as appropriate
    client.setLocation(37.388309, -121.973968)

    # Initialize network connection here
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket (SOCK_STREAM means a TCP socket)
    try:
        sock.connect((HOST, PORT))
    except socket.error, msg:
        print("Could not connect to server! Error: %s" % msg)
        sys.exit(-1)

    # Main update loop
    running = True
    while running == True:
        # Process incoming sound here
        # BUFFER_SIZE = 512
        l = [0 for i in range(micnum)]
        data = [0 for i in range(micnum)]
        for i in range(micnum):
            l[i], data[i] = [mic[i].read() for i in range(micnum)]

        # samples = sys.stdin.read(BUFFER_SIZE)
        finished = [False for i in range(micnum)]
        client.start(MyListener())
        while not finished:
            finished = [client.fill(data[i]) for i in range(micnum)]
        for i in range(micnum):
            l[i], data[i] = [mic[i].read() for i in range(micnum)]
        # samples = sys.stdin.read(BUFFER_SIZE)
        if len(data[0]) == 0:
            break
        client.finish()
        # time.sleep(0.5)

        # Send the result to iPhone
        '''
        Wrap processed data as json
            id: message id
            cnt: packet counter
            cat: category of sound
            int: intensity of sound
            cont: content of a sound
            dir: direction of the sound
            isFinal: a boolean terminal indicator
        '''
        # A container for processed data
        data = {}

        # Temporary test data
        ID = 1
        cnt = 1
        cat = 'SPEECH'
        inte = 3.0
        direc = 'FRONTLEFT'

        try:
            cont = raw_input("Input data to send to server: ")
        except KeyboardInterrupt:
            print("Ctrl+C pressed. Client terminating...")
            running = False

        data['id'] = ID
        data['cnt'] = cnt
        data['cat'] = cat
        data['int'] = inte
        data['cont'] = cont
        data['dir'] = direc
        data['isFinal'] = True

        data = json.dumps(data)

        sock.sendall(bytes(data + "\n"))

    # Shutdown network connection
    sock.close()

    # Shutdown SoundHound

    # Shutdown microphone --> no need!

if __name__ == '__main__':
    main(sys.argv[1:])
