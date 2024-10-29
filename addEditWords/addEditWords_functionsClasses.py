from PyQt5.QtWidgets import QLineEdit, QCheckBox, QScrollArea, QWidget, QFrame, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics
import json
from commonClassesFunctions.functionsClasses import StaticText, PushButton

class Sizes_addEditWords:
    def __init__(self):
        self.padding_small = None
        self.padding_medium = None
        self.padding_large = None
        self.APIwidth = None
        self.APIheight = None
        self.width_toggle = None

    def defineSizes(self):
        self.padding_small = 5
        self.padding_medium = 10
        self.padding_large = 20
        self.APIwidth = 1400
        self.APIheight = 1000
        self.width_toggle = 22

class addNewWordTextBoxes:
    def __init__(self,window,sizes,fonts,dataIn,jsonFileName):
        self.window = window
        self.sizes = sizes
        self.fonts = fonts 
        self.dataIn = dataIn        
        self.jsonFileName = jsonFileName
        self.addWordInput = None
        self.addDefInput = None   
        self.newWord = None
        self.newDefinition = None        

    def makeAddWordEditTextBox(self,left,top,width):    
        self.addWordInput = QLineEdit(self.window)    
        self.addWordInput.setGeometry(int(left), int(top), int(width), 40 )
        self.addWordInput.setFont(self.fonts.font_mediumLarge)
        self.addWordInput.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.addWordInput.setStyleSheet("QLineEdit { border: 1px solid black; }")

    def makeAddDefEditTextBox(self,left,top,width):    
        self.addDefInput = QLineEdit(self.window)    
        self.addDefInput.setGeometry(int(left), int(top), int(width), 40 )
        self.addDefInput.setFont(self.fonts.font_mediumLarge)
        self.addDefInput.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.addDefInput.setStyleSheet("QLineEdit { border: 1px solid black; }")

    def getNewWordDef(self):
        self.newWord = self.addWordInput.text()
        self.newDefinition = self.addDefInput.text()            
    
    def addWordToJSONfile(self):            
        # Make the new word/def json entry
        new_entry = {
            "word": self.newWord,
            "definition": self.newDefinition,
            "WOD_shown": False,
            "is_POD": False,
            "POD_shown": False
            }
        # Append new word/def to current word/def json list
        self.dataIn.append(new_entry)
        # Save new list with new word/def
        with open(self.jsonFileName, 'w') as file:
            json.dump(self.dataIn, file, indent=4) 

    def clearEditTextBoxes(self):
        self.addWordInput.clear()
        self.addDefInput.clear()

    def AddButtonPressed(self):
        self.getNewWordDef()
        self.addWordToJSONfile()        
        self.clearEditTextBoxes()        

        
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
        self.makeDict()
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

    def makeDict(self):
        for i in range(self.numWordDefs):
            self.wordDefDetails[i]['ID'] = i

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
        curToggleHandle.show()
        # Store toggle handle
        self.wordDefDetails[ind]['priorityWordTogggles'] = curToggleHandle 

    def makeDeleteButton(self,curRowTop,ind):              
        text = 'Delete'        
        position = (self.startX_delButton,curRowTop,0,0)
        pushButton_del = PushButton(self.scrollable_content,self.font_deleteButton,text,position) 
        pushButton_del.setButtonPadding(self.buttonPadding,self.buttonPadding)
        DelButton = pushButton_del.makeButton()  
        DelButton.show()           
        indDelButton = self.wordDefDetails[ind]['ID']
        DelButton.clicked.connect(lambda _, index=indDelButton: self.deleteButtonPressed(index))
        self.wordDefDetails[ind]['DeleteButtons'] = DelButton             
        
    def makeEditButton(self,curRowTop,ind):              
        text = 'Edit'        
        position = (self.startX_editButton,curRowTop,0,0)
        pushButton_edit = PushButton(self.scrollable_content,self.font_deleteButton,text,position) 
        pushButton_edit.setButtonPadding(self.buttonPadding,self.buttonPadding)        
        EditButton = pushButton_edit.makeButton()  
        EditButton.show()                 
        indEditButton = self.wordDefDetails[ind]['ID']
        EditButton.clicked.connect(lambda _, index=indEditButton: self.editButtonPressedy(index))
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
        new_entry = {'ID': self.numWordDefs,
                     'wordAndDef': textOnOneLine,
                     'textHeight': wordDefHeight,                     
                     'priorityWordTogggles': None,
                     'DeleteButtons': None,
                     'EditButtons': None,
                     'wordAndDefTextOb': None                     
                     }
        self.wordDefDetails.append(new_entry)    
    
    def nudgeEverything(self,nudge,indicesToNudge):
        for i in indicesToNudge:
            self.adjustGeoWithNewHeight(self.wordDefDetails[i]['priorityWordTogggles'],nudge)
            self.adjustGeoWithNewHeight(self.wordDefDetails[i]['DeleteButtons'],nudge)
            self.adjustGeoWithNewHeight(self.wordDefDetails[i]['EditButtons'],nudge)
            self.adjustGeoWithNewHeight(self.wordDefDetails[i]['wordAndDefTextOb'],nudge)
            
    def adjustGeoWithNewHeight(self,handle,nudge):
        curGeometry = handle.geometry()            
        handle.setGeometry(curGeometry.x(),curGeometry.y()+nudge,curGeometry.width(),curGeometry.height())        

    def updateAPIwithNewEntry(self,newWord,newDef):
        self.numWordDefs += 1   
        self.updateListWithNewWord(newWord,newDef) # add new word to list and get its details, including height
        self.getTotalTextAreaHeight()
        self.updateScrollAreaHeight()   
        # Push all other words down
        newWordHeight = self.wordDefDetails[self.numWordDefs-1]['textHeight'] + self.Vspacing_wordDefs
        indicesToNudge = range(self.numWordDefs-1)
        self.nudgeEverything(newWordHeight,indicesToNudge)             
        # Add new word row to top
        self.makeWordDef(self.VspaceAfterSmallTitles,self.numWordDefs-1)
        self.makeToggle(self.VspaceAfterSmallTitles,self.numWordDefs-1)
        self.makeDeleteButton(self.VspaceAfterSmallTitles,self.numWordDefs-1)
        self.makeEditButton(self.VspaceAfterSmallTitles,self.numWordDefs-1)

    def deleteButtonPressed(self, ID):        
        index = self.findIDIndex(ID)    
        # Confirm delete with dialog
        deleteDialog = DeleteWordDialog(self.fonts,self.window)
        result = deleteDialog.exec_()
        # Delete word from API and json
        if result == 1:
            # Store row height before deletion (for nudging)
            wordTextHeight = self.wordDefDetails[index]['textHeight']
            curButton = self.wordDefDetails[index]['DeleteButtons']
            buttonHeight = curButton.height()
            rowHeight = max(wordTextHeight,buttonHeight)
            # Delete the word row from the API
            self.deleteIndexInList(index)            
            # Nudge everything to accomodate deletion  
            if self.numWordDefs != index:          
                wordsToNudge = range(index)
                self.nudgeEverything(-rowHeight-self.Vspacing_wordDefs,wordsToNudge)
            # If not the last word, every word below (so now index to end) needs to be nudged up to row spacer and the textHeight
            self.numWordDefs -= 1

    def findIDIndex(self,ID):
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

    def editButtonPressed(self, index):
        print("Using the index...")
        # First, bring up a dialog box to edit the word/def (biggish thing in itself)
        # Figure out the height of the new word/def
        # Then, if this is different from what is was....
        # Adjust the scollable area
        # Push everything below down (or up depending on the whether the difference is positive or negative)
        # And then edit the word/def
        # If the text height is the same after the user has edited it, just edit the word/def without moving anything around (above)
        
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

    def dialogStarterProperties(self):
        self.setWindowTitle('Confirm delete')        

    def getTextAndAPIWidth(self):               
        fontMetrics = QFontMetrics(self.fonts.font_medium)
        bounding_rect = fontMetrics.boundingRect(0,0,0,0, Qt.AlignCenter, self.dialogText)
        self.width_text = bounding_rect.width()
        self.width = self.width_text + self.paddingEdge*2  

    def makeDialogText(self):                  
        textPos = (self.width/2, self.paddingEdge, self.width_text, 0)
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
        DelButton.clicked.connect(self.accept)  
        self.height = pushButton_del.positionAdjust[1] + pushButton_del.positionAdjust[3] + self.paddingEdge        

    def makeCancelButton(self):        
        text = 'Cancel'        
        position = (self.rightButtonCen,self.buttonStartY,self.buttonWidth,0)
        pushButton_cancel = PushButton(self,self.fonts.font_medium,text,position) 
        pushButton_cancel.setButtonPadding(self.butPad,self.butPad)
        pushButton_cancel.centerAlign_H()            
        CancelButton = pushButton_cancel.makeButton()              
        CancelButton.clicked.connect(self.reject)     
            
    def resizeAPI(self):
        self.setFixedSize(self.width, self.height)



