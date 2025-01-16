from StartStopProgram.startStopProgram_startProgramAPI import startProgram
from StartStopProgram.startStopProgram_stopProgramAPI import stopProgram
from commonClassesFunctions.functionsClasses_utils import PID, get_exe_path, getBaseDir, Depdenencies, RunExe
import subprocess
import time
import platform
import os

def startStopEditProgram():

    print('\nStartStopEditProgram.exe running')
    
    time.sleep(1) 

    pid_loading = PID("LoadingProgram")
        
    # Check if the program is currently running using its PID - the first point of entry is the timing loop code
    pid_timing = PID("TimingLoop") 
    
    print('\nChecking if TimingLoop.exe is running using its PID') 
    if pid_timing.checkIfPIDisRunning(): 
        print("\nPID for TimingLoop.exe is running, so running stopProgram API")  
        time.sleep(1) 
        # Will be an exe in programs
        # Kill loading exe        
        pid_loading.killProgram() # kill loading console when opening API
        stopProgram_YN = stopProgram()
        if stopProgram_YN:
            # Kill timing loop
            pid_timing.killProgram()
            print("\nKilling TimingLoop.exe using its PID")  
            time.sleep(1) 
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
        pid_loading.killProgram() # kill loading console when opening API
        runProgram_YN = startProgram()           
        if runProgram_YN:                  
            exeFilePath = get_exe_path('TimingLoop')
            print(f'\nRunning this exe using subprocess now:{exeFilePath}')
            time.sleep(4)
            dep = Depdenencies(platform, getBaseDir, os, subprocess)
            openConsole = False
            RunExe(exeFilePath, dep, openConsole)

if __name__ == "__main__":    
    startStopEditProgram()