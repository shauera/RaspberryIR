
import RPi.GPIO as GPIO
import math
import os
import pigpio
from datetime import datetime
from time import sleep

# This is for revision 1 of the Raspberry Pi, Model B
# This pin is also referred to as GPIO23
INPUT_WIRE = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(INPUT_WIRE, GPIO.IN, pull_up_down = GPIO.PUD_UP)

try:
    print ("---------- Waiting for input ----------")
    while True:
        value = 1
        # Loop until we read a 0
        while value:
            value = GPIO.input(INPUT_WIRE)

        # Grab the start time of the command
        startTime = datetime.now()

        # Used to buffer the command pulses
        command = []

        # The end of the "command" happens when we read more than
        # a certain number of 1s (1 is off for my IR receiver)
        numOnes = 0

        # Used to keep track of transitions from 1 to 0
        previousVal = 0
        while True:
            if value != previousVal:
                # The value has changed, so calculate the length of this run
                now = datetime.now()
                pulseLength = now - startTime
                if pulseLength.microseconds < 250:
                    command = []
                    break
                startTime = now
                command.append((previousVal, pulseLength.microseconds))

            if value:
                numOnes = numOnes + 1
            else:
                numOnes = 0

            # 10000 is arbitrary, adjust as necessary
            if numOnes > 10000:
                break

            previousVal = value
            value = GPIO.input(INPUT_WIRE)

        if len(command) > 0:
            print ("----------Start----------")
            for (val, pulse) in command:
                print (val, pulse)

            binaryString = "".join(map(lambda x: "1" if x[1] > 1000 else "0", filter(lambda x: x[0]==1, command))) 
            print(binaryString)
            print ("-----------End-----------")

            print ("Size of array is: " + str(len(command)))

except KeyboardInterrupt:  
    # exits when CTRL+C was pressed
    print ("/nuser terminatd")

except:
    print ("some error happened")

finally:  
    GPIO.cleanup() # this ensures a clean exit
    print ("---------- Exited ----------")


#1|10001000|01011011|11100100|00000000|00000000|10011100|00001100|00000000|00001110|00000000|00000000|01100000|00000110|00000000|00000000|10000011|00000001|00000000|01001001
#1|10001000|01011011|11100100|00000000|00000000|00011100|00001100|00000000|00001110|00000000|00000000|01100000|00000110|00000000|00000000|10000011|00000001|00000000|10001001
#1|10001000|01011011|11100100|00000000|00000000|00011100|00101100|00000000|00001110|00000000|00000000|01100000|00000110|00000000|00000000|10000011|00000001|00000000|10101001
#1|10001000|01011011|11100100|00000000|00000000|00011100|01001100|00000000|00001110|00000000|00000000|01100000|00000110|00000000|00000000|10000011|00000001|00000000|11001001
#1|10001000|01011011|11100100|00000000|00000000|10011100|00101100|00000000|00001110|00000000|00000000|01100000|00000110|00000000|00000000|10000011|00000001|00000000|01101001



