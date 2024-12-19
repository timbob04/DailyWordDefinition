import os
from datetime import datetime, time
from PyQt5.QtWidgets import QWidget
from commonClassesFunctions.functionsClasses import centerWindowOnScreen, getBaseDir
from RunProgram.runProgram_generateAPI import getAndMakeAPIcontent
from RunProgram.runProgram_functionsClasses import getTimeToRunApplicationPath

class TimingControl():
    def __init__(self,window):
        self.window = window
        self.lastRunTime = None

    def timeReached(self):

        # Get time to show API (decided by user)
        self.timeToShowDailyWord = self.getTimeToShowAPI()

        # Get minute of day this code last ran, do prevent the code below running twice within the same target minute
        current_time = datetime.now().time() 

        if self.checkIfTimeIsReached() and not self.isDateLastRunToday():

            # Update the dateLastRun text file
            self.writeNewDate()

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

    def checkIfTimeIsReached(self):
        # Get the current time of day
        current_time = datetime.now().time()
        # Compare the current time to the target time
        return self.timeToShowDailyWord <= current_time <= time(23, 59)
    
    def getTimeToShowAPI(self):
        time_dir = getTimeToRunApplicationPath()
        with open(time_dir, 'r') as file:
            time_str = file.read().strip()  # Read the time string and remove any extra whitespace
            return datetime.strptime(time_str, "%H:%M").time()
        
    def getDateLastRunPath(self):             
        base_dir = getBaseDir()
        common_dir = os.path.join(base_dir, '..', 'accessoryFiles')    
        return os.path.join(common_dir, 'dataLastRun.txt')  
    
    def readDateLastRun(self):
        file_path = self.getDateLastRunPath()
        if not os.path.exists(file_path):
            return None  # Return None if file doesn't exist
        with open(file_path, 'r') as file:
            try:
                date_str = file.read().strip()
                return datetime.strptime(date_str, "%m/%d/%Y").date()
            except Exception:
                return None
        
    def isDateLastRunToday(self):
        dateLastRun = self.readDateLastRun()
        if dateLastRun is None:
            return False
        return dateLastRun == datetime.now().date()
    
    def writeNewDate(self):
        file_path = self.getDateLastRunPath()
        current_date = datetime.now().strftime("%m/%d/%Y")  
        with open(file_path, 'w') as file:
            file.write(current_date)


    

