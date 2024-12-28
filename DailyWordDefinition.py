import os
import subprocess
from commonClassesFunctions.functionsClasses import get_exe_path, setPyQt5path

def runProgram():
    print('Running main program - starter duck')
    curPath = os.path.join('bin','StartStopEditProgram')
    exeFilePath = get_exe_path(curPath)
    print(f'\nThe path of the startStopEdit.exe is\n{exeFilePath}')
    subprocess.run([exeFilePath], shell=True, stdin=None, stdout=None, stderr=None)

if __name__ == "__main__":
    setPyQt5path()
    runProgram()