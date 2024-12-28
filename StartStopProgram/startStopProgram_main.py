from StartStopProgram.startStopProgram_startProgramAPI import startProgram
from StartStopProgram.startStopProgram_stopProgramAPI import stopProgram
from commonClassesFunctions.functionsClasses import PID, get_exe_path, setPyQt5path
# from RunProgram.runProgram_timingLoop import runApplicationTimingLoop
import subprocess

def startStopEditProgram():

    print('StartStopEditProgram exe running')

    # Check if the program is currently running using its PID - the first point of entry is the timing loop code
    pid_timing = PID("TimingLoop")    
    
    if pid_timing.checkIfPIDisRunning():    
        # Will be an exe in programs
        stopProgram_YN = stopProgram()
        if stopProgram_YN:
            # Kill timing loop
            pid_timing.killProgram()
            # Kill any instances of the main API to present words and definitions
            pid_runProgram = PID("PresentWordsAndDefinitions")
            if pid_runProgram.checkIfPIDisRunning():
                pid_runProgram.killProgram() 
    else:                
        runProgram_YN = startProgram()           
        if runProgram_YN:                  
            exeFilePath = get_exe_path('TimingLoop')
            print(f'\nThe path of the TimingLoop.exe is\n{exeFilePath}')
            subprocess.run([exeFilePath], shell=True, stdin=None, stdout=None, stderr=None)
            # runApplicationTimingLoop() # Before installation

if __name__ == "__main__":
    setPyQt5path()
    startStopEditProgram()