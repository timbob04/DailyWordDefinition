import json
from PyQt5.QtWidgets import QLineEdit, QCheckBox, QScrollArea, QWidget, QFrame, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics
from commonClassesFunctions.utils import readJSONfile
from commonClassesFunctions.PyQt5_functions import StaticText, PushButton, centerWindowOnScreen
from addEditWords.utils import getWordListPath

class MakeWordList:    
    def __init__(self,fonts,sizes,APIwidth,APIheight,startY,window):
        # Inputs        
        self.fonts = fonts
        self.sizes = sizes
        self.APIwidth = APIwidth
        self.APIheight = APIheight
        self.startY = startY
        self.window = window
        self.jsonFileName = getWordListPath()                
        # API spacing/sizes to use
        self.Vspacing_wordDefs = 50 # the vertical spacing between each word/def
        self.Hspacing = 15 # horizontal spacing for the word/def lines    
        self.textMaxWidth_PW = 30 # priority word title max with
        self.buttonPadding = 7
        self.VspaceAfterSmallTitles = 9
        # Fonts to use
        self.font_priortyWordTitle = fonts.font_small
        self.font_deleteButton = fonts.font_medium  
        self.font_wordAndDef = fonts.font_medium                
        # Run methods to make API
        self.getDataIn()
        self.getNumberOfWordsInList()
        self.getHorizontalSpacing() # For the main word list, figure out how wide things are and where they will start (left to right)
        self.getSingleLineTextHeight() # Get the height of a single line of text - for vertical spacing later
        self.makeDict() # Initialize dictionary to hold all the handles/details for the current words/defs list
        self.putEachWordAndDefInOneLine()
        self.getAllWordDefHeights() # get vertical heights for each word/def
        self.getTotalTextAreaHeight()
        self.makeTitles()
        self.getWordListYStart() # top starting position for word list
        self.makeScrollableArea()            
        self.makeInitialWordList()            
        self.addScrollableContent()
        # Anything after this is done when the user does something (clicks a button, etc)

    def getDataIn(self):
        self.dataIn = readJSONfile(self.jsonFileName)

    def getNumberOfWordsInList(self):
        if self.dataIn is not None:
            self.numWordDefs = len(self.dataIn)
        else:
            self.numWordDefs = 0

    # For the main word list, figure out how wide each made part is for toggles/buttons/text/etc
    def getHorizontalSpacing(self):        
        # Priority word toggle title width, height and starting x position
        curText = "Priority word"
        fontMetrics = QFontMetrics(self.font_priortyWordTitle)
        bounding_rect = fontMetrics.boundingRect(0,0,int(self.textMaxWidth_PW),0, Qt.AlignCenter | Qt.TextWordWrap, curText)       
        self.width_priorityWord = bounding_rect.width()    
        self.toggleStartX = self.sizes.padding_large + (self.width_priorityWord/2) - (self.sizes.width_toggle/2) 
        # Delete button width
        curText = "Delete"
        fontMetrics = QFontMetrics(self.font_deleteButton)
        bounding_rect = fontMetrics.boundingRect(0,0,0,0, Qt.AlignCenter, curText)
        self.width_deleteButton = bounding_rect.width()
        height_deleteButton = bounding_rect.height()
        self.height_wPad_delButton = height_deleteButton + (self.buttonPadding*2) # height with button padding
        width_wPad_delButton = self.width_deleteButton + (self.buttonPadding*2) # width with button padding
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
        # Width of the word and definition area
        self.width_wordDef = self.APIwidth - width_excludeWordDef
        # Starting position of word and definition area
        self.startX_wordAndDef = width_excludeWordDef - (self.sizes.padding_large*2)
  
    def getSingleLineTextHeight(self):                            
        fontMetrics = QFontMetrics(self.font_wordAndDef)       
        bounding_rect = fontMetrics.boundingRect(0,0,int(self.width_wordDef),0, Qt.AlignCenter, "A")       
        self.singleLineTextHeight = bounding_rect.height()  

    def makeDict(self):
        self.wordDefDetails = [{} for _ in range(self.numWordDefs)]
        for i in range(self.numWordDefs):
            self.wordDefDetails[i]['ID'] = i

    def putEachWordAndDefInOneLine(self):        
        for i in range(self.numWordDefs):
            wordDef = self.dataIn[i]["word"] + ": " + self.dataIn[i]["definition"]
            wordDef_withHyphens = self.softHypenLongWords(wordDef)
            self.wordDefDetails[i]['wordAndDef'] = wordDef_withHyphens

    def softHypenLongWords(self, text, max_word_length=15):
        # Add soft hyphens to long words, which are only used if the word needs to be wrapped
        words = text.split()  # Split text by spaces
        wrapped_words = []
        for word in words:
            if len(word) > max_word_length:
                # Insert soft hyphens at every max_word_length characters for long words
                wrapped_word = '\u00AD'.join([word[i:i+max_word_length] for i in range(0, len(word), max_word_length)]) # list comprehensions for storing each part of the long word, and then using join to join them all with soft hyphens in between
                wrapped_words.append(wrapped_word)
            else:
                wrapped_words.append(word)
        # Join words back with spaces
        return ' '.join(wrapped_words)

    def wordDefHeight(self,text):
        fontMetrics = QFontMetrics(self.font_wordAndDef)                
        bounding_rect = fontMetrics.boundingRect(0,0,int(self.width_wordDef),0, Qt.AlignLeft | Qt.TextWordWrap, text)       
        return bounding_rect.height()
        
    def getAllWordDefHeights(self):
        for i in range(self.numWordDefs):
            curText = self.wordDefDetails[i]['wordAndDef']
            self.wordDefDetails[i]['textHeight'] = self.wordDefHeight(curText)

    def getTotalTextAreaHeight(self):
        self.totalTextheight = 0
        for i in range(self.numWordDefs - 1, -1, -1): # reverse order because the most recently added word is at the top of the list in the API
            curRowHeight = max(self.wordDefDetails[i]['textHeight'],self.height_wPad_delButton) # the minimum row height is the size of the delete button
            if i < self.numWordDefs - 1: # if not the last word, add the vertical spacing between words/defs
                self.totalTextheight += (curRowHeight + self.Vspacing_wordDefs)
            else:
                self.totalTextheight += curRowHeight

    def makeTitles(self):
        # 'Priority words' title
        text = 'Priority word'
        textAlignment = Qt.AlignCenter
        centerH = self.sizes.padding_large + (self.width_priorityWord/2)
        textPos = (centerH, self.startY, self.width_priorityWord, 0)
        ST_priorityWordTitle = StaticText(self.window,self.font_priortyWordTitle,text,textPos,textAlignment)         
        ST_priorityWordTitle.centerAlign_H()
        ST_priorityWordTitle.makeTextObject()
        self.bottomOfPWtitle = ST_priorityWordTitle.positionAdjust[1] + ST_priorityWordTitle.positionAdjust[3]
        # 'Word: definition
        text = 'Word: definition'
        textAlignment = Qt.AlignVCenter | Qt.AlignLeft                
        textPos = (self.startX_wordAndDef+4, self.bottomOfPWtitle, self.width_wordDef, 0)
        ST_wordDefTitle = StaticText(self.window,self.font_priortyWordTitle,text,textPos,textAlignment)         
        ST_wordDefTitle.alignBottom()
        ST_wordDefTitle.makeTextObject()
        
    def getWordListYStart(self):
        self.topOfScrollArea = self.bottomOfPWtitle
        self.startY = self.topOfScrollArea + self.VspaceAfterSmallTitles

    def makeScrollableArea(self):
        # Create scrollable area for the current words/defs
        self.scroll_area = QScrollArea(self.window) # scroll area inside the 'window' parent
        self.scroll_area.setGeometry(0, self.topOfScrollArea, self.APIwidth, self.APIheight-self.topOfScrollArea)  # Set the size of the API area which can be scrolled
        self.scroll_area.setFrameShape(QFrame.NoFrame) # Remove border from around the scroll area
        # Create a widget to contain the scrollable area's contents        
        self.scrollable_content = QWidget()
        self.scrollable_content.setFixedSize(self.APIwidth, self.totalTextheight+self.sizes.padding_large)  # Set size of the scrollable content

    def addScrollableContent(self):
        # Set scroll area properties (should be set after the scrollable content is populated)
        self.scroll_area.setWidget(self.scrollable_content)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Disable horizontal scrolling
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded) 

    def updateScrollAreaHeight(self):
        # For updating the scroll area height after a word is added/removed/edited
        self.scrollable_content.setFixedSize(self.APIwidth, self.totalTextheight+self.sizes.padding_large)     
        
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
        curToggleHandle.show()
        # Create function for when a toggle is clicked
        indToggle = self.wordDefDetails[ind]['ID']
        curToggleHandle.clicked.connect(lambda _, index=indToggle: self.toggleClicked_updateJSON(index))
        # Store toggle handle
        self.wordDefDetails[ind]['priorityWordTogggles'] = curToggleHandle 

    def makeDeleteButton(self,curRowTop,ind):  
        # Make button            
        text = 'Delete'        
        position = (self.startX_delButton,curRowTop,0,0)
        pushButton_del = PushButton(self.scrollable_content,self.font_deleteButton,text,position) 
        pushButton_del.setButtonPadding(self.buttonPadding,self.buttonPadding)
        DelButton = pushButton_del.makeButton()  
        DelButton.show()           
        # Make function for each button
        indDelButton = self.wordDefDetails[ind]['ID']
        DelButton.clicked.connect(lambda _, index=indDelButton: self.deleteButtonPressed(index))
        # Store button handle
        self.wordDefDetails[ind]['DeleteButtons'] = DelButton             
        
    def makeEditButton(self,curRowTop,ind):
        # Make button             
        text = 'Edit'        
        position = (self.startX_editButton,curRowTop,0,0)
        pushButton_edit = PushButton(self.scrollable_content,self.font_deleteButton,text,position) 
        pushButton_edit.setButtonPadding(self.buttonPadding,self.buttonPadding)        
        EditButton = pushButton_edit.makeButton()  
        EditButton.show()
        # Make function for each button               
        indEditButton = self.wordDefDetails[ind]['ID']
        EditButton.clicked.connect(lambda _, index=indEditButton: self.editButtonPressed(index))
        # Store button handle
        self.wordDefDetails[ind]['EditButtons'] = EditButton                   
      
    def makeWordDefText(self,curRowTop,ind):  
        # Print text for current word/def
        curRowTop += (self.height_wPad_delButton/2) - (self.singleLineTextHeight/2)
        textAlignment = Qt.AlignVCenter | Qt.AlignLeft        
        text = self.wordDefDetails[ind]['wordAndDef']            
        textPos = (self.startX_wordAndDef, curRowTop, self.width_wordDef, 0)
        curSTob = StaticText(self.scrollable_content,self.font_wordAndDef,text,textPos,textAlignment)
        wordAndDefTextOb = curSTob.makeTextObject()  
        # Store text handle   
        self.wordDefDetails[ind]['wordAndDefTextOb'] = wordAndDefTextOb  

    def makeInitialWordList(self):
        # For all words in json file on loading the API
        curRowTop = self.VspaceAfterSmallTitles # Starting row top position        
        for i in range(self.numWordDefs - 1, -1, -1):
            # Make API things
            self.makeToggle(curRowTop,i)
            self.makeDeleteButton(curRowTop,i)
            self.makeEditButton(curRowTop,i)
            self.makeWordDefText(curRowTop,i)
            # Set new row top position
            rowHeight = max(self.wordDefDetails[i]['textHeight'],self.height_wPad_delButton) # the minimum possible row height is the delete button height
            curRowTop = curRowTop + rowHeight + self.Vspacing_wordDefs              

    def updateAPIwithNewEntry(self,newWord,newDef):
        self.dataIn = readJSONfile(self.jsonFileName)
        # What is run when the 'Add' button at the top of the API is pressed, to add a new word and definition
        # Update number of words
        self.numWordDefs += 1   
        # Add new word/def details to dict (wordDefDetails)
        self.updateDictWithNewWord(newWord,newDef) # add new word to list and get its details, including height
        # Update (increase) scrollable area
        self.getTotalTextAreaHeight()
        self.updateScrollAreaHeight()   
        # Push all other words down
        newWordHeight = self.wordDefDetails[self.numWordDefs-1]['textHeight']
        nudge = max(newWordHeight,self.height_wPad_delButton) + self.Vspacing_wordDefs
        indicesToNudge = range(self.numWordDefs-1) # the words to nudge down (everything underneath the newly added word, whih is all other words, because the new word is added to the top)
        self.nudgeRowsUpOrDown(nudge,indicesToNudge)        
        # Add new word/def and related things (buttons, toggle) to top row
        self.makeWordDefText(self.VspaceAfterSmallTitles,self.numWordDefs-1)
        self.makeToggle(self.VspaceAfterSmallTitles,self.numWordDefs-1)
        self.makeDeleteButton(self.VspaceAfterSmallTitles,self.numWordDefs-1)
        self.makeEditButton(self.VspaceAfterSmallTitles,self.numWordDefs-1)  

    def updateDictWithNewWord(self,newWord,newDef):                
        # New word details
        textOnOneLine = newWord + ": " + newDef # word and definition in one line
        textOnOneLine_softHyphen = self.softHypenLongWords(textOnOneLine) # soft hyphenate
        wordDefHeight = self.wordDefHeight(textOnOneLine_softHyphen) # get text height
        # Make entry
        new_entry = {'ID': self.numWordDefs,
                     'wordAndDef': textOnOneLine_softHyphen,
                     'textHeight': wordDefHeight,                     
                     'priorityWordTogggles': None,
                     'DeleteButtons': None,
                     'EditButtons': None,
                     'wordAndDefTextOb': None                     
                     }
        # Add entry        
        self.wordDefDetails.append(new_entry)               
    
    def nudgeRowsUpOrDown(self,nudge,indicesToNudge):
        for i in indicesToNudge:
            self.adjustTopPosition(self.wordDefDetails[i]['priorityWordTogggles'],nudge)
            self.adjustTopPosition(self.wordDefDetails[i]['DeleteButtons'],nudge)
            self.adjustTopPosition(self.wordDefDetails[i]['EditButtons'],nudge)
            self.adjustTopPosition(self.wordDefDetails[i]['wordAndDefTextOb'],nudge)
            
    def adjustTopPosition(self,handle,nudge):
        curGeometry = handle.geometry()
        handle.setGeometry(curGeometry.x(),curGeometry.y()+nudge,curGeometry.width(),curGeometry.height())                          

    def toggleClicked_updateJSON(self,ID):
        index = self.findIDIndex(ID)
        curToggleState = self.wordDefDetails[index]['priorityWordTogggles'].isChecked()
        # Change json data
        if curToggleState:
            self.dataIn[index]["is_POD"] = True
        else:
            self.dataIn[index]["is_POD"] = False
        # Save json data    
        self.writeToJson()

    def deleteButtonPressed(self, ID):        
        index = self.findIDIndex(ID)    
        # Confirm delete with dialog
        deleteDialog = DeleteWordDialog(self.fonts,self.window)
        result = deleteDialog.exec_()
        # Delete word from API and json
        if result == 1: # if delete confirmed
            # Store row height before deletion (for nudging words below current word up)
            nudge = max(self.wordDefDetails[index]['textHeight'],self.height_wPad_delButton)                           
            # Delete the word row from the API and dict
            self.deleteIndexInList(index)            
            # Nudge everything to accomodate deletion              
            if self.numWordDefs != index:          
                wordsToNudge = range(index) # only nudge words up to the deleted word
                self.nudgeRowsUpOrDown(-nudge-self.Vspacing_wordDefs,wordsToNudge)
            # Delete word from 'dataIn' and write json data back to json file
            del self.dataIn[index]
            self.writeToJson()
            # Update number of words
            self.numWordDefs -= 1
            # Update scroll area
            self.getTotalTextAreaHeight()
            self.updateScrollAreaHeight()  

    def makeNewDataIn(self,newWord,newDef):
        self.dataIn = [{
            "word": newWord,
            "definition": newDef,
            "WOD_shown": False,
            "is_POD": False,
            "POD_shown": False
            }]        

    def writeToJson(self):
        with open(self.jsonFileName, 'w') as file:
            json.dump(self.dataIn, file, indent=4)    

    def findIDIndex(self,ID):
        # Get position (index) of the current word/def in self.wordDefDetails, which will be the same index in the json data (dataIn)
        pos = None
        k = 0
        for item in self.wordDefDetails:
            if item['ID'] == ID:
                pos = k
                break  
            k+=1
        return pos            

    def deleteIndexInList(self,indexToDel):
        # Remove each widget (e.g., toggle) from the current dictionary index
        for _, item in self.wordDefDetails[indexToDel].items():            
            if isinstance(item, QWidget):
                item.deleteLater()  
        # Finally remove the empty dictionary index, including all non-widget things (e.g., str)
        del self.wordDefDetails[indexToDel]    

    def editButtonPressed(self, ID):
        index = self.findIDIndex(ID)   
        # Get word and definition separatly (only together in wordDefDetails) 
        word = self.dataIn[index]['word']
        definition = self.dataIn[index]['definition']
        # Run dialog box for the user to edit the word and/or definition
        editDialog = EditWordDialog(self.fonts,self.window,word,definition)
        result = editDialog.exec_()
        if result == 1: # If the user wants to save the edit
            # Get the new word and definition from the dialog text entry boxes
            new_word, new_definition = editDialog.getNewText() 
            self.dataIn[index]['word'] = new_word
            self.dataIn[index]['definition'] = new_definition
            # Put word and definition together, and update the dict (wordDefDetails)
            newWordDef = self.dataIn[index]["word"] + ": " + self.dataIn[index]["definition"]
            self.wordDefDetails[index]['wordAndDef'] = self.softHypenLongWords(newWordDef)            
            # Save the previous text height and top   
            prevTextHeight = self.wordDefDetails[index]['textHeight']    
            prevTextTop = self.wordDefDetails[index]['wordAndDefTextOb'].geometry().y()
            # Get the newly edited text height, and update wordDefDetails with this 
            newTextHeight = self.wordDefHeight(self.wordDefDetails[index]['wordAndDef'])
            self.wordDefDetails[index]['textHeight'] = newTextHeight
            # Difference in previous and newly edited text heights - for nudging the other word/def rows accordingly           
            diffHeights = newTextHeight - prevTextHeight               
            # Delete the word/def and then make anew (with edited version)
            self.wordDefDetails[index]['wordAndDefTextOb'].deleteLater()
            topPoint = prevTextTop - (self.height_wPad_delButton/2) + (self.singleLineTextHeight/2)
            self.makeWordDefText(topPoint,index)   
            # Nudge the rows below up or down depending on whether the word/def got shorter or longer
            if diffHeights != 0:
                nudge = max(newTextHeight,self.height_wPad_delButton) - max(prevTextHeight,self.height_wPad_delButton)            
                wordsToNudge = range(index)
                self.nudgeRowsUpOrDown(nudge,wordsToNudge)                                                                                     
            # Adjust scroll area
            self.getTotalTextAreaHeight()
            self.updateScrollAreaHeight() 
            # Save newly edited word/def to json file
            self.writeToJson()
            
