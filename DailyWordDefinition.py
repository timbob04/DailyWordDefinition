import subprocess
from commonClassesFunctions.utils import get_exe_path, Depdenencies, RunExe, getBaseDir
import platform
import os
import time

def runProgram():      
    exeFilePath = get_exe_path('LoadingProgramConsole')        
    dep = Depdenencies(platform, getBaseDir, os, subprocess)
    openConsole = True
    RunExe(exeFilePath, dep, openConsole)    

    time.sleep(10)  

if __name__ == "__main__":    
    runProgram()