
import RPi.GPIO as GPIO
import math
import os
import pigpio
from datetime import datetime
from time import sleep

try:
    G1 = 17
    pi = pigpio.pi()       # pi1 accesses the local Pi's GPIO
    pi.set_mode(G1, pigpio.OUTPUT) # GPIO 17 as output    
    OutputCode=[] # flash every 500 ms
    LeadingPulse=[pigpio.pulse(1<<G1, 0, 3500), pigpio.pulse(0, 1<<G1, 1688)]
    OnePulse=    [pigpio.pulse(1<<G1, 0, 480), pigpio.pulse(0, 1<<G1, 1260)]
    ZeroPulse=   [pigpio.pulse(1<<G1, 0, 480), pigpio.pulse(0, 1<<G1, 380)]

    OutputCode.extend(LeadingPulse)
    code = "110001000010110111110010000000000000000000001110000001100000000000000111000000000000000000110000000000110000000000000000010000011000000010000000010001001"
    code2 =  "11100000111000000100000010111111"
    code1 = "11100000111000000110011110011000"
    for digit in code:
        if digit == "0":
            OutputCode.extend(ZeroPulse)
        else:
            OutputCode.extend(OnePulse)

    for pulse in OutputCode:
        print (pulse.delay)

    pi.wave_clear()
    pi.wave_add_generic(OutputCode)
    outputWave = pi.wave_create() # create and save id

    pi.wave_send_once(outputWave)
    sleep(3)    
    pi.wave_tx_stop() # stop waveform
    pi.wave_clear() # clear all waveforms

except KeyboardInterrupt:  
    # exits when CTRL+C was pressed
    print ("/nuser terminatd")

except:
    print ("some error happened")

finally:  
    GPIO.cleanup() # this ensures a clean exit
    pi.write(G1, 0)
    pi.stop()
    print ("---------- Exited ----------")

#1 11100000 11100000 01000000 1011111
#1 11100000 11100000 01000000 1011111