class DeleteWordDialog(QDialog):
    def __init__(self, fonts, window):
        # Inheritance
        super().__init__(window)
        # Inputs
        self.fonts = fonts
        self.window = window    
        # Some details
        self.paddingEdge = 30                    
        self.butPad = 7
        self.dialogText = 'Are you sure you want to delete this word?'
        # Run initiation functions
        self.dialogStarterProperties()
        self.getTextAndAPIWidth()
        self.makeDialogText()
        self.getButtonPositions()
        self.makeDeleteButton()
        self.makeCancelButton()
        self.resizeAPI()
        centerWindowOnScreen(self.window)

    def dialogStarterProperties(self):
        self.setWindowTitle('Confirm delete')        

    def getTextAndAPIWidth(self):               
        fontMetrics = QFontMetrics(self.fonts.font_medium)
        bounding_rect = fontMetrics.boundingRect(0,0,0,0, Qt.AlignCenter, self.dialogText)
        self.width_text = bounding_rect.width()
        self.width_API = self.width_text + self.paddingEdge*2  

    def makeDialogText(self):                  
        textPos = (self.width_API/2, self.paddingEdge, self.width_text, 0)
        self.ST_deleteWord = StaticText(self,self.fonts.font_medium,self.dialogText,textPos,Qt.AlignCenter)
        self.ST_deleteWord.centerAlign_H()
        self.ST_deleteWord.makeTextObject()                        

    def getButtonPositions(self):
        self.buttonWidth = (self.width_text - self.paddingEdge - (self.butPad*4)) / 2
        self.leftButtonCen = self.paddingEdge + self.butPad + self.buttonWidth/2
        self.rightButtonCen = self.paddingEdge + self.butPad + self.buttonWidth \
                + self.paddingEdge + self.butPad + self.buttonWidth/2        
        self.buttonStartY = self.ST_deleteWord.positionAdjust[1] + \
                self.ST_deleteWord.positionAdjust[3] + self.paddingEdge*2  
    
    def makeDeleteButton(self):                            
        text = 'Delete'        
        position = (self.leftButtonCen,self.buttonStartY,self.buttonWidth,0)
        pushButton_del = PushButton(self,self.fonts.font_medium,text,position) 
        pushButton_del.setButtonPadding(self.butPad,self.butPad)
        pushButton_del.centerAlign_H()
        DelButton = pushButton_del.makeButton()                 
        DelButton.clicked.connect(self.accept) # Set the 'result' of this button to True
        self.height = pushButton_del.positionAdjust[1] + pushButton_del.positionAdjust[3] + self.paddingEdge        

    def makeCancelButton(self):        
        text = 'Cancel'        
        position = (self.rightButtonCen,self.buttonStartY,self.buttonWidth,0)
        pushButton_cancel = PushButton(self,self.fonts.font_medium,text,position) 
        pushButton_cancel.setButtonPadding(self.butPad,self.butPad)
        pushButton_cancel.centerAlign_H()            
        CancelButton = pushButton_cancel.makeButton()              
        CancelButton.clicked.connect(self.reject) # Set the 'result' of this button to False     
            
    def resizeAPI(self):
        self.setFixedSize(self.width_API, self.height)

