from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit, QScrollArea, QFileDialog
from PyQt5.QtCore import Qt
import platform
import os
import re
from win32com.client import Dispatch

class Fonts:
    def __init__(self):
        # Initialize fonts
        self.font_tiny = None
        self.font_small = None
        self.font_medium = None
        self.font_large = None
        self.font_large_bold = None
        # Default values
        self.fontFamily = "Arial"
    
    def makeFonts(self):
        self.font_tiny = QFont(self.fontFamily, 8, QFont.Normal, False)
        self.font_small = QFont(self.fontFamily, 9, QFont.Normal, False)
        self.font_medium = QFont(self.fontFamily, 11, QFont.Normal, False)
        self.font_large = QFont(self.fontFamily, 17, QFont.Normal, False)    
        self.font_large_bold = QFont(self.fontFamily, 17, QFont.Bold, False)

# Create static text boxes
class StaticText:
    def __init__(self, window, font, text, position, textAlignment):
        # Input values
        self.window = window
        self.font = font
        self.text = text
        self.textAlignment = textAlignment
        self.position = position
        # Default values
        self.wordWrap = True
        self.fontMetrics = QFontMetrics(font)  
        self.color = 'black'
        # Initialize some variables
        self.positionAdjust = None
        self.Vcenter = None
        self.Hcenter = None    
        # Constructor functions
        self.getActualPosition()
        self.getVandHcenter()

    def getActualPosition(self):
        bounding_rect = self.fontMetrics.boundingRect(0,0,int(self.position[2]),int(self.position[3]), self.textAlignment, self.text)       
        self.positionAdjust = [int(self.position[0]), int(self.position[1]), int(bounding_rect.width()), int(bounding_rect.height())]

    def getVandHcenter(self):
        self.Hcenter = self.positionAdjust[0] + self.positionAdjust[2]/2
        self.Vcenter = self.positionAdjust[1] + self.positionAdjust[3]/2

    def centerAlign_V(self):
        self.positionAdjust[1] = int(self.positionAdjust[1] - self.positionAdjust[3]/2)

    def centerAlign_H(self):
        self.positionAdjust[0] = int(self.positionAdjust[0] - self.positionAdjust[2]/2)
            
    def makeTextObject(self):
        textOb = QLabel(self.text, self.window)
        textOb.setWordWrap(self.wordWrap)    
        textOb.setFont(self.font)
        textOb.setAlignment(self.textAlignment)
        textOb.setGeometry(*self.positionAdjust) 
        textOb.setStyleSheet(f"QLabel {{ color : {self.color}; }}")
        return textOb
    
# Create push button
class PushButton:
    def __init__(self, window, font, text, position):
        # Input values
        self.window = window
        self.font = font
        self.text = text        
        self.position = position
        # Default values
        self.wordWrap = True
        self.fontMetrics = QFontMetrics(font)        
        self.positionAdjust = None
        self.Vcenter = None
        self.Hcenter = None
        self.buttonPadding = 7
        self.textAlignment = Qt.AlignLeft | Qt.AlignVCenter | Qt.TextWordWrap 
        # Constructor functions
        self.getActualPosition()
        self.getVandHcenter()

    def getActualPosition(self):
        bounding_rect = self.fontMetrics.boundingRect(0,0,int(self.position[2]),int(self.position[3]), self.textAlignment, self.text)       
        self.positionAdjust = [int(self.position[0]), int(self.position[1]), \
                                int(bounding_rect.width()+self.buttonPadding*2), int(bounding_rect.height()+self.buttonPadding*2)]

    def getVandHcenter(self):
        self.Hcenter = self.positionAdjust[0] + self.positionAdjust[2]/2
        self.Vcenter = self.positionAdjust[1] + self.positionAdjust[3]/2

    def centerAlign_V(self):
        self.positionAdjust[1] = int(self.positionAdjust[1] - self.positionAdjust[3]/2)

    def centerAlign_H(self):
        self.positionAdjust[0] = int(self.positionAdjust[0] - self.positionAdjust[2]/2)

    def rightAlign(self,rightPoint):
        diff = (self.positionAdjust[0] + self.positionAdjust[2]) - rightPoint 
        self.positionAdjust[0] = self.positionAdjust[0] - diff
            
    def makeButton(self):
        button = QPushButton(self.text, self.window)
        button.setGeometry(*(int(x) for x in self.positionAdjust))    
        button.setFont(self.font)
        button.setStyleSheet("QPushButton { text-align: center; }")
        return button    
    
