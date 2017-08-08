import pylab
import pyaudio
import struct
import sys
import numpy as np
import wave
import pygame
import scipy
from myfunctions import clip16

list5 =[]


def time_scale(List1,List2):

    print ('c')
    
    leng = len(List1)

    output_all1 = ''            # output signal in all (string)
    for k in range (0,leng):
        signalin=0
        N = 2048
        H = N/4
        #print k
        wavfile = List1[k]+'.wav'
        print wavfile
        tscale = int(List2[k])

        wf = wave.open( wavfile, 'rb')
        RATE = wf.getframerate()
        WIDTH = wf.getsampwidth()

        signalin  = wf.getnframes()
        #(sr,signalin) = wavfile.readframes(sys.argv[2])

        L = signalin
        #print L

        phi  = pylab.zeros(N)
        out = pylab.zeros(N, dtype=complex)
        out1 = pylab.zeros(N, dtype=complex)
        outresult = pylab.zeros(N, dtype=complex)
        sigout = pylab.zeros(L/tscale+N, dtype = complex)
        sigout1 = pylab.zeros(L/tscale+N, dtype = complex)
        sigout2 = pylab.zeros(L/tscale+N, dtype = complex)
        input_string = wf.readframes(L)
        print len(input_string)
        input_value1 = struct.unpack('h' * L, input_string)


        # max input amp, window
        amp = max(input_value1)
        win = pylab.hanning(N)
        p = 0
        pp = 0



        p1 = pyaudio.PyAudio()
        stream = p1.open(format = p1.get_format_from_width(WIDTH),
                        channels = 1,
                        rate = RATE,
                        input = False,
                        output = True)
        output_all = ''            # output signal in all (string)
        

        while p < L-(N+H):
            #print N
            # take the spectra of two consecutive windows
            p1 = int(p)

            
            #win = list(win)
            #print input_value[p1:p1+N]
            input_value = np.asarray(input_value1)
            
            #print input_value
            
            spec1 =  np.fft.fft(win*input_value[p1:p1+N])
            spec2 =  np.fft.fft(win*input_value[p1+H:p1+N+H])
            spec3 = abs(spec2)


            
            # take their phase difference and integrate

            #phi += (angle(spec2) - angle(spec1))
            phi = (phi + np.angle(spec2/spec1)) % 2 * (np.pi)
            out = np.fft.ifft(spec3*np.exp(1j*phi))
            
            
            for i in range(0,N):
                out.real[i] = clip16(out.real[i])
            
            
            B = len(sigout)

            output_string = struct.pack('h' * N, *(out.real))
           

            pp += H
            p += H*tscale

#print('* D')

            # Write output value to audio stream
            #stream.write(output_string)
            output_all1 = output_all1 + output_string
        
        #stream.write(output_all)
        list5.append(output_all1)


#stream.write(output_all1)



#output_all1 = output_all + output_all1
#stream.write(output_all1)
# print('* Done')
    
    stream.stop_stream()
    stream.close()
    #p1.terminate()
    output_wavefile = 'lala.wav'
    
    print 'Writing to wave file', output_wavefile

    
    wf = wave.open(output_wavefile, 'w')      # wave file
#print('* hip')
    wf.setnchannels(1)      # one channel (mono)
    wf.setsampwidth(2)      # two bytes per sample
    wf.setframerate(RATE)   # samples per second
    #print('* hop')
    wf.writeframes(output_all1)
    
    wf.close()
    return output_wavefile
    
    print('* Done')
