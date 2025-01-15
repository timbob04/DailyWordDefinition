import subprocess
from commonClassesFunctions.functionsClasses_utils import get_exe_path, Depdenencies, RunExe, getBaseDir
import time
import platform
import os

def runProgram():
    print('\nLoading program now ', end="")    
    exeFilePath = get_exe_path('StartStopEditProgram')        
    dep = Depdenencies(platform, getBaseDir, os, subprocess)
    RunExe(exeFilePath, dep)  
    for i in range(3):
        print(". ", end="", flush=True)
        time.sleep(1)  

if __name__ == "__main__":    
    runProgram()