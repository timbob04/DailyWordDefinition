import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from RunProgram.utils import WODandDef, PODandDef, Sizes_presentWODAPI, saveToggleChoice, getDateForTitle
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox
from commonClassesFunctions.utils import readJSONfile, getBaseDir, PID
from commonClassesFunctions.PyQt5_functions import Fonts, MakeTextWithMaxHeight, StaticText, PushButton, centerWindowOnScreen, setPyQt5path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "_internal"))

def getAndMakeAPIcontent():    

    print('\nWordDefAPI.exe running')

    # Start an application
    app = QApplication(sys.argv)

    # Create PID for current QApplication
    pid = PID("WordDefAPI")
    pid.createPID()
    print("\nCreating PID for WordDefAPI (this exe).")

    # Make a current window
    window = QMainWindow()
    dateForTitle = getDateForTitle()
    window.setWindowTitle("Word of the day.  " + dateForTitle) 

    # Predefined sizes of things
    sizes = Sizes_presentWODAPI()
    sizes.defineSizes()    
    
    # Get path of accessory files
    base_dir = getBaseDir()
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

    # Fonts
    fonts = Fonts()
    fonts.makeFonts()

    # Word title (small)
    # Toggle button text - Add WOD
    text = 'Word:'
    textAlignment = Qt.AlignLeft | Qt.AlignTop    
    textPos = (sizes.padding_large, sizes.padding_large, 0, 0)
    ST_wordTitleText = StaticText(window,fonts.font_small,text,textPos,textAlignment)     
    ST_wordTitleText.makeTextObject()
    
    lowestPoint = ST_wordTitleText.positionAdjust[1] + ST_wordTitleText.positionAdjust[3]
    bottomWordTitle = lowestPoint

    # Make WOD text
    textAlignment = Qt.AlignLeft | Qt.AlignTop 
    topPoint = lowestPoint + sizes.padding_small
    window.makeTextWithMaxHeight_WOD = MakeTextWithMaxHeight(window,WOD,sizes.padding_large, \
                                                  topPoint,sizes.WODwidth, \
                                                  sizes.maxWODheight,fonts.font_mediumLargeBold,\
                                                    textAlignment) # make part of 'window', but this will need to be used after this function is run, and everything apart from window is destroyed              
    window.makeTextWithMaxHeight_WOD.showText()
    
    lowestPoint = window.makeTextWithMaxHeight_WOD.textPos[1] + window.makeTextWithMaxHeight_WOD.textPos[3]
    rightMostPoint = sizes.padding_large + sizes.WODwidth    
    centerH_WOD = window.makeTextWithMaxHeight_WOD.textPos[0] + ( window.makeTextWithMaxHeight_WOD.textPos[2] / 2 ) 

    # Toggle button - add WOD to priority word list
    toggle_addWOD = QCheckBox('', window)
    leftPoint = rightMostPoint + sizes.padding_large + (sizes.smallTextWidth/2) - (sizes.width_toggle/2)
    topPoint = bottomWordTitle + sizes.padding_medium
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

    toggleTextBottom = topPoint + ST_addWODtext.positionAdjust[3]
    rightMostPoint_top = ST_addWODtext.positionAdjust[0] + ST_addWODtext.positionAdjust[2]

    # Definition title (small)
    text = 'Definition:'
    textAlignment = Qt.AlignLeft | Qt.AlignTop    
    topPoint = lowestPoint + sizes.padding_medium
    textPos = (sizes.padding_large, topPoint, 0, 0)
    ST_definitionTitleText = StaticText(window,fonts.font_small,text,textPos,textAlignment)     
    ST_definitionTitleText.makeTextObject()

    lowestPoint = ST_definitionTitleText.positionAdjust[1] + ST_definitionTitleText.positionAdjust[3]

    # Make WOD definition - only reveal on button press
    textAlignment = Qt.AlignLeft | Qt.AlignTop 
    topPoint = lowestPoint + sizes.padding_small
    window.makeTextWithMaxHeight_WODdef = MakeTextWithMaxHeight(window,WOD_definition,sizes.padding_large, \
                                                  topPoint,sizes.WODwidth, \
                                                  sizes.maxDefheight,fonts.font_mediumLarge,\
                                                    textAlignment) # make part of 'window', but this will need to be used after this function is run, and everything apart from window is destroyed              
    
    lowestPoint_wordDef = window.makeTextWithMaxHeight_WODdef.textPos[1] + window.makeTextWithMaxHeight_WODdef.textPos[3]
    lowestPoint = max(toggleTextBottom,lowestPoint_wordDef)

    # Print the priority word title
    text = 'Priority word of day'
    textAlignment = Qt.AlignCenter    
    topPoint = lowestPoint + (sizes.padding_large*2)
    textPos = (centerH_WOD, topPoint, sizes.PODwidth, 0)
    ST_PODtitle = StaticText(window,fonts.font_small_italic_bold,text,textPos,textAlignment)     
    ST_PODtitle.centerAlign_H()  
    PODtitle = ST_PODtitle.makeTextObject()  
    PODtitle.hide()

    lowestPoint = ST_PODtitle.positionAdjust[1] + ST_PODtitle.positionAdjust[3]

    # Print the priority word
    textAlignment = Qt.AlignHCenter | Qt.AlignTop     
    window.makeTextWithMaxHeight_POD = MakeTextWithMaxHeight(window,PODwithDef,centerH_WOD, \
                                                  lowestPoint + sizes.padding_small,sizes.PODwidth, \
                                                  sizes.maxPODheight,fonts.font_small_italic,\
                                                    textAlignment) # make part of 'window', but this will need to be used after this function is run, and everything apart from window is destroyed
    window.makeTextWithMaxHeight_POD.centerH()
    
    lowestPoint = window.makeTextWithMaxHeight_POD.textPos[1] + window.makeTextWithMaxHeight_POD.textPos[3]
    rightMostPoint_bottom = window.makeTextWithMaxHeight_POD.textPos[0] + window.makeTextWithMaxHeight_POD.textPos[2]

    # Make 'Reveal word definition' button and define its actions (clicked.connect)
    text = 'Reveal word definition'      
    position = (sizes.padding_large,lowestPoint+(sizes.padding_large*2),0,0)
    pushButton_reveal = PushButton(window,fonts.font_medium,text,position)     
    revealButton = pushButton_reveal.makeButton()
    if not curWODandDef.WODpresent:
        revealButton.setEnabled(False)
    # Actions for when the reveal button is pressed
    revealButton.clicked.connect(lambda: window.makeTextWithMaxHeight_WODdef.showText()) # reveal the WOD and its defintion
    revealButton.clicked.connect(lambda: toggle_addWOD.show()) # reveal toggle to add WOD to priority words    
    revealButton.clicked.connect(lambda: toggleText_addWOD.show()) # reveal text for the add WOD toggle
    revealButton.clicked.connect(lambda: PODtitle.show()) 
    revealButton.clicked.connect(lambda: window.makeTextWithMaxHeight_POD.showText()) # Priority word
    
    lowestPoint = lowestPoint + pushButton_reveal.positionAdjust[3] + (sizes.padding_large*2)
    
    rightMostPoint_all = max(rightMostPoint_top,rightMostPoint_bottom) 

    # Resize window
    window.resize(int(rightMostPoint_all+sizes.padding_large), int(lowestPoint+sizes.padding_large))

    # Show window
    window.show()

    # Center the window - put in the function (pass it 'window' and 'app')
    centerWindowOnScreen(window)

    # Run application's event loop
    exit_code = app.exec_()

    # Delete programs PID on program exit
    pid.cleanUpPID()

    # Exit application
    sys.exit(exit_code)

if __name__ == "__main__":
    setPyQt5path()
    getAndMakeAPIcontent()    