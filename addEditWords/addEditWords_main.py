import sys, os
import json

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtGui import QPainter, QPen

from commonClassesFunctions.functionsClasses import centerWindowOnScreen, getScreenWidthHeight, Fonts, StaticText, readJSONfile, PushButton

from .addEditWords_functionsClasses import Sizes_addEditWords, addNewWordTextBoxes, makeWordList

from PyQt5.QtCore import Qt

class DeleteWordDialog(QDialog):
    def __init__(self, fonts, window):
        # Inheritance
        super().__init__(window)
        # Inputs
        self.fonts = fonts
        self.window = window        
        # Some dialog sizes
        self.width = 200
        self.height = 100
                
        self.setWindowTitle('Confirm Deletion')
        self.setFixedSize(self.width, self.height)  # Set a fixed size for the dialog

        # Delete word text
        text = 'Delete word?'
        textAlignment = Qt.AlignCenter
        textPos = (self.width/2, 20, 0, 0)
        ST_deleteWord = StaticText(window,fonts.font_large_bold,text,textPos,textAlignment)         
        ST_deleteWord.centerAlign_H()
        ST_deleteWord.makeTextObject()

        # # Add 'Ok' button with manual positioning
        # ok_button = QPushButton('Ok', self)
        # ok_button.setGeometry(30, 50, 60, 30)
        # ok_button.clicked.connect(self.accept)

        # # Add 'Cancel' button with manual positioning
        # cancel_button = QPushButton('Cancel', self)
        # cancel_button.setGeometry(110, 50, 60, 30)
        # cancel_button.clicked.connect(self.reject)    

    def makeDeleteDialog(self):
        self.exec_()

def open_dialog(sizes, fonts, window):
    dialog = DeleteWordDialog(sizes, fonts, window)
    dialog.exec_()  # Open the dialog in a modal way        

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
    ST_addWordsTitle.makeTextObject()

    lowestPoint = ST_addWordsTitle.positionAdjust[1] + ST_addWordsTitle.positionAdjust[3]

    # Small label for 'Add word' edit text box
    text = 'Add word'
    textAlignment = Qt.AlignVCenter | Qt.AlignLeft
    textPos = (sizes.padding_large, lowestPoint+sizes.padding_large, 0, 0)
    ST_addWordLabel = StaticText(window,fonts.font_medium,text,textPos,textAlignment)         
    ST_addWordLabel.makeTextObject()

    # Small label for 'Add definition' edit text box
    text = 'Add definition'
    textAlignment = Qt.AlignVCenter | Qt.AlignLeft
    leftPos = sizes.padding_large + width_addWord + sizes.padding_large
    textPos = (leftPos, lowestPoint+sizes.padding_large, 0, 0)
    ST_addDefLabel = StaticText(window,fonts.font_medium,text,textPos,textAlignment)         
    ST_addDefLabel.makeTextObject()

    lowestPoint = ST_addDefLabel.positionAdjust[1] + ST_addDefLabel.positionAdjust[3]

    # Make edit text boxes to add a new word and definition
    editTextBoxes_addWord = addNewWordTextBoxes(window,sizes,fonts,data,curFilePath)
    editTextBoxes_addWord.makeAddWordEditTextBox(sizes.padding_large,lowestPoint+sizes.padding_small, width_addWord)
    editTextBoxes_addWord.makeAddDefEditTextBox(leftPos,lowestPoint+sizes.padding_small,width_addDefinition)

    lowestPoint = editTextBoxes_addWord.addDefInput.y() + editTextBoxes_addWord.addDefInput.height()

    # 'Add' button
    text = 'Add'      
    position = (sizes.padding_large,lowestPoint+sizes.padding_large,0,0)
    pushButton_Add = PushButton(window,fonts.font_mediumLarge,text,position) 
    pushButton_Add.setButtonPadding(14,7)
    AddButton = pushButton_Add.makeButton()     
    AddButton.clicked.connect(editTextBoxes_addWord.AddButtonPressed)
    AddButton.clicked.connect(lambda: wordList.updateAPIwithNewEntry(editTextBoxes_addWord.newWord,\
                                        editTextBoxes_addWord.newDefinition))

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
    ST_editWordsTitle.makeTextObject()

    lowestPoint = ST_editWordsTitle.positionAdjust[1] + ST_editWordsTitle.positionAdjust[3]

    # Make the word list in the edit words section
    startingY = lowestPoint + sizes.padding_large*2
    wordList = makeWordList(data,fonts,sizes,width,height,startingY,window)
       
    # Center the window - put in the function (pass it 'window' and 'app')
    centerWindowOnScreen(window, app)

    # Show window
    window.show()

    # Run application's event loop
    sys.exit(app.exec_())
    
main()    
