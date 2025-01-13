import subprocess
from commonClassesFunctions.functionsClasses_utils import get_exe_path, Depdenencies, RunExe, getBaseDir
import time
import platform
import os

def runProgram():
    print('\nDaily_Word_Definition.exe running')
    time.sleep(1)    
    exeFilePath = get_exe_path('StartStopEditProgram')    
    time.sleep(1)
    print(f'\nRunning this exe using subprocess now:{exeFilePath}')    
    dep = Depdenencies(platform, getBaseDir, os, subprocess)
    RunExe(exeFilePath, dep)  
    print('\nStarting application...')
    time.sleep(1)  

if __name__ == "__main__":    
    runProgram()