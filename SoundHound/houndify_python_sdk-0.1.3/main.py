#!/usr/bin/env python
import json
import socket
import sys

import houndify
import sys
import alsaaudio as alsa
import audioop as aud
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
    micnum = len(miccards) - 1
    mic = [alsa.PCM(alsa.PCM_CAPTURE, alsa.PCM_NORMAL)]
    mic.append(alsa.PCM(alsa.PCM_CAPTURE, alsa.PCM_NORMAL, miccards[1]))
    mic.append(alsa.PCM(alsa.PCM_CAPTURE, alsa.PCM_NORMAL, miccards[2]))
    #mic = [alsa.PCM(alsa.PCM_CAPTURE, alsa.PCM_NORMAL, miccards[i]) for i in range(micnum)]
    for i in range(micnum):
        mic[i].setchannels(CHANNELS)
        mic[i].setrate(RATE)
        mic[i].setformat(FORMAT)
        mic[i].setperiodsize(FRAMESIZE)

    # Initialize SoundHound here
    # Listener for the mic input
    class MyListener(houndify.HoundListener):
	def onPartialTranscript(self, transcript):
            pass
            #if transcript != "": print "Partial transcript: " + transcript
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


    l = [0 for i in range(micnum)]
    # Main update loop
    running = True
    while running == True:
        data = [0 for i in range(micnum)]
        # Process incoming sound here
        # BUFFER_SIZE = 512
        for i in range(micnum):
            l[i], data[i] = mic[i].read()

        # greedy algorithm which selects most loud sound
        #rms = [aud.rms(data[i],1) for i in range(micnum)]
        #rmssorted = sorted(rms)
        '''
        L = 100
        mxix = [aud.findmax(data[i],L) for i in range(micnum)]
        prms = [aud.rms(data[i][mxix[i]*2:(mxix[i]+L)*2],1) for i in range(micnum)]
        prmssorted = sorted(prms)
        print prmssorted
        '''
        direction = 'UNDEFINED'
        ind = 0
        #if prmssorted[2] - prmssorted[0] > 20:
        maxpp = [aud.maxpp(data[i],1) for i in range(micnum)]
        print maxpp
        maxppsorted = sorted(maxpp)
        if maxppsorted[2] - maxppsorted[1] > 20:
            # possible value of dirscore: 4,5,6,8,9,10
            #dirscore = 4 * prms.index(prmssorted[2]) + 2 * prms.index(prmssorted[1]) +  prms.index(prmssorted[0])
            dirscore = 4 * maxpp.index(maxppsorted[2]) + 2 * maxpp.index(maxppsorted[1]) +  maxpp.index(maxppsorted[0])
            print dirscore
            dictionary = {'0':'UNDEFINED',
                          '1':'UNDEFINED',
                          '2':'UNDEFINED',
                          '3':'UNDEFINED',
                          '4':'LEFT',
                          '5':'BACKLEFT',
                          '6':'FRONTLEFT',
                          '7':'UNDEFINED',
                          '8':'FRONTRIGHT',
                          '9':'BACKRIGHT',
                          '10':'RIGHT',
                          '11':'UNDEFINED',
                          '12':'UNDEFINED',
                          '13':'UNDEFINED',
                          '14':'UNDEFINED'}
            direction = dictionary[str(dirscore)]
            #ind = maxpp.index(maxppsorted[2])
            #i = prms.index(prmssorted[2])
            print ind
            print direction

        # samples = sys.stdin.read(BUFFER_SIZE)
        # finished = [None for i in range(micnum)]
        finished = False
        client.start(MyListener())
        while not finished:
        #while None in finished:
            #finished = [client.fill(data[i]) for i in range(micnum)]
            finished = client.fill(data[ind])
            #for i in range(micnum):
            l[ind], data[ind] = mic[ind].read()
            # samples = sys.stdin.read(BUFFER_SIZE)
            '''if len(data[ind]) == 0:
                print "end?"
                break'''
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
        counter = 1
        category = 'SPEECH'
        intensity = 3.0
        #direction = 'FRONTLEFT'
        content = 'HELLO'

        '''
        try:
            cont = raw_input("Input data to send to server: ")
        except KeyboardInterrupt:
            print("Ctrl+C pressed. Client terminating...")
            running = False
        '''

        data['id'] = ID
        data['cnt'] = counter
        data['cat'] = category
        data['int'] = intensity
        data['cont'] = content
        data['dir'] = direction
        data['isFinal'] = True

        data = json.dumps(data)

        sock.sendall(bytes(data + "\n"))

    # Shutdown network connection
    sock.close()

    # Shutdown SoundHound

    # Shutdown microphone --> no need!

if __name__ == '__main__':
    main(sys.argv[1:])
