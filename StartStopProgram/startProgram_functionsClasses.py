import os
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QScrollArea, QFileDialog
import platform

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
    checkTimeEntered.startButtonPressed = True
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