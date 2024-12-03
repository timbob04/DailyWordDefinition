# This script will be the basis for the main exe file.
# It will check to see if the program is already running or not, and then bring up the relevant API (Start or Stop program)
# To check, I can use the binary boolean file, and also the psutil library to check to see if an exe file is currently running or not - do both to be sure

import sys
from StartStopProgram.startProgram import startProgram
from StartStopProgram.stopProgram import stopProgram
from commonClassesFunctions.functionsClasses import getPIDfilePath, checkIfPIDisRunning
from PresentWordsAndDefinitions.presentWords_runProgram import runApplicationTimingLoop

def startStopEditProgram():

    PIDname  = getPIDfilePath()

    PIDrunning = checkIfPIDisRunning(PIDname)

    if PIDrunning:                
        stopProgram_YN = stopProgram()
        if stopProgram_YN:
            sys.exit()        
    else:                
        runProgram_YN = startProgram()           
        if runProgram_YN:            
            runApplicationTimingLoop()

startStopEditProgram()

