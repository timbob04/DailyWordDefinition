import subprocess
from commonClassesFunctions.functionsClasses_utils import get_exe_path, Depdenencies, RunExe, getBaseDir, PID
import platform
import os
import time

def loadingProgam():   

    pid = PID("LoadingProgram")

    if not pid.checkIfPIDisRunning():        
        print('\nLoading program', end="")  
        pid.createPID()
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