import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QLabel,  QLineEdit, QFileDialog, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFontMetrics, QFont
from PyQt5.QtCore import Qt
import os
import platform

# Functions

# Implement button clicked - action
def startButtonPressed(toggle_button,getStartupFolder,window):
    toggle_state = toggle_button.isChecked() # if true, add relevant file to startup folder
    print(f'winky woo {getStartupFolder.startupFolder}')
    # Store the time in which the program should run
    # Change the binary boolean file to 1 (true), for program now running
    # Anything else
    window.close() # Close the window

class GetAndShowStartupFolder:
    def __init__(self):
        self.startupFolder = self.getStartupFolderAutomatically()

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

    def manuallySelectPath(self):
        file_dialog = QFileDialog()
        selected_path = file_dialog.getExistingDirectory(None, "Select Folder")
        return selected_path

    def updatePath(self):
        new_folder = self.manuallySelectPath()
        if new_folder:
            self.startupFolder = new_folder

class StaticText:
    def __init__(self, window, font, text, position, alignment):
        # Default values
        self.wordWrap = True
        # Input values
        self.window = window
        self.font = font
        self.text = text
        self.position = position
        self.alignment = alignment

    def makeTextObject(self):
        textOb = QLabel(self.text, self.window)
        textOb.setWordWrap(self.wordWrap)    
        textOb.setGeometry(*(int(x) for x in self.position))    
        textOb.setFont(self.font)
        textOb.setAlignment(self.alignment)

def getVheightAndCenter(fontMetrics,width,text,startY):
    # Get height and vertical center point of text using its defined width and starting y point
    bounding_rect = fontMetrics.boundingRect(0, 0, width, 0, Qt.TextWordWrap, text)
    height = bounding_rect.height()
    centerRow = startY + height/2
    return height, centerRow

class EditText:
    def __init__(self, window, font, startingText, position):
        # Default values
        self.extraWidthAroundText = 10
        self.alignment = Qt.AlignCenter | Qt.AlignVCenter
        # Inputs
        self.window = window
        self.font = font
        self.startingText = startingText
        self.position = position    

    def makeEditTextBox(self):        
        editBox = QLineEdit(self.window) # Make edit box
        editBox.setText(self.startingText)
        editBox.setFont(self.font)
        font_metrics = QFontMetrics(editBox.font())  # Get the font metrics for the current font of the text box
        text_width = font_metrics.horizontalAdvance(editBox.text())  # Calculate the width of the text within the text box
        editBox.setFixedWidth(text_width+self.extraWidthAroundText)  # Set the width of the text box to fit the text, with added padding
        editBox.setAlignment(self.alignment) 
        editBox.setGeometry(*(int(x) for x in self.position))

def getButtonPosition(fontMetrics,startingX,centerV,text,padding):
    bounding_rect = fontMetrics.boundingRect(0, 0, 0, 0, Qt.AlignLeft, text)
    height = bounding_rect.height()
    halfHeight = height/2
    width = bounding_rect.width()
    position = (startingX,centerV-halfHeight-padding,\
                width+padding*2,height+padding*2)
    return position

def getTextWidthAndHeight(fontMetrics,text):
    bounding_rect = fontMetrics.boundingRect(0,0,0,0, Qt.AlignLeft, text)
    width = bounding_rect.width()
    height = bounding_rect.height()
    return width, height

     

