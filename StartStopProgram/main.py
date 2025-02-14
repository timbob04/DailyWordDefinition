from StartStopProgram.API_startProgram import startProgram
from StartStopProgram.API_stopProgram import stopProgram
from StartStopProgram.utils import clearDateLastRunFromTextFile
from commonClassesFunctions.utils import PID, get_exe_path, getBaseDir, Depdenencies, RunExe
import subprocess
import time
import platform
import os
import sys
import subprocess
from commonClassesFunctions.utils import get_exe_path, Depdenencies, RunExe, getBaseDir
import platform
import os
import time
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "_internal"))

def runProgram():      
    exeFilePath = get_exe_path('LoadingProgramConsole')        
    dep = Depdenencies(platform, getBaseDir, os, subprocess)
    openConsole = True
    RunExe(exeFilePath, dep, openConsole)    

    time.sleep(10)  

if __name__ == "__main__":    
    runProgram()

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
            dep = Depdenencies(platform, getBaseDir, os, subprocess)
            # Run the console message to inform the user that the program is running in the background
            exeFilePath = get_exe_path('StartingProgramConsole')
            print(f'\nRunning this exe using subprocess now:{exeFilePath}')                        
            openConsole = True
            RunExe(exeFilePath, dep, openConsole)
            time.sleep(12)
            # Clear the date last run from the text file, so it can run again if alredy run today
            clearDateLastRunFromTextFile()
            time.sleep(1)
            # Run the main timing loop, i.e., the main program in the background
            exeFilePath = get_exe_path('TimingLoop')
            print(f'\nRunning this exe using subprocess now:{exeFilePath}')                        
            openConsole = False
            RunExe(exeFilePath, dep, openConsole)

    time.sleep(2)
    pid_startStop.cleanUpPID()

if __name__ == "__main__":    
    startStopEditProgram()