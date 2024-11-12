import os

from .PresentWordsAndDefinitions_functionsClasses import WODandDef, PODandDef, Sizes_presentWODAPI, saveToggleChoice

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox
import sys

from commonClassesFunctions.functionsClasses import Fonts, readJSONfile, MakeTextWithMaxHeight, centerWindowOnScreen, StaticText, PushButton

def main():

    # Make window
    app = QApplication(sys.argv)    
    window = QMainWindow()    
    window.setWindowTitle('Word of the day')

    # Predefined sizes of things
    sizes = Sizes_presentWODAPI()
    sizes.defineSizes()    
    
    # Get path of accessory files
    base_dir = os.path.dirname(os.path.abspath(__file__))
    accessoryFiles_dir = os.path.join(base_dir, '..', 'accessoryFiles')
    # Path to json file for words and definitions
    curFilePath = os.path.join(accessoryFiles_dir, 'WordsDefsCodes.json')

    # Read WordsDefsCodes.json
    data = readJSONfile(curFilePath)

    # Get WOD and its definition (and update JSON file accordingly)
    curWODandDef = WODandDef(data, curFilePath)
    WOD, WOD_definition = curWODandDef.getAndreturnWOD()
    WODsPODstatus = curWODandDef.getWODsPODstatus()
    
    # Get POD and its definition (and update JSON file accordingly)
    curPODandDef = PODandDef(data, curFilePath)
    PODwithDef = curPODandDef.getAndreturnPOD()    

    # Are the WOD and POD the same?
    PODisWOD = PODwithDef[:len(WOD)] == WOD    

    fonts = Fonts()
    fonts.makeFonts()

    # Make WOD and its definition - only reveals WOD until the reveal button is pressed
    textAlignment = Qt.AlignLeft | Qt.AlignTop 
    WODwithDef = WOD + ": " + WOD_definition
    if curWODandDef.WODpresent: # if there is a word present
        text = WOD + ": "
    else:
        text = WOD
    makeTextWithMaxHeight_WOD = MakeTextWithMaxHeight(window,WODwithDef,sizes.padding_large, \
                                                  sizes.padding_large,sizes.WODwidth, \
                                                  sizes.maxWODheight,fonts.font_mediumLarge,\
                                                    textAlignment)     
    # Make the text using the WOD without definition to start
    makeTextWithMaxHeight_WOD.text = text
    makeTextWithMaxHeight_WOD.makeText()
    # Adjust the text inside makeTextWithMaxHeight_WOD for chaning later when the reveal button is pressed
    makeTextWithMaxHeight_WOD.text = WODwithDef
    
    rightMostPoint = sizes.padding_large + sizes.WODwidth
    lowestPoint = sizes.padding_large + makeTextWithMaxHeight_WOD.textPos[3]  
    centerH_WOD = makeTextWithMaxHeight_WOD.textPos[0] + ( makeTextWithMaxHeight_WOD.textPos[2] / 2 ) 
    
    # Toggle button - add WOD to priority word list
    toggle_addWOD = QCheckBox('', window)
    leftPoint = rightMostPoint + sizes.padding_large + (sizes.smallTextWidth/2) - (sizes.width_toggle/2)
    topPoint = sizes.padding_large + sizes.padding_medium
    textPos = (leftPoint,topPoint,sizes.width_toggle,sizes.width_toggle)
    toggle_addWOD.setGeometry(*(int(x) for x in textPos))
    toggle_addWOD.setStyleSheet(f"QCheckBox::indicator {{ width: {sizes.width_toggle}px; height: {sizes.width_toggle}px; }}")    
    if WODsPODstatus:
        toggle_addWOD.setChecked(True)
    else:
        toggle_addWOD.setChecked(False)
    toggle_addWOD.hide()
    wordPos = curWODandDef.positionOfWOD
    toggle_addWOD.clicked.connect(lambda: saveToggleChoice(toggle_addWOD,curFilePath,data,wordPos))
    centerH = textPos[0] + ( textPos[2] / 2 )    

    # Toggle button text - Add WOD
    text = 'Set word as priority word (show more often)'
    textAlignment = Qt.AlignCenter | Qt.AlignTop | Qt.TextWordWrap       
    topPoint = topPoint + sizes.width_toggle + sizes.padding_small
    textPos = (centerH, topPoint, sizes.smallTextWidth, 0)
    ST_addWODtext = StaticText(window,fonts.font_tiny,text,textPos,textAlignment)     
    ST_addWODtext.centerAlign_H()
    toggleText_addWOD = ST_addWODtext.makeTextObject()
    toggleText_addWOD.hide()    

    rightMostPoint = centerH + (sizes.smallTextWidth/2)
    lowestPoint = max(lowestPoint,topPoint+ST_addWODtext.positionAdjust[3])
    rightMostPoint_top = rightMostPoint

    # Print the priority word title
    text = 'Priority word of day'
    textAlignment = Qt.AlignCenter    
    topPoint = lowestPoint + (sizes.padding_large*2)
    textPos = (centerH_WOD, topPoint, sizes.PODwidth, 0)
    ST_PODtitle = StaticText(window,fonts.font_small_italic_bold,text,textPos,textAlignment)     
    ST_PODtitle.centerAlign_H()    

    lowestPoint = ST_PODtitle.positionAdjust[1] + ST_PODtitle.positionAdjust[3]
    topPoint_PODtitle = topPoint

    # Print the priority word
    textAlignment = Qt.AlignHCenter | Qt.AlignTop 
    text = PODwithDef
    makeTextWithMaxHeight_POD = MakeTextWithMaxHeight(window,text,centerH_WOD, \
                                                  lowestPoint + sizes.padding_small,sizes.PODwidth, \
                                                  sizes.maxPODheight,fonts.font_small_italic,\
                                                    textAlignment)     
    # Make the text initially blank, and then have this updated to the POD when the reveal button is pressed
    makeTextWithMaxHeight_POD.centerH()
    makeTextWithMaxHeight_POD.text = ""
    makeTextWithMaxHeight_POD.makeText()
    makeTextWithMaxHeight_POD.text = text

    lowestPoint = lowestPoint + makeTextWithMaxHeight_POD.textPos[3]    
    rightMostPoint_bottom = makeTextWithMaxHeight_POD.textPos[0] + makeTextWithMaxHeight_POD.textPos[2]

    # Make 'Reveal word definition' button and define its actions (clicked.connect)
    text = 'Reveal word definition'      
    position = (sizes.padding_large,lowestPoint+(sizes.padding_large*2),0,0)
    pushButton_reveal = PushButton(window,fonts.font_medium,text,position)     
    revealButton = pushButton_reveal.makeButton()
    if not curWODandDef.WODpresent:
        revealButton.setEnabled(False)
    # Actions for when the reveal button is pressed (more for other text/buttons/etc defined below)
    revealButton.clicked.connect(makeTextWithMaxHeight_WOD.editText) # reveal the WOD and its defintion
    revealButton.clicked.connect(lambda: toggle_addWOD.show()) # reveal toggle to add WOD to priority words    
    revealButton.clicked.connect(lambda: toggleText_addWOD.show()) # reeal text for the add WOD toggle
    revealButton.clicked.connect(ST_PODtitle.makeTextObject)    
    revealButton.clicked.connect(makeTextWithMaxHeight_POD.editText)      
   
    lowestPoint = lowestPoint + pushButton_reveal.positionAdjust[3] + (sizes.padding_large*2)
    
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