def main():

    # Fonts
    font_small = QFont()
    font_small.setPointSize(9)  # Set font size
    font_small.setBold(False)     # Set font to bold
    font_medium = QFont()
    font_medium.setPointSize(11)  # Set font size
    font_medium.setBold(False)     # Set font to bold
    font_large = QFont()
    font_large.setPointSize(16)  # Set font size
    font_large.setBold(False)     # Set font to bold
    # Font metrics for each font
    fontMetrics_small = QFontMetrics(font_small)
    fontMetrics_medium = QFontMetrics(font_medium)

    # Predefined sizes
    padding_small = 5
    padding_medium = 10
    padding_large = 20
    width_ST_chooseTime = 400
    startingY_checkBox = 175
    width_toggle = 22
    width_ST_startupToggle = 300

    # Found sizes

    # Text
    t_chooseTime = 'Choose time for daily word definition to appear (24 hour clock):'
    t_startupToggle = 'Add program to startup folder (needed to keep program running after computer reboot)'


    # Step 1: Create the main application object
    app = QApplication(sys.argv)

    # Step 2: Create the main window object
    window = QMainWindow()

    # Step 3: Set window title
    window.setWindowTitle('My PyQt5 Window')

    # Step 4: Set window size
    window.resize(800, 600)

    # Static text - choose time (top left)
    height, centerV = getVheightAndCenter(fontMetrics_medium,width_ST_chooseTime,t_chooseTime,padding_large)
    position = (padding_large, padding_large, width_ST_chooseTime, height+padding_small)
    alignment = Qt.AlignRight | Qt.AlignVCenter
    ST_chooseTime = StaticText(window,font_medium,t_chooseTime,position,alignment)
    ST_chooseTime.makeTextObject()

    rightMostPoint = padding_large + width_ST_chooseTime

    # Edit text box - enter hours (top right)
    position_ET_hours = getButtonPosition(fontMetrics_medium,rightMostPoint+padding_large,centerV,"HH",padding_small)
    ET_hours = EditText(window,font_medium,"HH",position_ET_hours)
    ET_hours.makeEditTextBox()

    rightMostPoint = rightMostPoint + padding_large + position_ET_hours[2]

    # Static text - colon (top right)
    width, height = getTextWidthAndHeight(fontMetrics_medium,":")
    position = (rightMostPoint+padding_small, centerV-height/2, width, height)
    alignment = Qt.AlignCenter | Qt.AlignVCenter
    ST_colon = StaticText(window,font_medium,":",position,alignment)
    ST_colon.makeTextObject()

    rightMostPoint = rightMostPoint + padding_small + width

    # Edit text box - enter minutes (top right)
    position_ET_mins = getButtonPosition(fontMetrics_medium,rightMostPoint+padding_small,centerV,"MM",padding_small)
    ET_mins = EditText(window,font_medium,"MM",position_ET_mins)
    ET_mins.makeEditTextBox()

    rightMostPoint_topRow = rightMostPoint + padding_small + position_ET_mins[2]

    # Toggle button - add to startup folder (bottom left)
    toggle_startup = QCheckBox('', window)
    toggle_startup.setGeometry(padding_large,startingY_checkBox,width_toggle,width_toggle)
    toggle_startup.setStyleSheet(f"QCheckBox::indicator {{ width: {width_toggle}px; height: {width_toggle}px; }}")
    toggle_startup.setChecked(False)

    rightMostPoint = padding_large + width_toggle
    centerV = startingY_checkBox + width_toggle/2

    # Static text - Add program to startup folder (bottom left)
    height, _ = getVheightAndCenter(fontMetrics_small,width_ST_startupToggle,t_startupToggle,padding_large)
    position = (rightMostPoint+padding_medium, centerV-height/2, width_ST_startupToggle, height)
    alignment = Qt.AlignLeft | Qt.AlignVCenter
    ST_startup = StaticText(window,font_small,t_startupToggle,position,alignment)
    ST_startup.makeTextObject()

    rightMostPoint = rightMostPoint + padding_medium + width_ST_startupToggle
    lowestPoint = centerV+height/2

    # # Get startup folder - first automatically, but also create button for manual selection
    # getAndShowStartupFolder = GetAndShowStartupFolder()
    # browse_button = QPushButton('Browse', window)
    # browse_button.clicked.connect(getAndShowStartupFolder.updatePath)

    # # Create an implement button and add it to the layout
    # implement_button = QPushButton('Start', window) # create an implement button
    # layout.addWidget(implement_button) # add the implement button to the vertical layout
    # # Slot
    # implement_button.clicked.connect(lambda: startButtonPressed(toggle_button,getStartupFolder,window))

    # Step 5: Center the window - put in the function (pass it 'window' and 'app')
    frameGm = window.frameGeometry()
    screen = app.primaryScreen()
    centerPoint = screen.availableGeometry().center()
    frameGm.moveCenter(centerPoint)
    window.move(frameGm.topLeft())

    # Step 5: Show the window
    window.show()

    # Step 6: Run the application's event loop
    sys.exit(app.exec_())

main()        

