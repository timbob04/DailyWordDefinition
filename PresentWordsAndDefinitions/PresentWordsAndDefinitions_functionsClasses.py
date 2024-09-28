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
        self.PODwidth = None
        self.maxPODheight = None

    def defineSizes(self):
        self.padding_small = 5
        self.padding_medium = 10
        self.padding_large = 20
        self.WODwidth = 400
        self.maxWODheight = 200
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
        self.WOD = "Currently no words/definitions.  Add some using the add/edit word API"
        self.definition = ""
        self.dataExists = False
        self.WODpresent = False
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
            #print(self.positionOfWOD)
            self.WOD = self.dataIn[self.positionOfWOD]['word']
            self.definition = self.dataIn[self.positionOfWOD]['definition']
        return self.WOD, self.definition

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

class ToggleChoices:
    def __init__(self, jsonData, jsonFilePath, WODob, PODob):
        self.jsonData = jsonData
        self.jsonFilePath = jsonFilePath
        self.WODob = WODob
        self.PODob = PODob
        self.addWOD = False
        self.remPriorityWOD = False        

    def addWODtogglePressed(self,h_toggle):
        if h_toggle.isChecked():
            self.addWOD = True
        else:
            self.addWOD = False    

    def remPODtogglePressed(self,h_toggle):
        if h_toggle.isChecked():
            self.remPriorityWOD = True
        else:
            self.remPriorityWOD = False   

    def saveToggleChoices(self):
        # Determine if WOD is now a POD and save choice - for the WOD, change its 'is_POD'
        if self.addWOD:
            self.jsonData[self.WODob.positionOfWOD]['is_POD'] = True
        else:
            self.jsonData[self.WODob.positionOfWOD]['is_POD'] = False
        # Determine if POD is now not a POD, and save choices - for the POD, change its 'is_POD'
        if self.remPriorityWOD:
            self.jsonData[self.PODob.positionOfPOD]['is_POD'] = False
        else:
            self.jsonData[self.PODob.positionOfPOD]['is_POD'] = True    
        # Save changes to json file
        with open(self.jsonFilePath, 'w') as file:
            json.dump(self.jsonData, file, indent=4)    



                     
        
        

