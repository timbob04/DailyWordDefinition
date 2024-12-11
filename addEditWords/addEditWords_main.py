import  os
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from commonClassesFunctions.functionsClasses import centerWindowOnScreen, getScreenWidthHeight, Fonts, StaticText, PushButton
from addEditWords.addEditWords_functionsClasses import Sizes_addEditWords, addNewWordTextBoxes, makeWordList

def addEditWords():

    # Make window    
    window = QMainWindow()    
    window.setWindowTitle('Add/edit words')

    # Import some fonts
    fonts = Fonts()
    fonts.makeFonts()

    # Predefined sizes of things
    sizes = Sizes_addEditWords()
    sizes.defineSizes() 

    # Get the monitor width and height
    monWidth, monHeight = getScreenWidthHeight()

    # Determine the API width and height to use
    width = min(sizes.APIwidth,monWidth)
    height = min(sizes.APIheight,monHeight)

    # Determine enter text box widths for adding new words and definitions
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
    editTextBoxes_addWord = addNewWordTextBoxes(window,sizes,fonts)
    editTextBoxes_addWord.makeAddWordEditTextBox(sizes.padding_large,lowestPoint+sizes.padding_small, width_addWord)
    editTextBoxes_addWord.makeAddDefEditTextBox(leftPos,lowestPoint+sizes.padding_small,width_addDefinition)

    lowestPoint = editTextBoxes_addWord.addDefInput.y() + editTextBoxes_addWord.addDefInput.height()

    # 'Add' button - for adding new word/definition when user enters it
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

    # Edit words title - new big section
    text = 'Edit words'
    textAlignment = Qt.AlignCenter
    textPos = (sizes.padding_large, lowestPoint + sizes.padding_large, 0, 0)
    ST_editWordsTitle = StaticText(window,fonts.font_large_bold,text,textPos,textAlignment)         
    ST_editWordsTitle.makeTextObject()

    lowestPoint = ST_editWordsTitle.positionAdjust[1] + ST_editWordsTitle.positionAdjust[3]

    # Make the word list in the edit words section, and handle all its actions
    startingY = lowestPoint + sizes.padding_large*2
    wordList = makeWordList(fonts,sizes,width,height,startingY,window)
       
    # Center the window - put in the function (pass it 'window' and 'app')
    centerWindowOnScreen(window)

    # Show window
    window.show()
