import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox
from PyQt5.QtCore import Qt
from StartStopProgram.utils import EditText, Sizes_stopProgram, OkButtonPressed, CheckTimeEntered_stop
from commonClassesFunctions.PyQt5_functions import Fonts, centerWindowOnScreen, StaticText, PushButton
from addEditWords.main import addEditWords

def stopProgram():

    # Make window
    app = QApplication(sys.argv)
    window = QMainWindow()    
    window.setWindowTitle('Program currently running')

    # Goes true when the user has decided to stop the program
    window.stopProgram = False

    # Fonts
    fonts = Fonts()
    fonts.makeFonts()

    # Predefined sizes of things
    sizes = Sizes_stopProgram()
    sizes.defineSizes()

    # Static text - edit time (top left)
    text = 'Change time that daily word definition appears (24 hour clock):'
    textAlignment = Qt.AlignRight | Qt.AlignVCenter | Qt.TextWordWrap    
    position = (sizes.padding_large, sizes.padding_large, sizes.width_ST_editTime, 0)
    ST_editTime = StaticText(window,fonts.font_medium,text,position,textAlignment)
    ST_editTime.makeTextObject()

    rightMostPoint = ST_editTime.positionAdjust[0] + ST_editTime.positionAdjust[2]
    centerV = ST_editTime.Vcenter
    bottomOfST = ST_editTime.positionAdjust[1] + ST_editTime.positionAdjust[3]

    # Object to check if HH and MM is entered correctly
    checkTimeEntered = CheckTimeEntered_stop()

    # Edit text box - enter hours (top right)    
    position = (rightMostPoint+sizes.padding_large,centerV,sizes.width_ET_hourMin,0)
    editText_hours = EditText(window,fonts.font_medium,"HH",position)
    editText_hours.centerAlign_V()    
    editText_hours.forceWidth()
    ET_hours = editText_hours.makeEditTextBox()
    ET_hours.textChanged.connect(checkTimeEntered.checkTime_HH) # slot for checking if HH entered correct using class CheckTimeEntered
    checkTimeEntered.ET_HH = ET_hours

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
    position = (rightMostPoint+sizes.padding_small,centerV,sizes.width_ET_hourMin,0)
    editText_mins = EditText(window,fonts.font_medium,"MM",position)
    editText_mins.centerAlign_V()    
    editText_mins.forceWidth()    
    ET_mins = editText_mins.makeEditTextBox()
    ET_mins.textChanged.connect(checkTimeEntered.checkTime_MM) # slot for checking if MM entered correct using class CheckTimeEntered
    checkTimeEntered.ET_MM = ET_mins

    rightMostPoint_topRow = position[0] + editText_mins.positionAdjust[2]
    bottomOfEditBox = editText_mins.positionAdjust[1] + editText_mins.positionAdjust[3]
    centerTopRow = (rightMostPoint_topRow + sizes.padding_large) / 2

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

    # Static text - --- Or ---
    text = '--- Or ---'        
    position = (centerTopRow, bottomOfST+sizes.padding_large, 0, 0)
    textAlignment = Qt.AlignCenter | Qt.AlignVCenter
    ST_Or = StaticText(window,fonts.font_medium,text,position,textAlignment)
    ST_Or.centerAlign_H()
    ST_Or.makeTextObject()

    lowestPoint = ST_Or.positionAdjust[1] + ST_Or.positionAdjust[3]

    # Toggle button - stop program (bottom left)
    toggle_stopProgram = QCheckBox('', window)
    toggle_stopProgram.setGeometry(sizes.padding_large,lowestPoint+sizes.padding_large,sizes.width_toggle,sizes.width_toggle)
    toggle_stopProgram.setStyleSheet(f"QCheckBox::indicator {{ width: {sizes.width_toggle}px; height: {sizes.width_toggle}px; }}")
    toggle_stopProgram.setChecked(False)
    toggle_stopProgram.clicked.connect(checkTimeEntered.checkStopToggle)

    rightMostPoint = sizes.padding_large + sizes.width_toggle
    lowestPoint = lowestPoint + sizes.padding_large + sizes.width_toggle

    # Static text - Stop program
    text = 'Stop program'        
    position = (rightMostPoint+sizes.padding_medium, lowestPoint-sizes.width_toggle/2, 0, 0)
    textAlignment = Qt.AlignLeft | Qt.AlignVCenter 
    ST_Or = StaticText(window,fonts.font_medium,text,position,textAlignment)
    ST_Or.centerAlign_V()
    ST_Or.makeTextObject()

    rightMostPoint = ST_Or.positionAdjust[0] + ST_Or.positionAdjust[2]
    lowestPoint = ST_Or.positionAdjust[1] + ST_Or.positionAdjust[3]

    # Edit word list button
    text = 'Edit word list'
    top = lowestPoint + sizes.padding_large*5
    position = (sizes.padding_large, top, 0, 0)
    PB_editWordList = PushButton(window,fonts.font_medium,text,position)        
    button_editWordList = PB_editWordList.makeButton()
    button_editWordList.clicked.connect(addEditWords)

    lowestPoint = PB_editWordList.positionAdjust[1] + PB_editWordList.positionAdjust[3]

    # Ok button
    text = 'Ok'
    position = (rightMostPoint_topRow, lowestPoint, 0, 0)
    PB_Ok = PushButton(window,fonts.font_large,text,position)
    PB_Ok.rightAlign()
    PB_Ok.bottomAlign()
    button_Ok = PB_Ok.makeButton()
    button_Ok.clicked.connect(lambda: OkButtonPressed(window,checkTimeEntered,toggle_stopProgram,ET_hours.text(),ET_mins.text()))    

    # Resize window
    window.resize(rightMostPoint_topRow+sizes.padding_large, lowestPoint+sizes.padding_large)

    # Center the window - put in the function (pass it 'window' and 'app')
    centerWindowOnScreen(window)

    # Show window
    window.show()

    # Run application's event loop
    app.exec_()

    return window.stopProgram