from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import sys
from commonClassesFunctions.functionsClasses import cleanUpPID, createPID, centerWindowOnScreen, getPIDfilePath
import os
from datetime import datetime
from PresentWordsAndDefinitions.presentWords_generateAPI import getAndMakeAPIcontent
from PresentWordsAndDefinitions.presentWords_functionsClasses import getDateForTitle

def runApplicationTimingLoop():

    # Start an application
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Prevent the app from quitting when the window is closed

    # Create PID for current QApplication
    PIDname  = getPIDfilePath()
    createPID(PIDname)    

    # Make a current window
    window = QMainWindow()
    dateForTitle = getDateForTitle()
    window.setWindowTitle("Word of the day.  " + dateForTitle) 

    # Crete timer to check time periodically and generate API if time to present API is reached
    timer = QTimer()
    timingControl = TimingControl(window) # Class to determine if time to present API is reached
    timer.timeout.connect(timingControl.timeReached)
    timer.start(1000)    

    # Run application's event loop
    exit_code = app.exec_()

    # Delete programs PID on program exit
    cleanUpPID(PIDname)

    # Exit application
    sys.exit(exit_code)

class TimingControl():
    def __init__(self,window):
        self.window = window
        self.lastRunTime = None

    def timeReached(self):

        # Get time to show API (decided by user)
        self.timeToShowDailyWord = self.getTimeToShowAPI()

        # Minute of that day that this code last ran, for not running code below within the same minute
        current_time = datetime.now().time() 

        if self.checkIfTimeMatches() and (current_time.hour, current_time.minute) != self.lastRunTime:

            # Update the last run minute
            self.lastRunTime = (current_time.hour, current_time.minute)

            # Close previous day's word window, if present
            if self.window:
                self.window.close()                
                if self.window.centralWidget() is not None:  # Check if central widget exists
                    self.window.centralWidget().deleteLater()  # Safely delete the central widget
                    self.window.setCentralWidget(None) # Clear all previous window content                
                for child in self.window.findChildren(QWidget):  # Find all child widgets
                    child.deleteLater()

            # Make API's new daily content
            getAndMakeAPIcontent(self.window)                

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
