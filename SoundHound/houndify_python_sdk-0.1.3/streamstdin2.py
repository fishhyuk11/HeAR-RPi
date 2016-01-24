#!/usr/bin/env python

import houndify
import sys
import alsaaudio
import audioop
import time

CHANNELS = 1
RATE = 16000
FORMAT = alsaaudio.PCM_FORMAT_S16_LE
FRAMESIZE = 1024

if __name__ == '__main__':

    inp = alsaaudio.PCM(type=alsaaudio.PCM_CAPTURE,mode=alsaaudio.PCM_NORMAL)
    inp.setchannels(CHANNELS)
    inp.setrate(RATE)
    inp.setformat(FORMAT)
    inp.setperiodsize(FRAMESIZE)

    #mix = alsaaudio.Mixer(control='Mic',id=0,cardindex=0)
    #print mix.getvolume()
    #mix.setvolume(50)

    print(alsaaudio.cards())

    '''
    if len(sys.argv) == 4:
	print "Usage: %s <CLIENT_KEY> <CLIENT_ID>" % sys.argv[0]
	sys.exit(0)
    '''

#   CLIENT_KEY = sys.argv[1]
#   CLIENT_ID = sys.argv[2]
    CLIENT_KEY = 'arunIHMyBqoARiGLn-sbdxuZNRRqBlafShVkTIDi6WNf7q0t-AsQAtWog8iga92FI99z8IuA6OUJxC1OUCNc-A=='
    CLIENT_ID = 'LdOQEtUzBrsZRMt4fEDnLw=='
    #
    # Simplest HoundListener; just print out what we receive.
    #
    # You can use these callbacks to interact with your UI.
    #
    class MyListener(houndify.HoundListener):
	def onPartialTranscript(self, transcript):
            print "Partial transcript: " + transcript
	def onFinalResponse(self, response):
            responseStr = str(response)
            splitString = response.split("'")
            for i in range(len(splitString)):
                if splitString[i] == 'Transcript':
                    print splitString[i+2]
		#print "Final response: " + str(response)
	def onTranslatedResponse(self, response):
            print "Translated response: " + response
	def onError(self, err):
            print "ERROR"
    client = houndify.StreamingHoundClient(CLIENT_KEY, CLIENT_ID)
    ## Pretend we're at SoundHound HQ.  Set other fields as appropriate
    client.setLocation(37.388309, -121.973968)
    for i in range(5):
        print i
#	BUFFER_SIZE = 512
        l, data = inp.read()
	# samples = sys.stdin.read(BUFFER_SIZE)
	finished = False
	client.start(MyListener())
	while not finished:
            finished = client.fill(data)
            l, data = inp.read()
            # samples = sys.stdin.read(BUFFER_SIZE)
            if len(data) == 0:
                break
	client.finish()
        #time.sleep(0.5)
