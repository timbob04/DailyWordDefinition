import json

class Sizes_presentWODAPI:
    def __init__(self):
        self.padding_small = None
        self.padding_medium = None
        self.padding_large = None
        self.WODwidth = None
        self.maxWODheight = None
        self.smallTextWidth = None
        self.width_toggle = None

    def defineSizes(self):
        self.padding_small = 5
        self.padding_medium = 10
        self.padding_large = 20
        self.WODwidth = 450
        self.maxWODheight = 200
        self.smallTextWidth = 80
        self.width_toggle = 22


def readJSONfile(filepath):
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
            return data
    except (json.JSONDecodeError, FileNotFoundError, IOError):
        return None

class WODandDef():
    def __init__(self,dataIn,fileName):
        # Inputs
        self.dataIn = dataIn
        self.fileName = fileName
        # Class variables
        self.allWordsPrevShown = None
        self.positionOfWOD = None
        self.WOD = None
        self.definition = None
        self.dataExists = False
        self.WODpresent = None
        # Methods on initiation
        self.doesDataExist()
        if self.dataExists:
            self.areWordsPreset()
        if self.WODpresent:   
            self.areAllWordsPrevShown() # if yes, go back to start of list
            self.getWODpositionAndUpdateList()
            self.updateJSONfile()

    def doesDataExist(self):    
        self.dataExists = not (self.dataIn is None)

    def areWordsPreset(self):
        wordPresent = any(word['word'] for word in self.dataIn)
        defPresent = any(word['definition'] for word in self.dataIn)
        WODshownPresent = any(word['WOD_shown'] for word in self.dataIn)
        self.WODpresent = wordPresent & defPresent & WODshownPresent

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
            #print(self.positionOfWOD)
            self.WOD = self.dataIn[self.positionOfWOD]['word']
            self.definition = self.dataIn[self.positionOfWOD]['definition']
        return self.WOD, self.definition

class RODandDef():
    def __init__(self,dataIn,fileName):       
        # Inputs
        self.dataIn = dataIn
        self.fileName = fileName
        # Class variables
        self.dataExists = False
        self.RODpresent = False
        self.allRODshown = False
        self.positionOfROD = None
        self.ROD = None
        self.definition = None
        # Methods on initiation
        self.doesDataExist()
        if self.dataExists:
            self.isRODpresent()
        if self.RODpresent:
            self.getRODpositions()
            self.areAllRODshown()
            self.getRODposAndUpdateList()
            self.updateJSONfile()

    def doesDataExist(self):    
        self.dataExists = not (self.dataIn is None)        

    def isRODpresent(self):
        self.RODpresent = any(word['is_ROD'] for word in self.dataIn)

    def getRODpositions(self):
        self.RODpositions = []
        for index, word in enumerate(self.dataIn):
            if word['is_ROD']:
                self.RODpositions.append(index)                    

    def areAllRODshown(self):
        self.allRODshown = all(self.dataIn[i]['ROD_shown'] for i in self.RODpositions)
        
    
    def getRODposAndUpdateList(self):
        if self.allRODshown:
            # Get position of first is_ROD    
            self.positionOfROD = self.RODpositions[0]
            # Make all ROD_shown in is_ROD False, except for the first which is to be presented
            for i in self.RODpositions[1:]: 
                self.dataIn[i]['ROD_shown'] = False            
        else:
            # Get position of current is_ROD (first with False in ROD_shown)
            self.positionOfROD = self.firstFalsePos_ROD()            
            # Make the ROD_shown at this position True
            self.dataIn[self.positionOfROD]['ROD_shown'] = True

    def firstFalsePos_ROD(self):    
        for i in self.RODpositions: 
            if not self.dataIn[i]['ROD_shown']:
                return i    

    def updateJSONfile(self):
        with open(self.fileName, 'w') as file:
            json.dump(self.dataIn, file, indent=4)  

    def getAndreturnROD(self): 
        if self.RODpresent:
            self.ROD = self.dataIn[self.positionOfROD]['word']
            self.definition = self.dataIn[self.positionOfROD]['definition']
        return self.ROD, self.definition      

class ToggleChoices:
    def __init__(self):
        self.addWOD = False
        self.remPriorityWOD = False

def addWODtogglePressed(h_toggle,toggleChoicesClass):
    if h_toggle.isChecked():
        toggleChoicesClass.addWOD = True
    else:
        toggleChoicesClass.addWOD = False    
        
        

