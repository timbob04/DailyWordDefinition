from StartStopProgram.startStopProgram_startProgramAPI import startProgram
from StartStopProgram.startStopProgram_stopProgramAPI import stopProgram
from commonClassesFunctions.functionsClasses_utils import PID, get_exe_path
# from RunProgram.runProgram_timingLoop import runApplicationTimingLoop
import subprocess
import time

def startStopEditProgram():

    print('\nStartStopEditProgram.exe running')
    
    time.sleep(1) 
    
    # Check if the program is currently running using its PID - the first point of entry is the timing loop code
    pid_timing = PID("TimingLoop") 
    
    print('\nChecking if TimingLoop.exe is running using its PID') 
    if pid_timing.checkIfPIDisRunning(): 
        print("\nPID for TimingLoop.exe is running, so running stopProgram API")  
        time.sleep(1) 
        # Will be an exe in programs
        stopProgram_YN = stopProgram()
        if stopProgram_YN:
            # Kill timing loop
            pid_timing.killProgram()
            print("\nKilling TimingLoop.exe using its PID")  
            time.sleep(1) 
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
            exeFilePath = get_exe_path('TimingLoop')
            print(f'\nRunning this exe using subprocess now:{exeFilePath}')
            time.sleep(4)
            subprocess.Popen([exeFilePath], creationflags=subprocess.CREATE_NEW_CONSOLE)
            # runApplicationTimingLoop() # Before installation

if __name__ == "__main__":    
    startStopEditProgram()