import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QLabel,  QLineEdit, QFileDialog, QSpacerItem, QSizePolicy, QScrollArea
from PyQt5.QtGui import QFontMetrics, QFont
from PyQt5.QtCore import Qt
import os
import platform

# Functions

# Implement button clicked - action
def startButtonPressed(toggle_button,getStartupFolder,window):
    # 1) Set time in timeToRunProgram.txt
    # 2) Change .bin file boolean to '1'
    # 3) Adds exe of main program to startup folder (if toggle pressed) - below
    # 4) Saves the startup folder in a text file (only if toggle pressed)
    
    # Number 3
    toggle_state = toggle_button.isChecked() # if true, add relevant file to startup folder
    if toggle_state:
        print(f'This is where I will add the main exe file to the startup folder, which is {getStartupFolder.startupFolder}')
   
   # And then close the window
    window.close() 

class Fonts:
    def __init__(self):
        self.font_small = None
        self.font_medium = None
        self.font_large = None
        self.font_large_bold = None
    
    def makeFonts(self):
        self.font_small = QFont("", 9, QFont.Normal, False)
        self.font_medium = QFont("", 11, QFont.Normal, False)
        self.font_large = QFont("", 17, QFont.Normal, False)    
        self.font_large_bold = QFont("", 17, QFont.Bold, False)
    
class GetAndShowStartupFolder:
    def __init__(self, position, window):
        # Default properties        
        self.window = window
        self.positionOfText = position
        self.font = QFont("", 7, QFont.Normal, False)
        self.textAlignment = Qt.AlignLeft
        self.wordWrap = False
        # Initialize text box
        self.textBox = None
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

    def makeScrollBarForStartupText(self):
        scroll_area = QScrollArea(self.window)
        scroll_area.setWidgetResizable(True)  
        scroll_area.setWidget(self.textBox)  
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  
        scroll_area.setGeometry(*(int(x) for x in self.positionOfText))

    def manuallySelectPath(self):
        file_dialog = QFileDialog()
        selected_path = file_dialog.getExistingDirectory(None, "Select Folder",self.startupFolder)
        return selected_path

    def updatePath(self):
        new_folder = self.manuallySelectPath()
        if new_folder:
            self.startupFolder = new_folder # update startup folder
            self.textBox.setText(new_folder) # update window text for startup folder

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

    def centerAlign(self):
        self.positionAdjust[1] = int(self.positionAdjust[1] - self.positionAdjust[3]/2)
            
    def makeTextObject(self):
        textOb = QLabel(self.text, self.window)
        textOb.setWordWrap(self.wordWrap)    
        textOb.setFont(self.font)
        textOb.setAlignment(self.textAlignment)
        textOb.setGeometry(*self.positionAdjust) 

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

    def centerAlign(self):
        self.positionAdjust[1] = int(self.positionAdjust[1] - self.positionAdjust[3]/2)
            
    def makeButton(self):
        button = QPushButton(self.text, self.window)
        button.setGeometry(*(int(x) for x in self.positionAdjust))    
        button.setFont(self.font)
        # button.setWordWrap = True
        button.setStyleSheet("QPushButton { text-align: center; }")
        # button.setMinimumSize(self.positionAdjust[2], self.positionAdjust[3])
        
        return button

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

    def centerAlign(self):
        self.positionAdjust[1] = int(self.positionAdjust[1] - self.positionAdjust[3]/2)
            
    def makeEditTextBox(self):        
        editBox = QLineEdit(self.window) # Make edit box
        editBox.setText(self.startingText)
        editBox.setFont(self.font)              
        editBox.setFixedWidth(self.positionAdjust[2])  # Set the width of the text box to fit the text, with added padding
        editBox.setAlignment(self.textAlignment) 
        editBox.setGeometry(*(int(x) for x in self.positionAdjust))

def centerWindowOnScreen(window, app):
    frameGm = window.frameGeometry()
    screen = app.primaryScreen()
    centerPoint = screen.availableGeometry().center()
    frameGm.moveCenter(centerPoint)
    window.move(frameGm.topLeft())        

