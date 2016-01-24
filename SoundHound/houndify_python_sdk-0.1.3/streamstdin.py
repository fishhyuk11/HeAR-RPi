#!/usr/bin/env python
import houndify
import sys
import alsaaudio
import audioop
import time

if __name__ == '__main__':

    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL,'Device')
    inp.setchannels(1)
    inp.setrate(16000)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp.setperiodsize(2048)

        inp1 = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL,'Device')
        inp1.setchannels(1)
        inp1.setrate(16000)
        inp1.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        inp1.setperiodsize(2048)

        inp2 = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, 'Device_1')
        inp2.setchannels(1)
        inp2.setrate(16000)
        inp2.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        inp2.setperiodsize(2048)

        inp3 = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, 'Device_2')
        inp3.setchannels(1)
        inp3.setrate(16000)
        inp3.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        inp3.setperiodsize(2048)

        print(alsaaudio.cards())
	if len(sys.argv) == 4:
		print "Usage: %s <CLIENT_KEY> <CLIENT_ID>" % sys.argv[0]
		sys.exit(0)


#	CLIENT_KEY = sys.argv[1]
#	CLIENT_ID = sys.argv[2]
	CLIENT_KEY = 'arunIHMyBqoARiGLn-sbdxuZNRRqBlafShVkTIDi6WNf7q0t-AsQAtWog8iga92FI99z8IuA6OUJxC1OUCNc-A=='
	CLIENT_ID = 'LdOQEtUzBrsZRMt4fEDnLw=='
	#
	# Simplest HoundListener; just print out what we receive.
	#
	# You can use these callbacks to interact with your UI.
	#
	class MyListener(houndify.HoundListener):
		def onPartialTranscript(self, transcript):
            if transcript != "": print "Partial transcript: " + transcript
		def onFinalResponse(self, response):
            responseStr = str(response)
            splitString = responseStr.split("'")
            for i in range(len(splitString)):
                if splitString[i] == 'Transcription':
                    print "Final response:" + splitString[i+2]
        		    #print "Final response: " + str(response)
		def onTranslatedResponse(self, response):
		    print "Translated response: " + response
		def onError(self, err):
		    print "ERROR"

    client = houndify.StreamingHoundClient(CLIENT_KEY, CLIENT_ID)
	## Pretend we're at SoundHound HQ.  Set other fields as appropriate
        client.setLocation(37.388309, -121.973968)
        i = 0
        while True:
            print i
            i += 1
#	    BUFFER_SIZE = 512
            l, data = inp.read()
	    #samples = sys.stdin.read(BUFFER_SIZE)
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
