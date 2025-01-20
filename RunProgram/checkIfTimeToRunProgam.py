import os
from datetime import datetime, time
from commonClassesFunctions.utils import getBaseDir

class TimingControl():

    def checkIfTimeToRunProgram(self):
        if self.checkIfTimeIsReached() and not self.isDateLastRunToday():
            self.writeNewDate() # Update the dateLastRun text file
            return True           
            
    def checkIfTimeIsReached(self):
        # Get the current time of day
        current_time = datetime.now().time()
        # Get time to show word
        timeToShowDailyWord = self.getTimeToShowAPI()
        # Compare the current time to the target time
        return timeToShowDailyWord <= current_time <= time(23, 59)
    
    def getTimeToShowAPI(self):
        time_dir = self.getTimeToRunApplicationPath()
        with open(time_dir, 'r') as file:
            time_str = file.read().strip()  # Read the time string and remove any extra whitespace
            return datetime.strptime(time_str, "%H:%M").time()
        
    def getTimeToRunApplicationPath(self):
        # Get path of accessory files
        base_dir = getBaseDir()
        accessoryFiles_dir = os.path.join(base_dir, '..', 'accessoryFiles')
        # Path to json file for words and definitions
        return os.path.join(accessoryFiles_dir, 'timeToRunApplication.txt')    
        
    def getDateLastRunPath(self):             
        base_dir = getBaseDir()
        common_dir = os.path.join(base_dir, '..', 'accessoryFiles')    
        return os.path.join(common_dir, 'dateLastRun.txt')  
    
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


    

