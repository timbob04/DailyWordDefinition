from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from commonClassesFunctions.functionsClasses import cleanUpPID, createPID
import os
import time
from datetime import datetime
from PresentWordsAndDefinitions.presentWords_generateAPI import getAndMakeAPIcontent
from commonClassesFunctions.functionsClasses import centerWindowOnScreen

def runApplicationTimingLoop():
    
    PIDname = "PresentWordsAndDefinitions.pid"    
    
    # Start an application
    app = QApplication(sys.argv)

    # Create PID for current QApplication
    createPID(PIDname)    

    # Make a current window
    window = QMainWindow()
    window.setWindowTitle('Word of the day') 

    # Crete timer to check time periodically and generate API if time to present API is reached
    timer = QTimer()
    timingControl = TimingControl(window) # Class to determine if time to present API is reached
    timer.timeout.connect(timingControl.timeReached)
    timer.start(58000)    

    # Run application's event loop
    exit_code = app.exec_()

    # Delete programs PID on program exit
    cleanUpPID(PIDname)

    # Exit application
    sys.exit(exit_code)

class TimingControl():
    def __init__(self,window):
        self.window = window

    def timeReached(self):

        # Get time to show API    
        self.timeToShowDailyWord = self.getTimeToShowAPI()

        if self.checkIfTimeMatches():

            # Close previous day's word window, if present
            if self.window:
                self.window.close()
                self.window.setCentralWidget(None) # Clear all previous window content
                time.sleep(0.1)

            # Make API's new daily content
            getAndMakeAPIcontent(self.window)    

            time.sleep(3) # So I don't run the function again within the same minute

            # Show window
            self.window.show()

            # Center the window - put in the function (pass it 'window' and 'app')
            centerWindowOnScreen(self.window)

    def checkIfTimeMatches(self):
        # Get the current time of day
        current_time = datetime.now().time()
        # Compare the current time to the target time
        return current_time.hour == self.timeToShowDailyWord.hour and current_time.minute == self.timeToShowDailyWord.minute    
    
    def getTimeToShowAPI(self):
        # Get path of accessory files
        base_dir = os.path.dirname(os.path.abspath(__file__))
        accessoryFiles_dir = os.path.join(base_dir, '..', 'accessoryFiles')
        # Path to json file for words and definitions
        time_dir = os.path.join(accessoryFiles_dir, 'timeToRunApplication.txt')
        with open(time_dir, 'r') as file:
            time_str = file.read().strip()  # Read the time string and remove any extra whitespace
            return datetime.strptime(time_str, "%H:%M").time()

runApplicationTimingLoop()
