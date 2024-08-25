import os
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QScrollArea, QFileDialog
import platform
import re

# Predefined sizes for text boxes, etc
class Sizes_startProgram:
    def __init__(self):
        self.padding_small = None
        self.padding_medium = None
        self.padding_large = None
        self.width_ST_chooseTime = None
        self.startingY_checkBox = None
        self.width_toggle = None
        self.width_ST_startupToggle = None
        self.width_text_startupFolder = None
        self.height_text_startupFolder = None
        self.width_button_change = None

    def defineSizes(self):
        self.padding_small = 5
        self.padding_medium = 10
        self.padding_large = 20
        self.width_ST_chooseTime = 400
        self.startingY_checkBox = 160
        self.width_toggle = 22
        self.width_ST_startupToggle = 300
        self.width_text_startupFolder = 230
        self.height_text_startupFolder = 50
        self.width_button_change = 45

class GetAndShowStartupFolder:
    def __init__(self, position, window):
        # Default properties        
        self.window = window
        self.positionOfText = position
        self.font = QFont("", 7, QFont.Normal, False)
        self.textAlignment = Qt.AlignLeft
        self.wordWrap = False
        # Initialize text box and scroll area
        self.textBox = None
        self.scroll_area = None
        # Functions to run on initialization
        self.startupFolder = self.getStartupFolderAutomatically()
        self.showStartupFolTextBox()
        self.makeScrollBarForStartupText()

    def getStartupFolderAutomatically(self):
        system = platform.system()
        if system == 'Windows':
            return os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        elif system == 'Darwin':  # macOS
            return os.path.expanduser('~/Library/LaunchAgents')
        elif system == 'Linux':
            return os.path.expanduser('~/.config/autostart')
        else:
            return None

    def showStartupFolTextBox(self):
        self.textBox = QLabel(self.startupFolder,self.window)
        self.textBox.setWordWrap(self.wordWrap) 
        self.textBox.setAlignment(self.textAlignment) 
        self.textBox.setGeometry(*(int(x) for x in self.positionOfText))  
        self.textBox.setFont(self.font)  
        self.textBox.hide() # show when startup folder toggle pressed

    def makeScrollBarForStartupText(self):
        self.scroll_area = QScrollArea(self.window)
        self.scroll_area.setWidgetResizable(True)  
        self.scroll_area.setWidget(self.textBox)  
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  
        self.scroll_area.setGeometry(*(int(x) for x in self.positionOfText))
        self.scroll_area.hide() # show when startup folder toggle pressed

    def manuallySelectPath(self):
        file_dialog = QFileDialog()
        selected_path = file_dialog.getExistingDirectory(None, "Select Folder",self.startupFolder)
        return selected_path

    def updatePath(self):
        new_folder = self.manuallySelectPath()
        if new_folder:
            self.startupFolder = new_folder # update startup folder
            self.textBox.setText(new_folder) # update window text for startup folder

def startButtonPressed(window,checkTimeEntered,HH,MM,startupToggle,startupFolOb):   
    checkTimeEntered.buttonPressed = True
    checkTimeEntered.showOrHideText()
    if checkTimeEntered.correctYN_both:        
        # Get path of accessory files
        base_dir = os.path.dirname(os.path.abspath(__file__))
        common_dir = os.path.join(base_dir, '..', 'accessoryFiles')
        # Write time to run program to .txt file
        curFilePath = os.path.join(common_dir, 'timeToRunApplication.txt')
        with open(curFilePath, 'w') as file:
            file.write(f"{HH}:{MM}")
        # Startup folder stuff
        curFilePath = os.path.join(common_dir, 'startupFolder.txt')
        if startupToggle.isChecked():
            startupFolderText = startupFolOb.startupFolder
            # Here put the main program in the startup folder
            print("Here put the main exe file in the startup folder")
        else:
            startupFolderText = "" # will make the startup folder .txt empty
        # Save startup folder text
        with open(curFilePath, 'w') as file:
            file.write(startupFolderText)            

        # Change application running boolean to true
        curFilePath = os.path.join(common_dir, 'applicationRunning_YN.txt')
        with open(curFilePath, 'w') as file:
            file.write("1")
        # Start the main program's exe file running
        print("Here run the main program's exe file")
        # Close window
        window.close() 

# Shows/hides startup path if the startup folder toggle button is pressed
def startupTogglePressed(h_toggle, h_changeButton, h_startupTextObject):
    if h_toggle.isChecked():
        h_changeButton.show()
        h_startupTextObject.textBox.show()
        h_startupTextObject.scroll_area.show()
    else:
        h_changeButton.hide()
        h_startupTextObject.textBox.hide()
        h_startupTextObject.scroll_area.hide()

# Class to determine if the HH and MM text in the edit text box is correct
class CheckTimeEntered():
    def __init__(self):        
        # Default values
        self.handleText = None
        self.correctYN_HH = False
        self.correctYN_MM = False
        self.correctYN_both = False  
        self.buttonPressed = False # becomes true once the Start button is pressed

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
        if not self.buttonPressed:
            return
        if self.correctYN_both:
            self.handleText.hide()
        else:
            self.handleText.show() 