# Create edit text box   
class EditText:
    def __init__(self, window, font, startingText, position):
        # Default values
        self.padding = 10
        self.textAlignment = Qt.AlignCenter | Qt.AlignVCenter
        self.fontMetrics = QFontMetrics(font)
        # Inputs
        self.window = window
        self.font = font
        self.startingText = startingText
        self.position = position  
        # Functions
        self.getActualPosition()

    def getActualPosition(self):
        bounding_rect = self.fontMetrics.boundingRect(0,0,0,0, self.textAlignment, self.startingText)       
        self.positionAdjust = [int(self.position[0]), int(self.position[1]), \
                                int(bounding_rect.width()+self.padding*2), int(bounding_rect.height()+self.padding)]

    def forceWidth(self):
        self.positionAdjust[2] = self.position[2]

    def centerAlign_V(self):
        self.positionAdjust[1] = int(self.positionAdjust[1] - self.positionAdjust[3]/2)

    def centerAlign_H(self):
        self.positionAdjust[0] = int(self.positionAdjust[0] - self.positionAdjust[2]/2)
            
    def makeEditTextBox(self):        
        editBox = QLineEdit(self.window) # Make edit box
        editBox.setText(self.startingText)
        editBox.setFont(self.font)              
        editBox.setFixedWidth(self.positionAdjust[2])  # Set the width of the text box to fit the text, with added padding
        editBox.setAlignment(self.textAlignment) 
        editBox.setGeometry(*(int(x) for x in self.positionAdjust))
        return editBox    
    
def getStartupFolder():
    system = platform.system()
    if system == 'Windows':
        return os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    elif system == 'Darwin':  # macOS
        return os.path.expanduser('~/Library/LaunchAgents')
    elif system == 'Linux':
        return os.path.expanduser('~/.config/autostart')
    else:
        return None
    

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

class EditStartupFolder:
    def __init__(self, position, window, startupFolder):
        # Default properties        
        self.window = window
        self.positionOfText = position
        self.startupFolder = startupFolder
        self.font = QFont("", 7, QFont.Normal, False)
        self.textAlignment = Qt.AlignLeft
        self.wordWrap = False
        # Initialize text box and scroll area
        self.textBox = None
        self.scroll_area = None
        self.newFolder = None
        # Functions to run on initialization        
        self.showStartupFolTextBox()
        self.makeScrollBarForStartupText()

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
        self.newFolder = file_dialog.getExistingDirectory(None, "Select Folder",self.startupFolder)        

    def updatePath(self):
        self.manuallySelectPath()
        if self.newFolder: # only do something if the user selects a new folder
            self.startupFolder = self.newFolder
            self.textBox.setText(self.startupFolder) # update window text for startup folder

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
        curFilePath = os.path.join(common_dir, 'startupFolder.txt') # write the startup folder to here
        if startupToggle.isChecked():
            startupFolder = startupFolOb.startupFolder
            tempFile = r"C:\Users\timot\OneDrive\Desktop\tempLinkStartupFile.txt"
            print("\nThis is where I will get the exe folder when finished everything else")
            create_startup_shortcut(tempFile, startupFolder)
        else:
            startupFolder = "" # will make the startup folder .txt empty
        # Save startup folder text
        with open(curFilePath, 'w') as file:
            file.write(startupFolder)        
        # Set the window.startButtonPressed to true
        window.runProgram = True        
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
class CheckTimeEntered_start():
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

