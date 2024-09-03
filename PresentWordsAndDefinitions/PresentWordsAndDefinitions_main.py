
# Intial
# Functions for:
# 1) Getting the words and finding the right one - class, with methods getWOD and getROD
# 2) Making the API
# 3) Collecting any user input and adjusting the word/definition/code list

import os

from .PresentWordsAndDefinitions_functionsClasses import readJSONfile, WODandDef, RODandDef, Sizes_presentWODAPI, ToggleChoices, addWODtogglePressed

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox
import sys

from PyQt5.QtGui import QTextDocument

from commonClassesFunctions.functionsClasses import Fonts, MakeTextWithMaxHeight, centerWindowOnScreen, StaticText

def main():

    # Make window
    app = QApplication(sys.argv)
    window = QMainWindow()    
    window.setWindowTitle('Program not currently running')

    # Predefined sizes of things
    sizes = Sizes_presentWODAPI()
    sizes.defineSizes()    
    
    # Get path of accessory files
    base_dir = os.path.dirname(os.path.abspath(__file__))
    accessoryFiles_dir = os.path.join(base_dir, '..', 'accessoryFiles')
    # Write time to run program to .txt file
    curFilePath = os.path.join(accessoryFiles_dir, 'WordsDefsCodes.json')

    # Read WordsDefsCodes.json
    data = readJSONfile(curFilePath)

    # Get WOD and its definition (and update JSON file accordingly)
    curWODandDef = WODandDef(data, curFilePath)
    WOD, WOD_definition = curWODandDef.getAndreturnWOD()

    # Get ROD and its definition (and update JSON file accordingly)
    curRODandDef = RODandDef(data, curFilePath)
    ROD, ROD_definition = curRODandDef.getAndreturnROD()
 
    print(f"WOD is: {WOD}.  Def is: {WOD_definition}")
    print(f"Rod is: {ROD}.  Def is: {ROD_definition}")

    fonts = Fonts()
    fonts.makeFonts()

    # Get the text height for the WOD and its definition
    textAlignment = Qt.AlignLeft | Qt.AlignTop 
    text = WOD + ": " + WOD_definition
    makeTextWithMaxHeight = MakeTextWithMaxHeight(window,text,sizes.padding_large, \
                                                  sizes.padding_large,sizes.WODwidth, \
                                                  sizes.maxWODheight,fonts.font_large,\
                                                    textAlignment) 
    
    rightMostPoint = sizes.padding_large + sizes.WODwidth
    lowestPoint = sizes.padding_large + makeTextWithMaxHeight.textPos[3]  

    # Class to save the toggle button choices
    toggleChoices = ToggleChoices()

    # Toggle button - add WOD to priority word list
    toggle_addWOD = QCheckBox('', window)
    leftPoint = rightMostPoint + sizes.padding_large + (sizes.smallTextWidth/2) - (sizes.width_toggle/2)
    topPoint = sizes.padding_large + sizes.padding_medium
    textPos = (leftPoint,topPoint,sizes.width_toggle,sizes.width_toggle)
    toggle_addWOD.setGeometry(*(int(x) for x in textPos))
    toggle_addWOD.setStyleSheet(f"QCheckBox::indicator {{ width: {sizes.width_toggle}px; height: {sizes.width_toggle}px; }}")
    toggle_addWOD.setChecked(False)
    toggle_addWOD.clicked.connect(lambda: addWODtogglePressed(toggle_addWOD,toggleChoices))

    text = 'Add word to priority word list'
    textAlignment = Qt.AlignCenter | Qt.AlignTop | Qt.TextWordWrap   
    leftPoint = rightMostPoint + sizes.padding_large
    topPoint = topPoint + sizes.width_toggle + sizes.padding_small
    textPos = (leftPoint, topPoint, sizes.smallTextWidth, 0)
    ST_addWODtext = StaticText(window,fonts.font_small,text,textPos,textAlignment)
    ST_addWODtext.makeTextObject()

    rightMostPoint = leftPoint + sizes.smallTextWidth
    lowestPoint = max(lowestPoint,topPoint+ST_addWODtext.positionAdjust[3])

    # Resize window
    window.resize(int(rightMostPoint+sizes.padding_large), int(lowestPoint+sizes.padding_large))

    # Center the window - put in the function (pass it 'window' and 'app')
    centerWindowOnScreen(window, app)

    # Show window
    window.show()

    # Run application's event loop
    sys.exit(app.exec_())
    
main()    
