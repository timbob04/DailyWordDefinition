import time
from RunProgram.runProgram_timingControl import TimingControl
from commonClassesFunctions.functionsClasses_utils import PID, get_exe_path, getBaseDir, Depdenencies, RunExe
import subprocess
import os
import platform

def runApplicationTimingLoop():

    print('\nTimingLoop.exe running')

    # For checking when the API should be presented
    timingControl = TimingControl()
    
    # Make PID to indicate that this code's timing loop is running
    pid_time = PID("TimingLoop")
    pid_time.createPID()
    print("\nCreating PID for TimingLoop.exe (this exe).")
    time.sleep(1)
        
    while True:  
        print('Timing loop looping ...')                  
        if timingControl.checkIfTimeToRunProgram():            
            print('\nTime reached to run WordDefAPI')     
            time.sleep(1)
            # Close any previous instances of main API to show words/definitions
            pid_wordDefAPI = PID("WordDefAPI")
            print("\nChecking if a previou instance of WordDefAPI.exe is runnnig using its PID.")                         
            if pid_wordDefAPI.checkIfPIDisRunning():
                print("\nKilling previous instances on WordDefAPI.exe")
                time.sleep(1)
                pid_wordDefAPI.killProgram()
            # Make API to show today's word and definition
            exeFilePath = get_exe_path('WordDefAPI')
            print(f'\nRunning this exe using subprocess now:{exeFilePath}\n')
            time.sleep(1)
            dep = Depdenencies(platform, getBaseDir, os, subprocess)
            openConsole = False
            RunExe(exeFilePath, dep, openConsole)
    
            # getAndMakeAPIcontent()         
        time.sleep(5)

# Run the main function if this script is executed directly
if __name__ == "__main__":    
    runApplicationTimingLoop()