class EditWordDialog(QDialog):
    def __init__(self, fonts, window, word, definition):
        # Inheritance
        super().__init__(window)
        # Inputs
        self.fonts = fonts
        self.window = window
        self.word = word
        self.definition = definition
        self.padding = 15
        self.smallGap = 6
        self.boxWidth = 400
        self.boxHeight = 40
        self.lowestPoint = 0
        self.buttonWidth = 100         
        # Functions to run 
        self.dialogStarterProperties()
        self.makeEditBoxTitle_word()
        self.makeEditBox_word()
        self.makeEditBoxTitle_def()
        self.makeEditBox_definition()
        self.makeSaveButton()
        self.makeCancelButton()
        self.resizeAPI()
        centerWindowOnScreen(self.window)

    def dialogStarterProperties(self):
        self.setWindowTitle('Edit word')  

    def makeEditBoxTitle_word(self):            
        text = 'Word'
        textAlignment = Qt.AlignLeft | Qt.AlignVCenter
        textPos = (self.padding, self.padding, self.boxWidth, 0)
        self.ST_wordTitle = StaticText(self,self.fonts.font_medium,text,textPos,textAlignment)                 
        self.ST_wordTitle.makeTextObject()
        self.lowestPoint = self.ST_wordTitle.positionAdjust[1] + self.ST_wordTitle.positionAdjust[3]

    def makeEditBox_word(self):     
        self.wordInput = QLineEdit(self)    
        top = self.lowestPoint + self.smallGap
        self.wordInput.setGeometry(self.padding, top, self.boxWidth, self.boxHeight )
        self.wordInput.setFont(self.fonts.font_medium)
        self.wordInput.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.wordInput.setStyleSheet("QLineEdit { border: 1px solid black; }")        
        self.wordInput.setText(self.word)
        self.wordInput.setCursorPosition(0) 
        self.lowestPoint = top + self.wordInput.height()

    def makeEditBoxTitle_def(self):            
        text = 'Definition'
        textAlignment = Qt.AlignLeft | Qt.AlignVCenter  
        top = self.lowestPoint + self.padding      
        textPos = (self.padding, top, self.boxWidth, 0)
        self.ST_defTitle = StaticText(self,self.fonts.font_medium,text,textPos,textAlignment)                 
        self.ST_defTitle.makeTextObject()
        self.lowestPoint = self.ST_defTitle.positionAdjust[1] + self.ST_defTitle.positionAdjust[3]

    def makeEditBox_definition(self):     
        self.defInput = QLineEdit(self)    
        top = self.lowestPoint + self.smallGap
        self.defInput.setGeometry(self.padding, top, self.boxWidth, self.boxHeight )
        self.defInput.setFont(self.fonts.font_medium)
        self.defInput.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.defInput.setStyleSheet("QLineEdit { border: 1px solid black; }")        
        self.defInput.setText(self.definition)
        self.defInput.setCursorPosition(0) 
        self.lowestPoint = top + self.defInput.height()

    def makeSaveButton(self):        
        text = 'Save'        
        self.top = self.lowestPoint + self.padding*2
        position = (self.padding,self.top,self.buttonWidth,0)
        pushButton_save = PushButton(self,self.fonts.font_medium,text,position)                 
        saveButton = pushButton_save.makeButton()              
        saveButton.clicked.connect(self.accept) # Make the 'result' of this button True
        self.lowestPoint = self.top + saveButton.height()

    def makeCancelButton(self):        
        text = 'Cancel'                
        right = self.padding + self.boxWidth
        position = (right,self.top,self.buttonWidth,0)
        pushButton_cancel = PushButton(self,self.fonts.font_medium,text,position)                 
        pushButton_cancel.rightAlign()
        cancelButton = pushButton_cancel.makeButton()              
        cancelButton.clicked.connect(self.reject) # Make the 'result' of this button False

    def resizeAPI(self):
        width = self.boxWidth + (self.padding*2)
        height = self.lowestPoint+self.padding
        self.setFixedSize(width, height)

    def getNewText(self):
        # For returning the newly edited word and/or definition
        return self.wordInput.text(), self.defInput.text()    