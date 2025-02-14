import subprocess
from commonClassesFunctions.utils import get_exe_path, Depdenencies, RunExe, getBaseDir, PID
import platform
import os
import time
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "_internal"))


def loadingProgam():   
    
    pid_startStop = PID("StartStopEditProgram")
    if pid_startStop.checkIfPIDisRunning():
        print('\nThe application is already open.')        
        time.sleep(3)
        print('\nAborting this attempt to open the application.')
        time.sleep(2)
    else:
        pid = PID("LoadingProgramConsole")
        pid.createPID()
        print('\nLoading program', end="")  
        # Run exe for StartStopEditProgram
        exeFilePath = get_exe_path('StartStopEditProgram')        
        dep = Depdenencies(platform, getBaseDir, os, subprocess)
        openConsole = False
        RunExe(exeFilePath, dep, openConsole)
        # Start loading dots while exe above is loading
        for _ in range(120): 
            print(".", end="", flush=True)
            time.sleep(1)  

if __name__ == "__main__":
    loadingProgam()