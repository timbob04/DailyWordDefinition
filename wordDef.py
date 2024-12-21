import os
from StartStopProgram.startStopProgram_startProgramAPI import startProgram
from StartStopProgram.startStopProgram_stopProgramAPI import stopProgram
from commonClassesFunctions.functionsClasses import PID, get_exe_path
from RunProgram.runProgram_timingLoop import runApplicationTimingLoop
import subprocess

def startStopEditProgram():

    # Check if the program is currently running using its PID - the first point of entry is the timing loop code
    pid_timing = PID("TimingLoop")    
    
    if pid_timing.checkIfPIDisRunning():    
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
            path = os.path.join('bin','TimingLoop')       
            exeFilePath = get_exe_path(path)
            subprocess.run([exeFilePath], capture_output=True, text=True)
            # runApplicationTimingLoop() # Before installation

if __name__ == "__main__":
    startStopEditProgram()