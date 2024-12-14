import sys
from StartStopProgram.startStopProgram_startProgramAPI import startProgram
from StartStopProgram.startStopProgram_stopProgramAPI import stopProgram
from commonClassesFunctions.functionsClasses import PID
from RunProgram.runProgram_main import runApplicationTimingLoop

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

if __name__ == "__main__":
    startStopEditProgram()