def create_startup_shortcut(file_path, startupFolder):
    system = platform.system()
    if system == 'Windows':
        shortcut_path = os.path.join(startupFolder, "presentWords_runProgram_shortcut.lnk") # the full file path of the short cut to the input file, to go in the startup folder
        shell = Dispatch('WScript.Shell') # Access the Windows Script Host to manage shortcuts
        shortcut = shell.CreateShortcut(shortcut_path) # Create shortcut file
        shortcut.TargetPath = file_path # Set the target path
        shortcut.WorkingDirectory = os.path.dirname(file_path) # Set the working directory for this shortcut to the original file's path
        shortcut.Save() # save the shortcut file
    elif system in ['Darwin', 'Linux']:        
        os.makedirs(startupFolder, exist_ok=True)
        desktop_file = os.path.join(startupFolder, "presentWords_runProgram_shortcut.desktop")
        with open(desktop_file, "w") as file:
            file.write(f"""[Desktop Entry]
Type=Application
Exec={file_path}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Run Present Words Program
""")
            
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
class CheckTimeEntered_stop():
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
        if self.correctYN_both or self.stopToggleState: # hide text if both HH and MM correct, or 'Stop program' toggle checked
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
        window.stopProgram = True
        window.close()                  
        RemoveStartupFolderShortcut()
    elif checkTimeEntered.correctYN_both:
        # Write time to run program to .txt file
        curFilePath = os.path.join(common_dir, 'timeToRunApplication.txt')
        with open(curFilePath, 'w') as file:
            file.write(f"{HH}:{MM}")    
        window.close()  

class RemoveStartupFolderShortcut:
    def __init__(self):
        self.extension = ''
        self.shortcut_auto = None
        self.shortcut_selected = None        
        self.findShortcutExtension()
        self.shortcutPath_auto() # path to shortcut file in automatically found startup folder for computer
        self.startUpFolderTxtFileName() # get the file where the pre-selected startup folder is saved
        self.shortcutPath_selected() # path to shortcut file in pre-selected startup folder for computer
        self.deleteShortcuts() # delete the shortcut/s
        self.makeStartupTxtFileBlank() # make the file where the pre-selected startup folder is blank        

    def findShortcutExtension(self):
        system = platform.system()
        if system == 'Windows':
            self.extension = '.lnk'
        elif system in ['Darwin', 'Linux']:   
            self.extension = '.desktop'

    def shortcutPath_auto(self):
        # Link to shortcut using automatically found startup folder
        startupFolder_auto = getStartupFolder()
        self.shortcut_auto = os.path.join(startupFolder_auto, f'presentWords_runProgram_shortcut{self.extension}')

    def startUpFolderTxtFileName(self):
        # Get path of accessory files
        base_dir = os.path.dirname(os.path.abspath(__file__))
        accessoryFiles_dir = os.path.join(base_dir, '..', 'accessoryFiles')
        # Path to json file for words and definitions
        self.startUpFolderTxtPath = os.path.join(accessoryFiles_dir, 'startupFolder.txt')

    def shortcutPath_selected(self):    
        if os.path.exists(self.startUpFolderTxtPath):
            with open(self.startUpFolderTxtPath, 'r') as file:
                path = file.readline().strip()  
            self.shortcut_selected = os.path.join(path, f'presentWords_runProgram_shortcut{self.extension}')

    def startUpFolderTxtFileName(self):
        # Get path of accessory files
        base_dir = os.path.dirname(os.path.abspath(__file__))
        accessoryFiles_dir = os.path.join(base_dir, '..', 'accessoryFiles')
        # Path to json file for words and definitions
        self.startUpFolderTxtPath = os.path.join(accessoryFiles_dir, 'startupFolder.txt')

    def deleteShortcuts(self):
        if os.path.exists(self.shortcut_auto):
            os.remove(self.shortcut_auto)
        if os.path.exists(self.shortcut_selected):
            os.remove(self.shortcut_selected)

    def makeStartupTxtFileBlank(self):
        if os.path.exists(self.startUpFolderTxtPath):
            with open(self.startUpFolderTxtPath, 'w') as file:
                file.write("")
  
   
   
    
    




    