def main():

    # Predefined sizes
    padding_small = 5
    padding_medium = 10
    padding_large = 20
    width_ST_chooseTime = 400
    startingY_checkBox = 160
    width_toggle = 22
    width_ST_startupToggle = 300
    width_text_startupFolder = 230
    height_text_startupFolder = 50
    width_button_change = 45

    # Step 1: Create the main application object
    app = QApplication(sys.argv)

    # Step 2: Create the main window object
    window = QMainWindow()

    # Step 3: Set window title
    window.setWindowTitle('My PyQt5 Window')

    # Step 4: Set window size
    window.resize(800, 600)

    # Fonts
    fonts = Fonts()
    fonts.makeFonts()

    # Static text - choose time (top left)
    text = 'Choose time for daily word definition to appear (24 hour clock):'
    textAlignment = Qt.AlignRight | Qt.AlignVCenter | Qt.TextWordWrap    
    position = (padding_medium, padding_medium, width_ST_chooseTime, 0)
    ST_chooseTime = StaticText(window,fonts.font_medium,text,position,textAlignment)
    ST_chooseTime.makeTextObject()

    rightMostPoint = ST_chooseTime.positionAdjust[0] + ST_chooseTime.positionAdjust[2]
    centerV = ST_chooseTime.Vcenter

    # Edit text box - enter hours (top right)    
    position = (rightMostPoint+padding_large,centerV,width_button_change,0)
    ET_hours = EditText(window,fonts.font_medium,"HH",position)
    ET_hours.centerAlign()    
    ET_hours.forceWidth()
    ET_hours.makeEditTextBox()

    rightMostPoint = rightMostPoint + padding_large + ET_hours.positionAdjust[2]

    # Static text - colon (top right)
    position = (rightMostPoint+padding_small, centerV, 0, 0)
    textAlignment = Qt.AlignCenter | Qt.AlignVCenter
    ST_colon = StaticText(window,fonts.font_medium,":",position,textAlignment)
    ST_colon.centerAlign()
    ST_colon.makeTextObject()

    rightMostPoint = rightMostPoint + padding_small + ST_colon.positionAdjust[2]

    # Edit text box - enter minutes (top right)
    position = (rightMostPoint+padding_small,centerV,width_button_change,0)
    ET_mins = EditText(window,fonts.font_medium,"MM",position)
    ET_mins.centerAlign()    
    ET_mins.forceWidth()    
    ET_mins.makeEditTextBox()

    rightMostPoint_topRow = position[0] + ET_mins.positionAdjust[2]

    # Toggle button - add to startup folder (bottom left)
    toggle_startup = QCheckBox('', window)
    toggle_startup.setGeometry(padding_large,startingY_checkBox,width_toggle,width_toggle)
    toggle_startup.setStyleSheet(f"QCheckBox::indicator {{ width: {width_toggle}px; height: {width_toggle}px; }}")
    toggle_startup.setChecked(False)

    rightMostPoint = padding_large + width_toggle
    centerV_toggleButton = startingY_checkBox + width_toggle/2

    # Static text - Add program to startup folder (bottom left)
    text = 'Add program to startup folder (needed to keep program running after computer reboot)'
    textAlignment = Qt.AlignLeft | Qt.AlignVCenter | Qt.TextWordWrap    
    position = (rightMostPoint+padding_medium, centerV_toggleButton, width_ST_startupToggle, 0)    
    ST_startup = StaticText(window,fonts.font_small,text,position,textAlignment)
    ST_startup.centerAlign()
    ST_startup.makeTextObject()

    rightMostPoint_startupText = position[0] + position[2]
    lowestPoint = ST_startup.positionAdjust[1] + ST_startup.positionAdjust[3]

    # Get and show startup folder
    position = (padding_large,lowestPoint+padding_large,width_text_startupFolder,height_text_startupFolder)
    getAndShowStartupFolder = GetAndShowStartupFolder(position, window)
    
    centerV = position[1] + position[3]/2
    rightMostPoint = position[0] + position[2] 
    
    # Make 'change' startup folder button
    text = 'Change'      
    position = (rightMostPoint+padding_medium,centerV,0,0)
    PB_change = PushButton(window,fonts.font_medium,text,position)
    PB_change.centerAlign()
    button_change = PB_change.makeButton()
    # Make slot for button for when it is pressed
    button_change.clicked.connect(getAndShowStartupFolder.updatePath)

    # Start button
    text = 'Start'
    position = (rightMostPoint_startupText+padding_large, centerV_toggleButton, 0, 0)
    PB_start = PushButton(window,fonts.font_large_bold,text,position)
    PB_start.centerAlign()
    button_start = PB_start.makeButton()
    # button_start.clicked.connect(lambda: startButtonPressed(function inputs...))

    # Step 5: Center the window - put in the function (pass it 'window' and 'app')
    centerWindowOnScreen(window, app)

    # Step 5: Show the window
    window.show()

    # Step 6: Run the application's event loop
    sys.exit(app.exec_())

main()        

