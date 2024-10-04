import sys, os

from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt5.QtGui import QPainter, QPen

from commonClassesFunctions.functionsClasses import centerWindowOnScreen, getScreenWidthHeight, Fonts, StaticText, readJSONfile, PushButton

from .addEditWords_functionsClasses import Sizes_addEditWords, addWordToJSONfile

from PyQt5.QtCore import Qt

class makeWordList:
    ###### Temp notes
    # The list will be in reverse order (newest words at top)
    # Once I get the total height of all words/defs, either use a vertical scale bar, or not
    # For this above, make sure to save some space on the right for this appear
    # Also, I want to do this for the edit words section only, without including the 'Edit words' title, or the small 'Priority words' and 'Word: definition' titles
    # For this, I will use QScrollArea for this bottom section if the contents are too tall, or just regular coding (not QScrollArea) if not
    def __init__(self,dataIn):
        # Inputs
        self.dataIn = dataIn
        # Predefined
        self.Vspacing_wordDefs = 50 # the vertical spacing between each word/def
        self.Hspacing_1 = 10 # horizontal spacing for the word/def lines - option 1
        self.Hspacing_2 = 20 # horizontal spacing for the word/def lines - option 2
        self.Hspacing_word = 100

    def getHorizontalSpacing(self):
        print("Here figure out the horizontal spacing for each main area")    
        # priority word toggle button (need to consider its title)
        # Delete button - get its width (with button padding)
        # Edit button - get its width (with button padding)
        # Word width (predefined) - will need to decide what to do if longer than box (make this unilikely using the box size, and the word's fontsize)
        # Definition box width (remaining left over)
        # And all the horizontal spacing between these things (predefined)

    def getAllWordDefs_oneLine(self):
        print("Here get all the words and defs on one line for each word/def")    

    def wordDefHeights(self):
        print("Here figure out the height of each word/def, and the total height of all word/defs (with the spacing between)")    

    def makeWordDefList(self):
        print("Here I will make the word and def list with all the extras - delete buttons, etc")
        # I will need to store a handle to each thing (toggle button, StaticText, etc).
        # For this, I can use a widget to handle a single toggle/button/button/word/def entry for each word/def (chatGPT chat).
        # The entries are 1) priority toggle button, delete button, edit button, word text, definition text

    def updateListWithNewEntry(newWord,newDef):
        print("Here update the list, putting the new word/def at the top")


