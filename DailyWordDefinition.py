import subprocess
from commonClassesFunctions.functionsClasses_utils import get_exe_path
import time

def runProgram():
    print('\nDaily_Word_Definition.exe running')
    time.sleep(1)
    # curPath = os.path.join('bin','StartStopEditProgram')
    exeFilePath = get_exe_path('StartStopEditProgram')
    print(f'\nRunning this exe using subprocess now:{exeFilePath}')
    time.sleep(1)
    # subprocess.run([exeFilePath], shell=True, stdin=None, stdout=None, stderr=None)
    subprocess.Popen([exeFilePath], creationflags=subprocess.CREATE_NEW_CONSOLE)

if __name__ == "__main__":    
    runProgram()