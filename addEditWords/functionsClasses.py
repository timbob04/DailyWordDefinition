import json
import os
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt
from commonClassesFunctions.utils import readJSONfile, getBaseDir

# Some common sizes used to make the API
class Sizes_addEditWords:
    def __init__(self):
        self.padding_small = None
        self.padding_medium = None
        self.padding_large = None
        self.APIwidth = None
        self.APIheight = None
        self.width_toggle = None

    def defineSizes(self):
        self.padding_small = 5
        self.padding_medium = 10
        self.padding_large = 20
        self.APIwidth = 1400
        self.APIheight = 1000
        self.width_toggle = 22

# For the edit text boxes to add new words and definitions to the list
class addNewWordTextBoxes:
    def __init__(self,window,sizes,fonts):
        self.window = window
        self.sizes = sizes
        self.fonts = fonts                         
        self.addWordInput = None
        self.addDefInput = None   
        self.newWord = None
        self.newDefinition = None   
        self.jsonFileName = getWordListPath()        

    def makeAddWordEditTextBox(self,left,top,width):    
        self.addWordInput = QLineEdit(self.window)    
        self.addWordInput.setGeometry(int(left), int(top), int(width), 40 )
        self.addWordInput.setFont(self.fonts.font_mediumLarge)
        self.addWordInput.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.addWordInput.setStyleSheet("QLineEdit { border: 1px solid black; }")

    def makeAddDefEditTextBox(self,left,top,width):    
        self.addDefInput = QLineEdit(self.window)    
        self.addDefInput.setGeometry(int(left), int(top), int(width), 40 )
        self.addDefInput.setFont(self.fonts.font_mediumLarge)
        self.addDefInput.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.addDefInput.setStyleSheet("QLineEdit { border: 1px solid black; }")

    def getNewWordDef(self):
        self.newWord = self.addWordInput.text()
        self.newDefinition = self.addDefInput.text()            
    
    def addWordToJSONfile(self):      
        self.dataIn = readJSONfile(self.jsonFileName)      
        # Make the new word/def json entry
        new_entry = {
            "word": self.newWord,
            "definition": self.newDefinition,
            "WOD_shown": False,
            "is_POD": False,
            "POD_shown": False
            }
        # Append new word/def to current word/def json list
        if self.dataIn is not None:
            self.dataIn.append(new_entry)
        else:
            self.dataIn = [new_entry]
        # Save new list with new word/def
        with open(self.jsonFileName, 'w') as file:
            json.dump(self.dataIn, file, indent=4) 

    def clearEditTextBoxes(self):
        self.addWordInput.clear()
        self.addDefInput.clear()
    
    def AddButtonPressed(self):
        self.getNewWordDef()
        self.addWordToJSONfile()        
        self.clearEditTextBoxes()   

def getWordListPath():
    # Get path of accessory files
    base_dir = getBaseDir()
    accessoryFiles_dir = os.path.join(base_dir, '..', 'accessoryFiles')
    # Path to json file for words and definitions
    return os.path.join(accessoryFiles_dir, 'WordsDefsCodes.json')             
    
