
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
    wave_500=[pigpio.pulse(1<<G1, 0, 500000), pigpio.pulse(0, 1<<G1, 500000)]

    OutputCode.extend(wave_500)

    pi.wave_clear()
    pi.wave_add_generic(OutputCode)
    outputWave = pi.wave_create() # create and save id

    pi.wave_send_repeat(outputWave)
    sleep(10)    
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