def main():

    # Make window
    app = QApplication(sys.argv)    
    window = QMainWindow()    
    window.setWindowTitle('Add/edit words')

    # Import some fonts
    fonts = Fonts()
    fonts.makeFonts()

    # Get path of accessory files
    base_dir = os.path.dirname(os.path.abspath(__file__))
    accessoryFiles_dir = os.path.join(base_dir, '..', 'accessoryFiles')
    # Path to json file for words and definitions
    curFilePath = os.path.join(accessoryFiles_dir, 'WordsDefsCodes.json')

    # Read WordsDefsCodes.json
    data = readJSONfile(curFilePath)

    # Predefined sizes of things
    sizes = Sizes_addEditWords()
    sizes.defineSizes() 

    # Get the monitor width and height
    monWidth, monHeight = getScreenWidthHeight(app)

    # Determine the API width and height to use
    width = min(sizes.APIwidth,monWidth)
    height = min(sizes.APIheight,monHeight)

    # Determine enter text box widths
    availableWidth = width - (sizes.padding_large*3)
    width_addWord = availableWidth / 4
    width_addDefinition = availableWidth - width_addWord

    # Size API 
    window.resize(int(width), int(height))

    # Add words title
    text = 'Add words'
    textAlignment = Qt.AlignCenter
    textPos = (sizes.padding_large, sizes.padding_large, 0, 0)
    ST_addWordsTitle = StaticText(window,fonts.font_large_bold,text,textPos,textAlignment)         
    addWordsTitle = ST_addWordsTitle.makeTextObject()

    lowestPoint = ST_addWordsTitle.positionAdjust[1] + ST_addWordsTitle.positionAdjust[3]

    # Small label for 'Add word' edit text box
    text = 'Add word'
    textAlignment = Qt.AlignCenter
    textPos = (sizes.padding_large, lowestPoint+sizes.padding_large, 0, 0)
    ST_addWordLabel = StaticText(window,fonts.font_medium,text,textPos,textAlignment)         
    addWordLabel = ST_addWordLabel.makeTextObject()

    # Small label for 'Add definition' edit text box
    text = 'Add definition'
    textAlignment = Qt.AlignCenter
    leftPos = sizes.padding_large + width_addWord + sizes.padding_large
    textPos = (leftPos, lowestPoint+sizes.padding_large, 0, 0)
    ST_addDefLabel = StaticText(window,fonts.font_medium,text,textPos,textAlignment)         
    addDefLabel = ST_addDefLabel.makeTextObject()

    lowestPoint = ST_addDefLabel.positionAdjust[1] + ST_addDefLabel.positionAdjust[3]

    # Edit text box to add word
    addWordInput = QLineEdit(window)    
    addWordInput.setGeometry(sizes.padding_large, lowestPoint+sizes.padding_small, int(width_addWord), 40 )
    addWordInput.setFont(fonts.font_mediumLarge)
    addWordInput.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    addWordInput.setStyleSheet("QLineEdit { border: 1px solid black; }")

    # Edit text box to add definition
    addDefInput = QLineEdit(window)    
    addDefInput.setGeometry(int(leftPos), lowestPoint+sizes.padding_small, int(width_addDefinition), 40 )
    addDefInput.setFont(fonts.font_mediumLarge)
    addDefInput.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    addDefInput.setStyleSheet("QLineEdit { border: 1px solid black; }")

    lowestPoint = addDefInput.y() + addDefInput.height()

    # 'Add' button
    text = 'Add'      
    position = (sizes.padding_large,lowestPoint+sizes.padding_large,0,0)
    pushButton_Add = PushButton(window,fonts.font_mediumLarge,text,position) 
    pushButton_Add.setButtonPadding(14,7)
    AddButton = pushButton_Add.makeButton()          
    AddButton.clicked.connect(lambda: addWordToJSONfile(curFilePath,data,addWordInput,addDefInput))
    AddButton.clicked.connect(addWordInput.clear)
    AddButton.clicked.connect(addDefInput.clear)

    lowestPoint = pushButton_Add.positionAdjust[1] + pushButton_Add.positionAdjust[3]

    # Draw a line to separate the 'Add words' and 'Edit words' main sections
    x_start = sizes.padding_large
    x_end = width - sizes.padding_large
    y_start = lowestPoint + (sizes.padding_large*2)
    y_end = lowestPoint + (sizes.padding_large*2)
    def custom_paint(event):
        painter = QPainter(window)
        pen = QPen(Qt.gray, 10)  # Set the color and thickness of the line
        painter.setPen(pen)
        painter.drawLine(x_start,y_start,x_end,y_end)  # Draw the line
    window.paintEvent = custom_paint

    lowestPoint = y_start

    # Edit words title
    text = 'Edit words'
    textAlignment = Qt.AlignCenter
    textPos = (sizes.padding_large, lowestPoint + sizes.padding_large, 0, 0)
    ST_editWordsTitle = StaticText(window,fonts.font_large_bold,text,textPos,textAlignment)         
    editWordsTitle = ST_editWordsTitle.makeTextObject()

    lowestPoint = ST_editWordsTitle.positionAdjust[1] + ST_editWordsTitle.positionAdjust[3]


    # Center the window - put in the function (pass it 'window' and 'app')
    centerWindowOnScreen(window, app)

    # Show window
    window.show()

    # Run application's event loop
    sys.exit(app.exec_())
    
main()    
