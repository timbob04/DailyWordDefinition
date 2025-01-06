import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox
from PyQt5.QtCore import Qt
from commonClassesFunctions.functionsClasses_PyQt5 import Fonts, centerWindowOnScreen, StaticText, PushButton
from addEditWords.addEditWords_main import addEditWords
from StartStopProgram.startStopProgram_functionsClasses import EditText, getStartupFolder, Sizes_startProgram, EditStartupFolder, startupTogglePressed, startButtonPressed, CheckTimeEntered_start

def startProgram():

    # Make window
    app = QApplication(sys.argv)
    window = QMainWindow()    
    window.setWindowTitle('Program not currently running')

    # Goes true when the user has decided to start the program
    window.runProgram = False

    # Fonts
    fonts = Fonts()
    fonts.makeFonts()

    # Predefined sizes of things
    sizes = Sizes_startProgram()
    sizes.defineSizes()

    # Static text - choose time (top left)
    text = 'Choose time for daily word definition to appear (24 hour clock):'
    textAlignment = Qt.AlignRight | Qt.AlignVCenter | Qt.TextWordWrap    
    position = (sizes.padding_large, sizes.padding_large, sizes.width_ST_chooseTime, 0)
    ST_chooseTime = StaticText(window,fonts.font_medium,text,position,textAlignment)
    ST_chooseTime.makeTextObject()

    rightMostPoint = ST_chooseTime.positionAdjust[0] + ST_chooseTime.positionAdjust[2]
    centerV = ST_chooseTime.Vcenter

    # Object to check if HH and MM fields are entered correctly
    checkTimeEntered = CheckTimeEntered_start()

    # Edit text box - enter hours (top right)    
    position = (rightMostPoint+sizes.padding_large,centerV,sizes.width_button_change,0)
    editText_hours = EditText(window,fonts.font_medium,"HH",position)
    editText_hours.centerAlign_V()    
    editText_hours.forceWidth()
    ET_hours = editText_hours.makeEditTextBox()
    ET_hours.textChanged.connect(checkTimeEntered.checkTime_HH) # slot for checking if HH entered correct using class CheckTimeEntered

    rightMostPoint = rightMostPoint + sizes.padding_large + editText_hours.positionAdjust[2]

    # Static text - colon (top right)
    position = (rightMostPoint+sizes.padding_small, centerV, 0, 0)
    textAlignment = Qt.AlignCenter | Qt.AlignVCenter
    ST_colon = StaticText(window,fonts.font_medium,":",position,textAlignment)
    ST_colon.centerAlign_V()
    ST_colon.makeTextObject()

    rightMostPoint = rightMostPoint + sizes.padding_small + ST_colon.positionAdjust[2]
    centerH = ST_colon.positionAdjust[0] + ST_colon.positionAdjust[2]/2

    # Edit text box - enter minutes (top right)
    position = (rightMostPoint+sizes.padding_small,centerV,sizes.width_button_change,0)
    editText_mins = EditText(window,fonts.font_medium,"MM",position)
    editText_mins.centerAlign_V()    
    editText_mins.forceWidth()    
    ET_mins = editText_mins.makeEditTextBox()
    ET_mins.textChanged.connect(checkTimeEntered.checkTime_MM) # slot for checking if MM entered correct using class CheckTimeEntered

    rightMostPoint_topRow = position[0] + editText_mins.positionAdjust[2]
    bottomOfEditBox = editText_mins.positionAdjust[1] + editText_mins.positionAdjust[3]

    # Static text - time entered incorrectly
    position = (centerH,bottomOfEditBox+sizes.padding_small,110,0)
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
    toggle_startup.setGeometry(sizes.padding_large,sizes.startingY_checkBox,sizes.width_toggle,sizes.width_toggle)
    toggle_startup.setStyleSheet(f"QCheckBox::indicator {{ width: {sizes.width_toggle}px; height: {sizes.width_toggle}px; }}")
    toggle_startup.setChecked(False)
    toggle_startup.clicked.connect(lambda: startupTogglePressed(toggle_startup,button_change,editStartupFolder))

    rightMostPoint = sizes.padding_large + sizes.width_toggle
    centerV_toggleButton = sizes.startingY_checkBox + sizes.width_toggle/2

    # Static text - Add program to startup folder (bottom left)
    text = 'Add program to startup folder (needed to keep program running after computer reboot)'
    textAlignment = Qt.AlignLeft | Qt.AlignVCenter | Qt.TextWordWrap    
    position = (rightMostPoint+sizes.padding_medium, centerV_toggleButton, sizes.width_ST_startupToggle, 0)    
    ST_startup = StaticText(window,fonts.font_small,text,position,textAlignment)
    ST_startup.centerAlign_V()
    ST_startup.makeTextObject()
 
    lowestPoint = ST_startup.positionAdjust[1] + ST_startup.positionAdjust[3]

    # Get and show startup folder
    startupFolder = getStartupFolder()
    position = (sizes.padding_large,lowestPoint+sizes.padding_large,sizes.width_text_startupFolder,sizes.height_text_startupFolder)
    editStartupFolder = EditStartupFolder(position, window, startupFolder)
    
    centerV = position[1] + position[3]/2
    rightMostPoint = position[0] + position[2] 
    lowestPoint = editStartupFolder.positionOfText[1] + editStartupFolder.positionOfText[3]
    
    # Make 'change' startup folder button
    text = 'Change'      
    position = (rightMostPoint+sizes.padding_medium,centerV,0,0)
    PB_change = PushButton(window,fonts.font_medium,text,position)
    PB_change.centerAlign_V()
    button_change = PB_change.makeButton()
    button_change.hide() # hide button until toggle is pressed
    # Make slot for button for when it is pressed
    button_change.clicked.connect(editStartupFolder.updatePath)

    # Edit word list button
    text = 'Edit word list'
    top = lowestPoint + sizes.padding_large*2
    position = (sizes.padding_large, top, 0, 0)
    PB_editWordList = PushButton(window,fonts.font_medium,text,position)        
    button_editWordList = PB_editWordList.makeButton()
    button_editWordList.clicked.connect(addEditWords)

    lowestPoint = PB_editWordList.positionAdjust[1] + PB_editWordList.positionAdjust[3]

    # Start button
    text = 'Start'
    position = (rightMostPoint_topRow, lowestPoint, 0, 0)
    PB_start = PushButton(window,fonts.font_large_bold,text,position)
    PB_start.bottomAlign()
    PB_start.rightAlign()
    button_start = PB_start.makeButton()
    button_start.clicked.connect(lambda: startButtonPressed(window,checkTimeEntered,ET_hours.text(),ET_mins.text(),toggle_startup,editStartupFolder))

    rightMostPoint_botRow = PB_start.positionAdjust[0] + PB_start.positionAdjust[2]

    # Resize window
    rightMostPoint_final = max(rightMostPoint_botRow,rightMostPoint_topRow)
    window.resize(rightMostPoint_final+sizes.padding_large, lowestPoint+sizes.padding_large)

    # Center the window - put in the function (pass it 'window' and 'app')
    centerWindowOnScreen(window)

    # Show window
    window.show()

    # Run application's event loop
    app.exec_()

    return window.runProgram
    