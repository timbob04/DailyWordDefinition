from RunProgram.runProgram_timingControl import TimingControl
import time
from commonClassesFunctions.functionsClasses import PID
from RunProgram.runProgram_generateAPI import getAndMakeAPIcontent

def runApplicationTimingLoop():

    # For checking when the API should be presented
    timingControl = TimingControl()
    
    # Make PID to indicate that this code's timing loop is running
    pid = PID("TimingLoop")
    pid.createPID()

    while True:                
        if timingControl.checkIfTimeToRunProgram():
            # Close any previous instances of main API to show words/definitions
            pid = PID("PresentWordsAndDefinitions")            
            if pid.checkIfPIDisRunning():
                pid.killProgram()
            # Make API to show today's word and definition
            getAndMakeAPIcontent()     
        time.sleep(60)

# Run the main function if this script is executed directly
if __name__ == "__main__":
    runApplicationTimingLoop()