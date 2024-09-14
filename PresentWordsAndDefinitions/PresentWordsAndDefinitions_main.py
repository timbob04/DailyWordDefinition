
# Intial
# Functions for:
# 1) Getting the words and finding the right one - class, with methods getWOD and getROD
# 2) Making the API
# 3) Collecting any user input and adjusting the word/definition/code list

import os

from .PresentWordsAndDefinitions_functionsClasses import readJSONfile, WODandDef, PODandDef, Sizes_presentWODAPI, ToggleChoices, addWODtogglePressed, remPODtogglePressed

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox
import sys

from commonClassesFunctions.functionsClasses import Fonts, MakeTextWithMaxHeight, centerWindowOnScreen, StaticText, PushButton




 

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
    curPODandDef = PODandDef(data, curFilePath)
    POD, POD_definition = curPODandDef.getAndreturnPOD()
 
    print(f"WOD is: {WOD}.  Def is: {WOD_definition}")
    print(f"POD is: {POD}.  Def is: {POD_definition}")

    fonts = Fonts()
    fonts.makeFonts()

    # Get the text height for the WOD and its definition
    textAlignment = Qt.AlignLeft | Qt.AlignTop 
    text = WOD + ": " + WOD_definition 
    makeTextWithMaxHeight_WOD = MakeTextWithMaxHeight(window,text,sizes.padding_large, \
                                                  sizes.padding_large,sizes.WODwidth, \
                                                  sizes.maxWODheight,fonts.font_mediumLarge,\
                                                    textAlignment)     
    # Make the text using the WOD without definition to start
    makeTextWithMaxHeight_WOD.text = WOD + ": "
    makeTextWithMaxHeight_WOD.makeText()
    # Adjust the text inside makeTextWithMaxHeight_WOD for chaning later when the reveal button is pressed
    makeTextWithMaxHeight_WOD.text = WOD + ": " + WOD_definition
    
    rightMostPoint = sizes.padding_large + sizes.WODwidth
    lowestPoint = sizes.padding_large + makeTextWithMaxHeight_WOD.textPos[3]  
    centerH_WOD = makeTextWithMaxHeight_WOD.textPos[0] + ( makeTextWithMaxHeight_WOD.textPos[2] / 2 ) 

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
    toggle_addWOD.hide()
    toggle_addWOD.clicked.connect(lambda: addWODtogglePressed(toggle_addWOD,toggleChoices))

    centerH = textPos[0] + ( textPos[2] / 2 )
    leftPoint_toggleWOD = leftPoint

    # Toggle button text - Add WOD
    text = 'Add word to priority word list'
    textAlignment = Qt.AlignCenter | Qt.AlignTop | Qt.TextWordWrap       
    topPoint = topPoint + sizes.width_toggle + sizes.padding_small
    textPos = (centerH, topPoint, sizes.smallTextWidth, 0)
    ST_addWODtext = StaticText(window,fonts.font_small,text,textPos,textAlignment)     
    ST_addWODtext.centerAlign_H()

    rightMostPoint = centerH + sizes.smallTextWidth
    lowestPoint = max(lowestPoint,topPoint+ST_addWODtext.positionAdjust[3])
    rightMostPoint_top = rightMostPoint

    # Make 'Reveal word definition' button and define its actions (clicked.connect)
    text = 'Reveal word definition'      
    position = (sizes.padding_large,lowestPoint+sizes.padding_large,0,0)
    pushButton = PushButton(window,fonts.font_medium,text,position)     
    revealButton = pushButton.makeButton()
    # Actions for when the reveal button is pressed (more for other text/buttons/etc defined below)
    revealButton.clicked.connect(makeTextWithMaxHeight_WOD.editText) # reveal the WOD and its defintion
    revealButton.clicked.connect(lambda: toggle_addWOD.show()) # reveal toggle to add WOD to priority words    
    revealButton.clicked.connect(ST_addWODtext.makeTextObject) # reeal text for the add WOD toggle

    lowestPoint = lowestPoint + pushButton.positionAdjust[3] + sizes.padding_large  

    # Print the priority word title
    text = 'Priority word of day'
    textAlignment = Qt.AlignCenter    
    topPoint = lowestPoint + sizes.padding_large
    textPos = (centerH_WOD, topPoint, sizes.PODwidth, 0)
    ST_PODtitle = StaticText(window,fonts.font_small_italic_bold,text,textPos,textAlignment)     
    ST_PODtitle.centerAlign_H()
    revealButton.clicked.connect(ST_PODtitle.makeTextObject)    

    lowestPoint = ST_PODtitle.positionAdjust[1] + ST_PODtitle.positionAdjust[3]
    topPoint_PODtitle = topPoint

    # Print the priority word
    textAlignment = Qt.AlignHCenter | Qt.AlignTop 
    text = POD + ": " + POD_definition  
    makeTextWithMaxHeight_POD = MakeTextWithMaxHeight(window,text,centerH_WOD, \
                                                  lowestPoint + sizes.padding_small,sizes.PODwidth, \
                                                  sizes.maxPODheight,fonts.font_small_italic,\
                                                    textAlignment)     
    # Make the text initially blank, and then have this updated to the POD when the reveal button is pressed
    makeTextWithMaxHeight_POD.centerH()
    makeTextWithMaxHeight_POD.text = ""
    makeTextWithMaxHeight_POD.makeText()
    makeTextWithMaxHeight_POD.text = text
    revealButton.clicked.connect(makeTextWithMaxHeight_POD.editText)    

    lowestPoint = lowestPoint + makeTextWithMaxHeight_POD.textPos[3]    
    rightMostPoint = makeTextWithMaxHeight_POD.textPos[0] + makeTextWithMaxHeight_POD.textPos[2]

    # Toggle button - Remove word from priority word list
    toggle_remPOD = QCheckBox('', window)
    leftPoint = leftPoint_toggleWOD
    topPoint = topPoint_PODtitle
    textPos = (leftPoint,topPoint,sizes.width_toggle,sizes.width_toggle)
    toggle_remPOD.setGeometry(*(int(x) for x in textPos))
    toggle_remPOD.setStyleSheet(f"QCheckBox::indicator {{ width: {sizes.width_toggle}px; height: {sizes.width_toggle}px; }}")
    toggle_remPOD.setChecked(False)
    toggle_remPOD.hide()
    toggle_remPOD.clicked.connect(lambda: remPODtogglePressed(toggle_remPOD,toggleChoices))
    revealButton.clicked.connect(lambda: toggle_remPOD.show())

    centerH = textPos[0] + (textPos[2] / 2)

    # Toggle button text - Rem POD
    text = 'Remove word from priority word list'
    textAlignment = Qt.AlignCenter | Qt.AlignTop | Qt.TextWordWrap   
    topPoint = topPoint + sizes.width_toggle + sizes.padding_small
    textPos = (centerH, topPoint, sizes.smallTextWidth, 0)
    ST_remPODtext = StaticText(window,fonts.font_small,text,textPos,textAlignment) 
    ST_remPODtext.centerAlign_H()
    # ST_remPODtext.makeTextObject()
    revealButton.clicked.connect(ST_remPODtext.makeTextObject)

    rightMostPoint = leftPoint + sizes.smallTextWidth
    lowestPoint = max(lowestPoint,ST_remPODtext.positionAdjust[1]+ST_remPODtext.positionAdjust[3])


    rightMostPoint_bottom = rightMostPoint
    rightMostPoint_all = max(rightMostPoint_top,rightMostPoint_bottom) 


    # Resize window
    window.resize(int(rightMostPoint_all+sizes.padding_large), int(lowestPoint+sizes.padding_large))

    # Center the window - put in the function (pass it 'window' and 'app')
    centerWindowOnScreen(window, app)

    # Show window
    window.show()

    # Run application's event loop
    sys.exit(app.exec_())
    
main()    
