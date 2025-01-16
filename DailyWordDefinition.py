import subprocess
from commonClassesFunctions.functionsClasses_utils import get_exe_path, Depdenencies, RunExe, getBaseDir
import platform
import os

def runProgram():      
    exeFilePath = get_exe_path('LoadingProgramConsole')        
    dep = Depdenencies(platform, getBaseDir, os, subprocess)
    openConsole = True
    RunExe(exeFilePath, dep, openConsole)      

if __name__ == "__main__":    
    runProgram()