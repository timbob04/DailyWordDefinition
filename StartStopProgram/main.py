from StartStopProgram.API_startProgram import startProgram
from StartStopProgram.API_stopProgram import stopProgram
from commonClassesFunctions.utils import PID, get_exe_path, getBaseDir, Depdenencies, RunExe
import subprocess
import time
import platform
import os

def startStopEditProgram():

    print('\nStartStopEditProgram.exe running')
    pid_startStop = PID("StartStopEditProgram")
    pid_startStop.createPID()
                    
    # Check if the program is currently running using its PID - the first point of entry is the timing loop code
    pid_timing = PID("TimingLoop") 

    time.sleep(2)   
    pid_loading = PID("LoadingProgramConsole") 
    pid_loading.killProgram()
    pid_loading.cleanUpPID()
    
    print('\nChecking if TimingLoop.exe is running using its PID') 
    if pid_timing.checkIfPIDisRunning(): 
        print("\nPID for TimingLoop.exe is running, so running stopProgram API")                  
        stopProgram_YN = stopProgram()
        if stopProgram_YN:
            # Kill timing loop
            pid_timing.killProgram()
            print("\nKilling TimingLoop.exe using its PID")              
            # Kill any instances of the main API to present words and definitions
            pid_runProgram = PID("WordDefAPI")            
            if pid_runProgram.checkIfPIDisRunning():
                print("\nPID for WordDefAPI.exe is running, so killing it using its PID.")
                time.sleep(1)
                pid_runProgram.killProgram()                 
                time.sleep(1)
    else:                
        print("\nPID for TimingLoop.exe is not running, so starting up startProgram API")
        time.sleep(1)
        runProgram_YN = startProgram()           
        if runProgram_YN:                  
            exeFilePath = get_exe_path('TimingLoop')
            print(f'\nRunning this exe using subprocess now:{exeFilePath}')
            time.sleep(4)
            dep = Depdenencies(platform, getBaseDir, os, subprocess)
            openConsole = False
            RunExe(exeFilePath, dep, openConsole)

    time.sleep(2)
    pid_startStop.cleanUpPID()

if __name__ == "__main__":    
    startStopEditProgram()