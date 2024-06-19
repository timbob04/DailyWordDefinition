import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QCheckBox, QLabel,  QLineEdit, QFileDialog, QScrollArea
from PyQt5.QtGui import QFontMetrics, QFont
from PyQt5.QtCore import Qt
import os
import platform
import re

# Classes/functions/etc

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
        if startupToggle.isChecked():
            # Save startup folder
            curFilePath = os.path.join(common_dir, 'startupFolder.txt')
            with open(curFilePath, 'w') as file:
                file.write(startupFolOb.startupFolder)            
            # Here put the main program in the startup folder
            print("Here put the main exe file in the startup folder")
        # Change application running boolean to true
        curFilePath = os.path.join(common_dir, 'applicationRunning_YN.txt')
        with open(curFilePath, 'w') as file:
            file.write("1")
        # Start the main program's exe file running
        print("Here run the main program's exe file")
        # Close window
        window.close() 

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
            
    def makeButton(self):
        button = QPushButton(self.text, self.window)
        button.setGeometry(*(int(x) for x in self.positionAdjust))    
        button.setFont(self.font)
        button.setStyleSheet("QPushButton { text-align: center; }")
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

def centerWindowOnScreen(window, app):
    frameGm = window.frameGeometry()
    screen = app.primaryScreen()
    centerPoint = screen.availableGeometry().center()
    frameGm.moveCenter(centerPoint)
    window.move(frameGm.topLeft())        

def startupTogglePressed(h_toggle, h_changeButton, h_startupTextObject):
    if h_toggle.isChecked():
        h_changeButton.show()
        h_startupTextObject.textBox.show()
        h_startupTextObject.scroll_area.show()
    else:
        h_changeButton.hide()
        h_startupTextObject.textBox.hide()
        h_startupTextObject.scroll_area.hide()

class CheckTimeEntered():
    def __init__(self):        
        # Default values
        self.handleText = None
        self.correctYN_HH = False
        self.correctYN_MM = False
        self.correctYN_both = False  
        self.startButtonPressed = False # becomes true once the Start button is pressed

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
        if not self.startButtonPressed:
            return
        if self.correctYN_both:
            self.handleText.hide()
        else:
            self.handleText.show()



        

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

    # Object to check if HH and MM entered correctly
    checkTimeEntered = CheckTimeEntered()

    # Edit text box - enter hours (top right)    
    position = (rightMostPoint+padding_large,centerV,width_button_change,0)
    editText_hours = EditText(window,fonts.font_medium,"HH",position)
    editText_hours.centerAlign_V()    
    editText_hours.forceWidth()
    ET_hours = editText_hours.makeEditTextBox()
    ET_hours.textChanged.connect(checkTimeEntered.checkTime_HH) # slot for checking if HH entered correct using class CheckTimeEntered

    rightMostPoint = rightMostPoint + padding_large + editText_hours.positionAdjust[2]

    # Static text - colon (top right)
    position = (rightMostPoint+padding_small, centerV, 0, 0)
    textAlignment = Qt.AlignCenter | Qt.AlignVCenter
    ST_colon = StaticText(window,fonts.font_medium,":",position,textAlignment)
    ST_colon.centerAlign_V()
    ST_colon.makeTextObject()

    rightMostPoint = rightMostPoint + padding_small + ST_colon.positionAdjust[2]
    centerH = ST_colon.positionAdjust[0] + ST_colon.positionAdjust[2]/2

    # Edit text box - enter minutes (top right)
    position = (rightMostPoint+padding_small,centerV,width_button_change,0)
    editText_mins = EditText(window,fonts.font_medium,"MM",position)
    editText_mins.centerAlign_V()    
    editText_mins.forceWidth()    
    ET_mins = editText_mins.makeEditTextBox()
    ET_mins.textChanged.connect(checkTimeEntered.checkTime_MM) # slot for checking if MM entered correct using class CheckTimeEntered

    rightMostPoint_topRow = position[0] + editText_mins.positionAdjust[2]
    bottomOfEditBox = editText_mins.positionAdjust[1] + editText_mins.positionAdjust[3]

    # Static text - time entered incorrectly
    position = (centerH,bottomOfEditBox+padding_small,110,0)
    text = 'Time entered incorrectly'
    textAlignment = Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWordWrap 
    ST_incorrectTime = StaticText(window,fonts.font_small,text,position,textAlignment)
    ST_incorrectTime.color = 'red'
    ST_incorrectTime.centerAlign_H()
    text_incorrectTime = ST_incorrectTime.makeTextObject()
    text_incorrectTime.hide()
    checkTimeEntered.handleText = text_incorrectTime

    # Toggle button - add to startup folder (bottom left)
    toggle_startup = QCheckBox('', window)
    toggle_startup.setGeometry(padding_large,startingY_checkBox,width_toggle,width_toggle)
    toggle_startup.setStyleSheet(f"QCheckBox::indicator {{ width: {width_toggle}px; height: {width_toggle}px; }}")
    toggle_startup.setChecked(False)
    toggle_startup.clicked.connect(lambda: startupTogglePressed(toggle_startup,button_change,getAndShowStartupFolder))

    rightMostPoint = padding_large + width_toggle
    centerV_toggleButton = startingY_checkBox + width_toggle/2

    # Static text - Add program to startup folder (bottom left)
    text = 'Add program to startup folder (needed to keep program running after computer reboot)'
    textAlignment = Qt.AlignLeft | Qt.AlignVCenter | Qt.TextWordWrap    
    position = (rightMostPoint+padding_medium, centerV_toggleButton, width_ST_startupToggle, 0)    
    ST_startup = StaticText(window,fonts.font_small,text,position,textAlignment)
    ST_startup.centerAlign_V()
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
    PB_change.centerAlign_V()
    button_change = PB_change.makeButton()
    button_change.hide() # hide button until toggle is pressed
    # Make slot for button for when it is pressed
    button_change.clicked.connect(getAndShowStartupFolder.updatePath)

    # Start button
    text = 'Start'
    position = (rightMostPoint_startupText+padding_large, centerV_toggleButton, 0, 0)
    PB_start = PushButton(window,fonts.font_large_bold,text,position)
    PB_start.centerAlign_V()
    button_start = PB_start.makeButton()
    button_start.clicked.connect(lambda: startButtonPressed(window,checkTimeEntered,ET_hours.text(),ET_mins.text(),toggle_startup,getAndShowStartupFolder))


    # Center the window - put in the function (pass it 'window' and 'app')
    centerWindowOnScreen(window, app)

    # Step 5: Show the window
    window.show()

    # Step 6: Run the application's event loop
    sys.exit(app.exec_())

main()        

