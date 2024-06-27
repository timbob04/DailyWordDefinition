import os
import re

# Predefined sizes for text boxes, etc
class Sizes_stopProgram:
    def __init__(self):
        self.padding_small = None
        self.padding_medium = None
        self.padding_large = None
        self.width_ST_editTime = None
        self.startingY_checkBox = None
        self.width_toggle = None
        self.width_ET_hourMin = None
       

    def defineSizes(self):
        self.padding_small = 5
        self.padding_medium = 10
        self.padding_large = 20
        self.width_ST_editTime = 400
        self.startingY_checkBox = 160
        self.width_toggle = 22
        self.width_ET_hourMin = 45

# Class to determine if the HH and MM text in the edit text box is correct
class CheckTimeEntered():
    def __init__(self):        
        # Default values
        self.handleText = None
        self.correctYN_HH = False
        self.correctYN_MM = False
        self.correctYN_both = False  
        self.ET_HH = None
        self.ET_MM = None
        self.OkbuttonPressed = False # becomes true once the Ok button is pressed
        self.stopToggleState = False # becomes true when stop toggle checked on

    def checkStopToggle(self, toggleState):
        self.stopToggleState = toggleState              
        self.changeStateOfEditBox()
        self.showOrHideText()

    def changeStateOfEditBox(self):
        self.ET_HH.setReadOnly(self.stopToggleState)
        self.ET_HH.setEnabled(not self.stopToggleState) 
        self.ET_MM.setReadOnly(self.stopToggleState)
        self.ET_MM.setEnabled(not self.stopToggleState)

    def checkTime_HH(self, newText):
        if re.fullmatch(r'([0-1]?[0-9]|2[0-3])', newText): # is the hour entered between 00 and 23
            self.correctYN_HH = True
        else: 
            self.correctYN_HH = False
        self.bothCorrect()    
        self.showOrHideText()

    def checkTime_MM(self, newText):
        if re.fullmatch(r'([0-5]?[0-9])', newText): # is the minute entered between 00 and 59
            self.correctYN_MM = True
        else: 
            self.correctYN_MM = False
        self.bothCorrect()
        self.showOrHideText()

    def bothCorrect(self):
        if self.correctYN_HH & self.correctYN_MM:
            self.correctYN_both = True
        else:
            self.correctYN_both = False

    def showOrHideText(self):
        if not self.OkbuttonPressed: # don't do anything if Ok button not pressed yet
            return
        if self.correctYN_both | self.stopToggleState: # hide text if both HH and MM correct, or 'Stop program' toggle checked
            self.handleText.hide()
        else:
            self.handleText.show() # otherwise show text

def OkButtonPressed(window,checkTimeEntered,stopProgramToggle,HH,MM): 
    
    checkTimeEntered.OkbuttonPressed = True
    checkTimeEntered.showOrHideText()

    # Get path of accessory files
    base_dir = os.path.dirname(os.path.abspath(__file__))
    common_dir = os.path.join(base_dir, '..', 'accessoryFiles')

    if stopProgramToggle.isChecked():
        print('All the things for stopping the program and removing it from the startup folder')
        # 1) Stop to main exe
        # 2) Remove the main exe from the startup folder
        # 3) Change application running boolean to false
        curFilePath = os.path.join(common_dir, 'applicationRunning_YN.txt')
        with open(curFilePath, 'w') as file:
            file.write("0")            
    elif checkTimeEntered.correctYN_both:
        print('All the things for editing the time for the program to run')
        # Write time to run program to .txt file
        curFilePath = os.path.join(common_dir, 'timeToRunApplication.txt')
        with open(curFilePath, 'w') as file:
            file.write(f"{HH}:{MM}")
    else:
        return
    
    window.close()  

