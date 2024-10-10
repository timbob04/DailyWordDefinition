import sys, os

from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QCheckBox, QScrollArea, QWidget
from PyQt5.QtGui import QPainter, QPen, QFontMetrics

from commonClassesFunctions.functionsClasses import centerWindowOnScreen, getScreenWidthHeight, Fonts, StaticText, readJSONfile, PushButton

from .addEditWords_functionsClasses import Sizes_addEditWords, addWordToJSONfile

from PyQt5.QtCore import Qt

class makeWordList:
    ###### Temp notes
    # The list will be in reverse order (newest words at top)
    # Once I get the total height of all words/defs, either use a vertical scale bar, or not
    # For this above, make sure to save some space on the right for this appear
    # Also, I want to do this for the edit words section only, without including the 'Edit words' title, or the small 'Priority words' and 'Word: definition' titles
    # For this, I will use QScrollArea for this bottom section if the contents are too tall, or just regular coding (not QScrollArea) if not
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
        self.Hspacing = 10 # horizontal spacing for the word/def lines    
        self.textMaxWidth_PW = 30 # priority word title max with
        self.buttonPadding = 7
        self.VspaceAfterSmallTitles = 22
        # Predefined fonts
        self.font_priortyWordTitle = fonts.font_small
        self.font_deleteButton = fonts.font_mediumLarge   
        self.font_wordAndDef = fonts.font_medium   
        # Other
        self.wordDefDetails = []  
        self.numWordDefs = len(dataIn)
        # Initialize dictionary for holding details for each row (word/def with buttons, etc)
        self.wordDefDetails = [{} for _ in range(self.numWordDefs)]
        # Run starter functions
        self.getHorizontalSpacing()
        self.putEachWordDefsInOneLine()
        self.wordDefHeights()
        self.getTotalTextAreaHeight()
        self.makeTitles()
        self.getTopOfScrollArea()
        self.makeScrollableArea()
        self.getFirstRowCenter()
        self.makePriorityWordToggles()

    def getHorizontalSpacing(self):        
        # Priority word toggle title width and height
        curText = "Priority word"
        fontMetrics = QFontMetrics(self.font_priortyWordTitle)
        bounding_rect = fontMetrics.boundingRect(0,0,int(self.textMaxWidth_PW),0, Qt.AlignCenter | Qt.TextWordWrap, curText)       
        self.width_priorityWord = bounding_rect.width()
        self.height_priorityWord = bounding_rect.height()
        # Delete button width
        curText = "Delete"
        fontMetrics = QFontMetrics(self.font_deleteButton)
        bounding_rect = fontMetrics.boundingRect(0,0,0,0, Qt.AlignCenter, curText)       
        self.width_deleteButton = bounding_rect.width()        
        # Edit button width
        curText = "Edit"        
        bounding_rect = fontMetrics.boundingRect(0,0,0,0, Qt.AlignCenter, curText)       
        self.width_editButton = bounding_rect.width()   
        # Width of everything apart from word/def box, from left to right
        width_excludeWordDef = self.sizes.padding_large + self.width_priorityWord + \
            self.Hspacing + self.width_deleteButton + self.Hspacing + self.width_editButton + \
            self.Hspacing + self.sizes.padding_large
        # Width of word and definition area
        self.width_wordDef = self.APIwidth - width_excludeWordDef
        # Starting position of word and definition area
        self.startX_wordAndDef = width_excludeWordDef - self.sizes.padding_large

    def putEachWordDefsInOneLine(self):        
        for i in range(self.numWordDefs):
            self.wordDefDetails[i]['wordAndDef'] = self.dataIn[i]["word"] + ": " + self.dataIn[i]["definition"]

    def wordDefHeights(self):
        fontMetrics = QFontMetrics(self.font_wordAndDef)
        for i in range(self.numWordDefs):
            curText = self.wordDefDetails[i]['wordAndDef']
            bounding_rect = fontMetrics.boundingRect(0,0,int(self.width_wordDef),0, Qt.AlignCenter, curText)       
            self.wordDefDetails[i]['textHeight'] = bounding_rect.height()

    def getTotalTextAreaHeight(self):
        self.totalTextheight = 0
        for i in range(self.numWordDefs):
            self.totalTextheight += self.wordDefDetails[i]['textHeight']

    def makeTitles(self):
        # 'Priority words' title
        text = 'Priority words'
        textAlignment = Qt.AlignCenter
        self.PW_H = self.sizes.padding_large + (self.width_priorityWord/2)
        textPos = (self.PW_H, self.startY, self.width_priorityWord, 0)
        self.ST_priorityWordTitle = StaticText(self.window,self.font_priortyWordTitle,text,textPos,textAlignment)         
        self.ST_priorityWordTitle.centerAlign_H()
        self.ST_priorityWordTitle.makeTextObject()
        # 'Word: definition
        text = 'Word: definition'
        textAlignment = Qt.AlignLeft
        bottomOfPWtitle = self.ST_priorityWordTitle.positionAdjust[1] + self.ST_priorityWordTitle.positionAdjust[3]        
        textPos = (self.startX_wordAndDef+4, bottomOfPWtitle, self.width_wordDef, 0)
        self.ST_wordDefTitle = StaticText(self.window,self.font_priortyWordTitle,text,textPos,textAlignment)         
        self.ST_wordDefTitle.alignBottom()
        self.ST_wordDefTitle.makeTextObject()
        
    def getTopOfScrollArea(self):
        self.topOfScrollArea = self.ST_priorityWordTitle.positionAdjust[1] + self.ST_priorityWordTitle.positionAdjust[3]

    def makeScrollableArea(self):
        # Create scrollable area for the current words/defs
        scroll_area = QScrollArea(self.window)
        scroll_area.setGeometry(0, self.topOfScrollArea, self.APIwidth, self.APIheight-self.topOfScrollArea)  # Set the size of the API area which can be scrolled
        # Create a widget to contain the scrollable area's contents
        currentTextHeight = self.totalTextheight
        scrollable_content = QWidget()
        scrollable_content.setFixedSize(self.APIwidth, self.totalTextheight+self.sizes.padding_large)  # Set size of the scrollable content

    def getFirstRowCenter(self):
        self.startY = self.topOfScrollArea + self.VspaceAfterSmallTitles

    def makePriorityWordToggles(self):
        toggleStartX = self.PW_H - self.sizes.width_toggle/2
        curRowCenter = self.startY
        for i in range(self.numWordDefs):
            curToggleHandle = QCheckBox('', self.window)            
            togglePos = (toggleStartX,curRowCenter-(self.sizes.width_toggle/2), \
                         self.sizes.width_toggle,self.sizes.width_toggle)
            curToggleHandle.setGeometry(*(int(x) for x in togglePos))
            curToggleHandle.setStyleSheet(f"QCheckBox::indicator {{ width: {self.sizes.width_toggle}px; height: {self.sizes.width_toggle}px; }}")            
            curRowCenter = curRowCenter + self.wordDefDetails[i]['textHeight'] + self.Vspacing_wordDefs
            if self.dataIn[i]['is_POD']:
                curToggleHandle.setChecked(True)
            else:
                curToggleHandle.setChecked(False)
            self.wordDefDetails[i]['priorityWordTogggles'] = curToggleHandle    
            
            # Add part about making the toggle checked or not checked based on the json file

        print("Here I will make the word and def list with all the extras - delete buttons, etc")
        # For each thing (e.g., toggle button), I will need to collect its handle, and also its position.
        # Store these things in self.wordDefDetails
        # The position will be needed for later, when I have to move everything down after I add a new word/def (top part of API)
        # The things I need to make for each row, and save a handle and positio for, are:
        # the 1) priority toggle button, delete button, edit button, word and def text.
        # One more thing... for the lowest point of each row, use either the edit (or delete) button bottom, or the text (whichever is lowest) 
        # Start the next row using this value

    def updateListWithNewEntry(newWord,newDef):
        print("Here update the list, putting the new word/def at the top")

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
    addWordsTitle = ST_addWordsTitle.makeTextObject()

    lowestPoint = ST_addWordsTitle.positionAdjust[1] + ST_addWordsTitle.positionAdjust[3]

    # Small label for 'Add word' edit text box
    text = 'Add word'
    textAlignment = Qt.AlignCenter
    textPos = (sizes.padding_large, lowestPoint+sizes.padding_large, 0, 0)
    ST_addWordLabel = StaticText(window,fonts.font_medium,text,textPos,textAlignment)         
    addWordLabel = ST_addWordLabel.makeTextObject()

    # Small label for 'Add definition' edit text box
    text = 'Add definition'
    textAlignment = Qt.AlignCenter
    leftPos = sizes.padding_large + width_addWord + sizes.padding_large
    textPos = (leftPos, lowestPoint+sizes.padding_large, 0, 0)
    ST_addDefLabel = StaticText(window,fonts.font_medium,text,textPos,textAlignment)         
    addDefLabel = ST_addDefLabel.makeTextObject()

    lowestPoint = ST_addDefLabel.positionAdjust[1] + ST_addDefLabel.positionAdjust[3]

    # Edit text box to add word
    addWordInput = QLineEdit(window)    
    addWordInput.setGeometry(sizes.padding_large, lowestPoint+sizes.padding_small, int(width_addWord), 40 )
    addWordInput.setFont(fonts.font_mediumLarge)
    addWordInput.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    addWordInput.setStyleSheet("QLineEdit { border: 1px solid black; }")

    # Edit text box to add definition
    addDefInput = QLineEdit(window)    
    addDefInput.setGeometry(int(leftPos), lowestPoint+sizes.padding_small, int(width_addDefinition), 40 )
    addDefInput.setFont(fonts.font_mediumLarge)
    addDefInput.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    addDefInput.setStyleSheet("QLineEdit { border: 1px solid black; }")

    lowestPoint = addDefInput.y() + addDefInput.height()

    # 'Add' button
    text = 'Add'      
    position = (sizes.padding_large,lowestPoint+sizes.padding_large,0,0)
    pushButton_Add = PushButton(window,fonts.font_mediumLarge,text,position) 
    pushButton_Add.setButtonPadding(14,7)
    AddButton = pushButton_Add.makeButton()          
    AddButton.clicked.connect(lambda: addWordToJSONfile(curFilePath,data,addWordInput,addDefInput))
    AddButton.clicked.connect(addWordInput.clear)
    AddButton.clicked.connect(addDefInput.clear)

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
    editWordsTitle = ST_editWordsTitle.makeTextObject()

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
