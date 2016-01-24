#!/usr/bin/env python
import houndify
import sys
import alsaaudio
import audioop
import time


BUFFER_SIZE = 1024
CHANNEL = 1
RATE = 16000

if __name__ == '__main__':


    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)
    inp.setchannels(1)
    inp.setrate(16000)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp.setperiodsize(BUFFER_SIZE)

#    inp1 = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, 'hw:0,0')
#    inp1.setchannels(1)
#    inp1.setrate(RATE)
#    inp1.setformat(alsaaudio.PCM_FORMAT_S16_LE)
#    inp1.setperiodsize(BUFFER_SIZE)

    inp2 = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, 'hw:1,0')
    inp2.setchannels(1)
    inp2.setrate(RATE)
    inp2.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp2.setperiodsize(BUFFER_SIZE)

    inp3 = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, 'hw:2,0')
    inp3.setchannels(1)
    inp3.setrate(RATE)
    inp3.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp3.setperiodsize(BUFFER_SIZE)

    print(alsaaudio.cards())
    if len(sys.argv) == 4:
	print "Usage: %s <CLIENT_KEY> <CLIENT_ID>" % sys.argv[0]
	sys.exit(0)

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
#    client.start(MyListener())
    while True:
        print i
        i += 1
        l, data = inp.read()
#        l1, data1 = inp1.read()
        l2, data2 = inp2.read()
        l3, data3 = inp3.read()
#        print("Read %u %u %u bytes" % (l, l2, l3))
	    #samples = sys.stdin.read(BUFFER_SIZE)
	finished = False
	client.start(MyListener())

        volRep1 = audioop.max(data,1)
        volRep2 = audioop.max(data2,1)
        volRep3 = audioop.max(data3,1)

        if max(volRep1, volRep2, volRep3) == volRep1:
#            data = data1
            mode = 'mic0'
            print "mic1!!!"
        elif max(volRep1, volRep2, volRep3) == volRep2:
#            data = data2
            mode = 'mic1'
            print "mic2!!!"
        else:
#            data = data3
            mode = 'mic2'
            print "mic3!!!"

	while not finished:
            finished = client.fill(data)
#            if mode == 'mic0':
#                finished = client.fill(data1)
#                l1, data1 = inp1.read()
#                if len(data1) == 0: break
#            elif mode == 'mic1':
#                finished = client.fill(data2)
#                l2, data2 = inp2.read()
#                if len(data2) == 0: break
#            elif mode == 'mic2':
#                finished = client.fill(data3)
#                l3, data3 = inp3.read()
#                if len(data3) == 0: break
            l, data = inp.read()
            # samples = sys.stdin.read(BUFFER_SIZE)
	    if len(data) == 0:
                break
        client.finish()
        #volRep1 = None
        #volRep2 = None
        #volRep3 = None
        time.sleep(0.5)
