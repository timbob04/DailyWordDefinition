
# Intial
# Functions for:
# 1) Getting the words and finding the right one - class, with methods getWOD and getROD
# 2) Making the API
# 3) Collecting any user input and adjusting the word/definition/code list

import os

from .PresentWordsAndDefinitions_functionsClasses import readJSONfile, WODandDef, RODandDef, Sizes_presentWODAPI

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

from commonClassesFunctions.functionsClasses import Fonts, calculateTextboxDim, centerWindowOnScreen

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
    textAlignment = Qt.AlignRight | Qt.AlignTop | Qt.TextWordWrap  
    fonts.font_medium
    text = WOD + ": " + WOD_definition
    textHeight_WOD = calculateTextboxDim(text, sizes.WODwidth, fonts.font_medium, textAlignment)

    
    


    # Resize window
    rightMostPoint_final = max(rightMostPoint_botRow,rightMostPoint_topRow)
    window.resize(rightMostPoint_final+sizes.padding_large, lowestPoint+sizes.padding_large)

    # Center the window - put in the function (pass it 'window' and 'app')
    centerWindowOnScreen(window, app)

    # Show window
    window.show()

    # Run application's event loop
    sys.exit(app.exec_())

    


main()    