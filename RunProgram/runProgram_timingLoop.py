import time
from RunProgram.runProgram_timingControl import TimingControl
from commonClassesFunctions.functionsClasses import PID, get_exe_path, setPyQt5path
import subprocess

def runApplicationTimingLoop():

    # For checking when the API should be presented
    timingControl = TimingControl()
    
    # Make PID to indicate that this code's timing loop is running
    pid = PID("TimingLoop")
    pid.createPID()

    while True:                    
        if timingControl.checkIfTimeToRunProgram():
            # Close any previous instances of main API to show words/definitions
            pid = PID("WordDefAPI")                        
            if pid.checkIfPIDisRunning():
                pid.killProgram()
            # Make API to show today's word and definition
            exeFilePath = get_exe_path('WordDefAPI')
            subprocess.run([exeFilePath], shell=True, stdin=None, stdout=None, stderr=None)
            # getAndMakeAPIcontent()         
        time.sleep(5)

# Run the main function if this script is executed directly
if __name__ == "__main__":
    setPyQt5path()
    runApplicationTimingLoop()