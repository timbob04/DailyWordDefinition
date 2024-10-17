import sys, os
import json

from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QCheckBox, QScrollArea, QWidget, QFrame
from PyQt5.QtGui import QPainter, QPen, QFontMetrics

from commonClassesFunctions.functionsClasses import centerWindowOnScreen, getScreenWidthHeight, Fonts, StaticText, readJSONfile, PushButton

from .addEditWords_functionsClasses import Sizes_addEditWords, addNewWordTextBoxes

from PyQt5.QtCore import Qt

class makeWordList:    
    def __init__(self,dataIn,fonts,sizes,APIwidth,APIheight,startY,window):
        # Inputs
        self.dataIn = dataIn
        self.fonts = fonts
        self.sizes = sizes
        self.APIwidth = APIwidth
        self.APIheight = APIheight
        self.startY = startY
        self.window = window
        # Predefined sizes
        self.Vspacing_wordDefs = 50 # the vertical spacing between each word/def
        self.Hspacing = 15 # horizontal spacing for the word/def lines    
        self.textMaxWidth_PW = 30 # priority word title max with
        self.buttonPadding = 7
        self.VspaceAfterSmallTitles = 9
        # Predefined fonts
        self.font_priortyWordTitle = fonts.font_small
        self.font_deleteButton = fonts.font_medium  
        self.font_wordAndDef = fonts.font_medium   
        # Other        
        self.numWordDefs = len(dataIn)
        # Initialize dictionary for holding details for each row (word/def with buttons, etc)
        self.wordDefDetails = [{} for _ in range(self.numWordDefs)]
        # Run starter functions
        self.getHorizontalSpacing()
        self.putEachWordDefsInOneLine()
        self.getWordDefHeights()
        self.getTotalTextAreaHeight()
        self.makeTitles()
        self.getTopOfScrollArea()
        self.makeScrollableArea()
        self.getFirstRowCenter()        
        self.makeInitialWordList()            
        self.addScrollableContent()
    
    def getHorizontalSpacing(self):        
        # Priority word toggle title width, height and x position
        curText = "Priority word"
        fontMetrics = QFontMetrics(self.font_priortyWordTitle)
        bounding_rect = fontMetrics.boundingRect(0,0,int(self.textMaxWidth_PW),0, Qt.AlignCenter | Qt.TextWordWrap, curText)       
        self.width_priorityWord = bounding_rect.width()
        self.height_priorityWord = bounding_rect.height()
        # Get toggle x position
        self.toggleStartX = self.sizes.padding_large + (self.width_priorityWord/2) - (self.sizes.width_toggle/2) 
        # Delete button width
        curText = "Delete"
        fontMetrics = QFontMetrics(self.font_deleteButton)
        bounding_rect = fontMetrics.boundingRect(0,0,0,0, Qt.AlignCenter, curText)       
        self.width_deleteButton = bounding_rect.width()  
        height_deleteButton = bounding_rect.height()  
        self.height_wPad_delButton = height_deleteButton + (self.buttonPadding*2)
        width_wPad_delButton = self.width_deleteButton + (self.buttonPadding*2)
        self.startX_delButton = self.sizes.padding_large + self.width_priorityWord + self.Hspacing
        # Edit button width
        curText = "Edit"        
        bounding_rect = fontMetrics.boundingRect(0,0,0,0, Qt.AlignCenter, curText)       
        self.width_editButton = bounding_rect.width()   
        self.startX_editButton = self.startX_delButton + width_wPad_delButton + self.Hspacing
        # Width of everything apart from word/def box, from left to right
        width_excludeWordDef = self.sizes.padding_large + self.width_priorityWord + \
            self.Hspacing + self.width_deleteButton + self.Hspacing + self.width_editButton + \
            self.Hspacing + (self.sizes.padding_large*2) + \
            (self.buttonPadding*4) # 2 buttons, so 4 paddings                                   
        # Width of word and definition area
        self.width_wordDef = self.APIwidth - width_excludeWordDef
        # Starting position of word and definition area
        self.startX_wordAndDef = width_excludeWordDef - (self.sizes.padding_large*2)
        # Height of a sigle line piece of text                
        fontMetrics = QFontMetrics(self.font_wordAndDef)       
        bounding_rect = fontMetrics.boundingRect(0,0,int(self.width_wordDef),0, Qt.AlignCenter, "A")       
        self.singleLineTextHeight = bounding_rect.height()    

    def putEachWordDefsInOneLine(self):        
        for i in range(self.numWordDefs):
            self.wordDefDetails[i]['wordAndDef'] = self.dataIn[i]["word"] + ": " + self.dataIn[i]["definition"]

    def wordDefHeight(self,text):
        fontMetrics = QFontMetrics(self.font_wordAndDef)                
        bounding_rect = fontMetrics.boundingRect(0,0,int(self.width_wordDef),0, Qt.AlignCenter | Qt.TextWordWrap, text)       
        return bounding_rect.height()
        
    def getWordDefHeights(self):
        for i in range(self.numWordDefs):
            curText = self.wordDefDetails[i]['wordAndDef']
            self.wordDefDetails[i]['textHeight'] = self.wordDefHeight(curText)

    def getTotalTextAreaHeight(self):
        self.totalTextheight = 0
        for i in range(self.numWordDefs - 1, -1, -1): # reverse order because more recent word is at the top (in the API)
            curRowHeight = max(self.wordDefDetails[i]['textHeight'],self.height_wPad_delButton)
            if i < self.numWordDefs - 1:
                self.totalTextheight += (curRowHeight + self.Vspacing_wordDefs)
            else:
                self.totalTextheight += curRowHeight

    def makeTitles(self):
        # 'Priority words' title
        text = 'Priority words'
        textAlignment = Qt.AlignCenter
        centerH = self.sizes.padding_large + (self.width_priorityWord/2)
        textPos = (centerH, self.startY, self.width_priorityWord, 0)
        self.ST_priorityWordTitle = StaticText(self.window,self.font_priortyWordTitle,text,textPos,textAlignment)         
        self.ST_priorityWordTitle.centerAlign_H()
        self.ST_priorityWordTitle.makeTextObject()
        # 'Word: definition
        text = 'Word: definition'
        textAlignment = Qt.AlignVCenter | Qt.AlignLeft
        bottomOfPWtitle = self.ST_priorityWordTitle.positionAdjust[1] + self.ST_priorityWordTitle.positionAdjust[3]        
        textPos = (self.startX_wordAndDef+4, bottomOfPWtitle, self.width_wordDef, 0)
        self.ST_wordDefTitle = StaticText(self.window,self.font_priortyWordTitle,text,textPos,textAlignment)         
        self.ST_wordDefTitle.alignBottom()
        self.ST_wordDefTitle.makeTextObject()
        
    def getTopOfScrollArea(self):
        self.topOfScrollArea = self.ST_priorityWordTitle.positionAdjust[1] + self.ST_priorityWordTitle.positionAdjust[3]

    def makeScrollableArea(self):
        # Create scrollable area for the current words/defs
        self.scroll_area = QScrollArea(self.window)
        self.scroll_area.setGeometry(0, self.topOfScrollArea, self.APIwidth, self.APIheight-self.topOfScrollArea)  # Set the size of the API area which can be scrolled
        self.scroll_area.setFrameShape(QFrame.NoFrame) # Remove borderaround from the scroll area
        # Create a widget to contain the scrollable area's contents        
        self.scrollable_content = QWidget()
        self.scrollable_content.setFixedSize(self.APIwidth, self.totalTextheight+self.sizes.padding_large)  # Set size of the scrollable content

    def updateScrollAreaHeight(self):
        self.scrollable_content.setFixedSize(self.APIwidth, self.totalTextheight+self.sizes.padding_large) 

    def getFirstRowCenter(self):
        self.startY = self.topOfScrollArea + self.VspaceAfterSmallTitles

    def makeToggle(self,curRowTop,ind):
        # Positioning
        curRowCenter = curRowTop + (self.height_wPad_delButton/2)
        togglePos = (self.toggleStartX,curRowCenter-(self.sizes.width_toggle/2), \
                        self.sizes.width_toggle,self.sizes.width_toggle)
        # Make toggle
        curToggleHandle = QCheckBox('', self.scrollable_content)                    
        curToggleHandle.setGeometry(*(int(x) for x in togglePos))
        curToggleHandle.setStyleSheet(f"QCheckBox::indicator {{ width: {self.sizes.width_toggle}px; height: {self.sizes.width_toggle}px; }}")            
        # Set toggle to checked (is_pod == true) or unchecked
        if self.dataIn[ind]['is_POD']:
            curToggleHandle.setChecked(True)
        else:
            curToggleHandle.setChecked(False)
        # Store toggle handle
        self.wordDefDetails[ind]['priorityWordTogggles'] = curToggleHandle 

    def makeDeleteButton(self,curRowTop,ind):              
        text = 'Delete'        
        position = (self.startX_delButton,curRowTop,0,0)
        pushButton_del = PushButton(self.scrollable_content,self.font_deleteButton,text,position) 
        pushButton_del.setButtonPadding(self.buttonPadding,self.buttonPadding)
        DelButton = pushButton_del.makeButton()             
        #DelButton.clicked.connect(lambda: addWordToJSONfile(curFilePath,data,addWordInput,addDefInput))
        self.wordDefDetails[ind]['DeleteButtons'] = DelButton             
        
    def makeEditButton(self,curRowTop,ind):              
        text = 'Edit'        
        position = (self.startX_editButton,curRowTop,0,0)
        pushButton_edit = PushButton(self.scrollable_content,self.font_deleteButton,text,position) 
        pushButton_edit.setButtonPadding(self.buttonPadding,self.buttonPadding)
        EditButton = pushButton_edit.makeButton()           
        #EditButton.clicked.connect(lambda: addWordToJSONfile(curFilePath,data,addWordInput,addDefInput))    
        self.wordDefDetails[ind]['EditButtons'] = EditButton                   
      
    def makeWordDef(self,curRowTop,ind):  
        curRowTop += (self.height_wPad_delButton/2) - (self.singleLineTextHeight/2)
        textAlignment = Qt.AlignVCenter | Qt.AlignLeft        
        text = self.wordDefDetails[ind]['wordAndDef']            
        textPos = (self.startX_wordAndDef, curRowTop, self.width_wordDef, 0)
        curSTob = StaticText(self.scrollable_content,self.font_wordAndDef,text,textPos,textAlignment)
        wordAndDefTextOb = curSTob.makeTextObject()     
        self.wordDefDetails[ind]['wordAndDefTextOb'] = wordAndDefTextOb  

    def makeInitialWordList(self):
        curRowTop = self.VspaceAfterSmallTitles # Starting row top position        
        for i in range(self.numWordDefs - 1, -1, -1):
            # Make API things
            self.makeToggle(curRowTop,i)
            self.makeDeleteButton(curRowTop,i)
            self.makeEditButton(curRowTop,i)
            self.makeWordDef(curRowTop,i)
            # Set new row top position
            rowHeight = max(self.wordDefDetails[i]['textHeight'],self.height_wPad_delButton)
            curRowTop = curRowTop + rowHeight + self.Vspacing_wordDefs              

    def addScrollableContent(self):
        # Set scroll area properties (should be set after the scrollable content is populated)
        self.scroll_area.setWidget(self.scrollable_content)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Disable horizontal scrolling
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded) 

    def updateListWithNewWord(self,newWord,newDef): # list in this class
        textOnOneLine = newWord + ": " + newDef        
        wordDefHeight = self.wordDefHeight(textOnOneLine)
        new_entry = { 'wordAndDef': textOnOneLine,
                     'textHeight': wordDefHeight,                     
                     'priorityWordTogggles': None,
                     'DeleteButtons': None,
                     'EditButtons': None,
                     'wordAndDefTextOb': None
                     }
        self.wordDefDetails.append(new_entry)
        self.numWordDefs += 1   
    
    def pushEverythingDown(self,newWordHeight):
        nudge = newWordHeight + self.Vspacing_wordDefs
        for i in range(self.numWordDefs-1):
            self.adjustGeoWithNewHeight(self.wordDefDetails[i]['priorityWordTogggles'],nudge)
            self.adjustGeoWithNewHeight(self.wordDefDetails[i]['DeleteButtons'],nudge)
            self.adjustGeoWithNewHeight(self.wordDefDetails[i]['EditButtons'],nudge)
            self.adjustGeoWithNewHeight(self.wordDefDetails[i]['wordAndDefTextOb'],nudge)
            
    def adjustGeoWithNewHeight(self,handle,nudge):
        curGeometry = handle.geometry()            
        handle.setGeometry(curGeometry.x(),curGeometry.y()+nudge,curGeometry.width(),curGeometry.height())        

    def updateAPIwithNewEntry(self,newWord,newDef):
        self.updateListWithNewWord(newWord,newDef) # add new word to list and get its details, including height
        self.getTotalTextAreaHeight()
        self.updateScrollAreaHeight()   
        # Push all other words down
        newWordHeight = self.wordDefDetails[-1]['textHeight']
        self.pushEverythingDown(newWordHeight)             
        # Add new word row to top
        self.makeToggle(self.VspaceAfterSmallTitles,-1)
        self.makeDeleteButton(self.VspaceAfterSmallTitles,-1)
        self.makeEditButton(self.VspaceAfterSmallTitles,-1)
        self.makeWordDef(self.VspaceAfterSmallTitles,-1)




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
