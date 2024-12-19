import sys
from StartStopProgram.startStopProgram_startProgramAPI import startProgram
from StartStopProgram.startStopProgram_stopProgramAPI import stopProgram
from StartStopProgram.startStopProgram_functionsClasses import get_exe_path
from commonClassesFunctions.functionsClasses import PID
# from RunProgram.runProgram_main import runApplicationTimingLoop
import subprocess

def startStopEditProgram():

    # Check if the program is currently running using its PID
    pid_timing = PID("TimingLoop")
    PIDrunning = pid_timing.checkIfPIDisRunning()
    
    if PIDrunning:    
        # Will be an exe in programs            
        stopProgram_YN = stopProgram()
        if stopProgram_YN:
            # Kill timing loop
            pid_timing.killProgram()
            # Kill any instances of the main API to present words and definitions
            pid_runProgram = PID("PresentWordsAndDefinitions")
            if pid_runProgram.checkIfPIDisRunning():
                pid_runProgram.killProgram() 
    else:                
        runProgram_YN = startProgram()           
        if runProgram_YN:            
            exeFilePath = get_exe_path('Background')
            subprocess.run([exeFilePath], capture_output=True, text=True)
            # runApplicationTimingLoop() # Before installation

if __name__ == "__main__":
    startStopEditProgram()