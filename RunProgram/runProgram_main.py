import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow
from commonClassesFunctions.functionsClasses import PID
from RunProgram.runProgram_functionsClasses import getDateForTitle
from RunProgram.runProgram_timingControl import TimingControl

def runApplicationTimingLoop():

    # Start an application
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Prevent the app from quitting when the window is closed

    # Create PID for current QApplication
    pid = PID()
    pid.createPID()    

    # Make a current window
    window = QMainWindow()
    dateForTitle = getDateForTitle()
    window.setWindowTitle("Word of the day.  " + dateForTitle) 

    # Crete timer to check time periodically and generate API if time to present API is reached
    timer = QTimer()
    timingControl = TimingControl(window) # Class to determine if time to present API is reached
    timer.timeout.connect(timingControl.timeReached)
    timer.start(1000) 
    # timer.start(60000)    

    # Run application's event loop
    exit_code = app.exec_()

    # Delete programs PID on program exit
    pid.cleanUpPID()

    # Exit application
    sys.exit(exit_code)

# Run the main function if this script is executed directly
if __name__ == "__main__":
    runApplicationTimingLoop()