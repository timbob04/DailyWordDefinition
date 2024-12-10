import sys
from StartStopProgram.startProgram_generateAPI import startProgram
from StartStopProgram.stopProgram_generateAPI import stopProgram
from commonClassesFunctions.functionsClasses import PID
from PresentWordsAndDefinitions.presentWords_runProgram import runApplicationTimingLoop

def startStopEditProgram():

    # Check if the program is currently running using its PID
    pid = PID()
    PIDrunning = pid.checkIfPIDisRunning()

    if PIDrunning:                
        stopProgram_YN = stopProgram()
        if stopProgram_YN:
            pid.killProgram()
            sys.exit()        
    else:                
        runProgram_YN = startProgram()           
        if runProgram_YN:            
            runApplicationTimingLoop()

startStopEditProgram()

