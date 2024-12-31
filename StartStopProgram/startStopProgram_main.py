from StartStopProgram.startStopProgram_startProgramAPI import startProgram
from StartStopProgram.startStopProgram_stopProgramAPI import stopProgram
from commonClassesFunctions.functionsClasses import PID, get_exe_path, setPyQt5path
# from RunProgram.runProgram_timingLoop import runApplicationTimingLoop
import subprocess
import time

def startStopEditProgram():

    print('\nStartStopEditProgram.exe is running\n')
    time.sleep(1.5) 
    
    # Check if the program is currently running using its PID - the first point of entry is the timing loop code
    pid_timing = PID("TimingLoop") 
    print('\nGetting PID for TimingLoop.exe') 
    
    if pid_timing.checkIfPIDisRunning(): 
        print("\nPID for TimingLoop.exe is running.  So running stopProgram API")  
        time.sleep(3) 
        # Will be an exe in programs
        stopProgram_YN = stopProgram()
        if stopProgram_YN:
            # Kill timing loop
            pid_timing.killProgram()
            print("\nKilling TimingLoop.exe using its PID")  
            time.sleep(3) 
            # Kill any instances of the main API to present words and definitions
            pid_runProgram = PID("WordDefAPI")            
            if pid_runProgram.checkIfPIDisRunning():
                print("\nPID for WordDefAPI.exe is running.")
                time.sleep(3)
                pid_runProgram.killProgram() 
                print("\nKilling WordDefAPI.exe using its PID")
                time.sleep(3)
    else:                
        print("\nPID for TimingLoop.exe is not running.  So starting up startProgram API")
        time.sleep(3)
        runProgram_YN = startProgram()           
        if runProgram_YN:                  
            exeFilePath = get_exe_path('TimingLoop')
            print(f'\nRunning this exe using subprocess now:{exeFilePath}')
            time.sleep(4)
            subprocess.Popen([exeFilePath], creationflags=subprocess.CREATE_NEW_CONSOLE)
            # runApplicationTimingLoop() # Before installation

if __name__ == "__main__":
    setPyQt5path()
    startStopEditProgram()