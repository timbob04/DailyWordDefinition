import os
import json
from datetime import datetime

class Sizes_presentWODAPI:
    def __init__(self):
        self.padding_small = None
        self.padding_medium = None
        self.padding_large = None
        self.WODwidth = None
        self.maxWODheight = None
        self.maxDefheight = None
        self.smallTextWidth = None
        self.width_toggle = None
        self.PODwidth = None
        self.maxPODheight = None

    def defineSizes(self):
        self.padding_small = 5
        self.padding_medium = 10
        self.padding_large = 20
        self.WODwidth = 400
        self.maxWODheight = 120
        self.maxDefheight = 200
        self.smallTextWidth = 120
        self.width_toggle = 22
        self.PODwidth = self.WODwidth * 0.8
        self.maxPODheight = 150

class WODandDef():
    def __init__(self,dataIn,fileName):
        # Inputs
        self.dataIn = dataIn
        self.fileName = fileName
        # Class variables
        self.allWordsPrevShown = None
        self.positionOfWOD = None
        self.WOD = "No words added"
        self.definition = ""
        self.dataExists = False
        self.WODpresent = False
        self.WODsPODstatus = False
        # Methods on initiation
        self.doesDataExist()
        if self.dataExists:
            self.areWordsPresent()
        if self.WODpresent:   
            self.areAllWordsPrevShown() # if yes, go back to start of list
            self.getWODpositionAndUpdateList()
            self.updateJSONfile()

    def doesDataExist(self):    
        self.dataExists = not (self.dataIn is None) and len(self.dataIn) > 0

    def areWordsPresent(self):
        wordPresent = any(word['word'] for word in self.dataIn)
        defPresent = any(word['definition'] for word in self.dataIn)        
        self.WODpresent = wordPresent and defPresent

    def areAllWordsPrevShown(self):
        # Check to see if the entire list of words has been presented (for this round)
        self.allWordsPrevShown = all(word['WOD_shown'] for word in self.dataIn)

    def getWODpositionAndUpdateList(self):       
        # Get WOD and update word list accordingly
        if (self.allWordsPrevShown):
            for word in self.dataIn[1:]: # change all 'WOD_shown' to false, except the first
                word['WOD_shown'] = False
            self.positionOfWOD = 0    
        else:
            self.positionOfWOD = self.firstFalse_WOD_shown()
            self.dataIn[self.positionOfWOD]['WOD_shown'] = True
    
    def firstFalse_WOD_shown(self):
        for index, word in enumerate(self.dataIn):
            if not word['WOD_shown']:
                return index
        return None  

    def updateJSONfile(self):
        with open(self.fileName, 'w') as file:
            json.dump(self.dataIn, file, indent=4)  

    def getAndreturnWOD(self): 
        if self.WODpresent:            
            self.WOD = self.dataIn[self.positionOfWOD]['word']
            self.definition = self.dataIn[self.positionOfWOD]['definition']
        return self.WOD, self.definition
    
    def getWODsPODstatus(self):
        if self.WODpresent:
            self.WODsPODstatus = self.dataIn[self.positionOfWOD]['is_POD']
        return self.WODsPODstatus

class PODandDef():
    def __init__(self,dataIn,fileName):       
        # Inputs
        self.dataIn = dataIn
        self.fileName = fileName
        # Class variables
        self.dataExists = False
        self.PODpresent = False
        self.allPODshown = False
        self.positionOfPOD = None
        self.PODandDef = "Currently no priority words"        
        # Methods on initiation
        self.doesDataExist()
        if self.dataExists:
            self.isPODpresent()
        if self.PODpresent:
            self.getPODpositions()
            self.areAllPODshown()
            self.getPODposAndUpdateList()
            self.updateJSONfile()        

    def doesDataExist(self):    
        self.dataExists = not (self.dataIn is None) and len(self.dataIn) > 0   

    def isPODpresent(self):
        self.PODpresent = any(word['is_POD'] for word in self.dataIn)

    def getPODpositions(self):
        self.PODpositions = []
        for index, word in enumerate(self.dataIn):
            if word['is_POD']:
                self.PODpositions.append(index)                    

    def areAllPODshown(self):
        self.allPODshown = all(self.dataIn[i]['POD_shown'] for i in self.PODpositions)
            
    def getPODposAndUpdateList(self):
        if self.allPODshown:
            # Get position of first is_POD    
            self.positionOfPOD = self.PODpositions[0]
            # Make all POD_shown in is_POD False, except for the first which is to be presented
            for i in self.PODpositions[1:]: 
                self.dataIn[i]['POD_shown'] = False            
        else:
            self.positionOfPOD = self.firstFalsePos_POD() # get the position of the first 'Pod_shown' is false
            if self.positionOfPOD is not None:
                # Make the POD_shown at this position True
                self.dataIn[self.positionOfPOD]['POD_shown'] = True
            else:
                # Handle the case where no unshown POD is found (e.g., reset or log an error)
                self.positionOfPOD = self.PODpositions[0]  # or other appropriate action

    def firstFalsePos_POD(self):    
        for i in self.PODpositions: 
            if not self.dataIn[i]['POD_shown']:
                return i    

    def updateJSONfile(self):
        with open(self.fileName, 'w') as file:
            json.dump(self.dataIn, file, indent=4)  

    def getAndreturnPOD(self): 
        if self.PODpresent:
            POD = self.dataIn[self.positionOfPOD]['word']
            definition = self.dataIn[self.positionOfPOD]['definition']            
            self.PODandDef = POD + ": " + definition
        return self.PODandDef

def saveToggleChoice(h_toggle,jsonFilePath,jsonData,pos):            
    # Update data
    if h_toggle.isChecked(): 
        jsonData[pos]['is_POD'] = True
    else:
        jsonData[pos]['is_POD'] = False   
    # Save data
    with open(jsonFilePath, 'w') as file:
        json.dump(jsonData, file, indent=4)    

def getDateForTitle():
     # Get the current date
    today = datetime.now()
    # Determine the current day (number)
    day = today.day
    # Figure out the suffix for the current day
    if 10 <= day <= 20:  # "Teen" numbers always get "th"
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        # The function 'get' uses the first argument and returns the output of the matching input in the preceding dictionary (dicionary.get)
        # If there is no match, it returns what is in the second argument for the get function
    # Format the date with the correct suffix
    formatted_date = today.strftime(f"%d{suffix} %B %Y")
    return formatted_date

def getTimeToRunApplicationPath():
    # Get path of accessory files
    base_dir = os.path.dirname(os.path.abspath(__file__))
    accessoryFiles_dir = os.path.join(base_dir, '..', 'accessoryFiles')
    # Path to json file for words and definitions
    return os.path.join(accessoryFiles_dir, 'timeToRunApplication.txt')
                     
        
        

