import time
from RunProgram.runProgram_timingControl import TimingControl
from commonClassesFunctions.functionsClasses import PID, get_exe_path, setPyQt5path
import subprocess

def runApplicationTimingLoop():

    # For checking when the API should be presented
    timingControl = TimingControl()
    
    # Make PID to indicate that this code's timing loop is running
    pid_time = PID("TimingLoop")
    pid_time.createPID()
    print("\nCreating PID for timing loop (this exe).")
    time.sleep(3)
        
    while True:  
        print('Timing loop looping ...')                  
        if timingControl.checkIfTimeToRunProgram():            
            print('\n\nTime reached to run WordDefAPI')     
            time.sleep(3)
            # Close any previous instances of main API to show words/definitions
            pid_wordDefAPI = PID("WordDefAPI")                         
            if pid_wordDefAPI.checkIfPIDisRunning():
                print("\n\nKilling previous instances on WordDefAPI.")
                time.sleep(3)
                pid_wordDefAPI.killProgram()
            # Make API to show today's word and definition
            exeFilePath = get_exe_path('WordDefAPI')
            print(f'\nRunning this exe using subprocess now:{exeFilePath}')
            time.sleep(3)
            subprocess.Popen([exeFilePath], creationflags=subprocess.CREATE_NEW_CONSOLE)
            # subprocess.Popen([exeFilePath], creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_CONSOLE)
            # getAndMakeAPIcontent()         
        time.sleep(5)

# Run the main function if this script is executed directly
if __name__ == "__main__":
    setPyQt5path()
    runApplicationTimingLoop()