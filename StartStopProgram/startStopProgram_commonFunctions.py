from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
import re

class Fonts:
    def __init__(self):
        # Initialize fonts
        self.font_tiny = None
        self.font_small = None
        self.font_medium = None
        self.font_large = None
        self.font_large_bold = None
        # Default values
        self.fontFamily = "Arial"
    
    def makeFonts(self):
        self.font_tiny = QFont(self.fontFamily, 8, QFont.Normal, False)
        self.font_small = QFont(self.fontFamily, 9, QFont.Normal, False)
        self.font_medium = QFont(self.fontFamily, 11, QFont.Normal, False)
        self.font_large = QFont(self.fontFamily, 17, QFont.Normal, False)    
        self.font_large_bold = QFont(self.fontFamily, 17, QFont.Bold, False)

# Create static text boxes
class StaticText:
    def __init__(self, window, font, text, position, textAlignment):
        # Input values
        self.window = window
        self.font = font
        self.text = text
        self.textAlignment = textAlignment
        self.position = position
        # Default values
        self.wordWrap = True
        self.fontMetrics = QFontMetrics(font)  
        self.color = 'black'
        # Initialize some variables
        self.positionAdjust = None
        self.Vcenter = None
        self.Hcenter = None    
        # Constructor functions
        self.getActualPosition()
        self.getVandHcenter()

    def getActualPosition(self):
        bounding_rect = self.fontMetrics.boundingRect(0,0,int(self.position[2]),int(self.position[3]), self.textAlignment, self.text)       
        self.positionAdjust = [int(self.position[0]), int(self.position[1]), int(bounding_rect.width()), int(bounding_rect.height())]

    def getVandHcenter(self):
        self.Hcenter = self.positionAdjust[0] + self.positionAdjust[2]/2
        self.Vcenter = self.positionAdjust[1] + self.positionAdjust[3]/2

    def centerAlign_V(self):
        self.positionAdjust[1] = int(self.positionAdjust[1] - self.positionAdjust[3]/2)

    def centerAlign_H(self):
        self.positionAdjust[0] = int(self.positionAdjust[0] - self.positionAdjust[2]/2)
            
    def makeTextObject(self):
        textOb = QLabel(self.text, self.window)
        textOb.setWordWrap(self.wordWrap)    
        textOb.setFont(self.font)
        textOb.setAlignment(self.textAlignment)
        textOb.setGeometry(*self.positionAdjust) 
        textOb.setStyleSheet(f"QLabel {{ color : {self.color}; }}")
        return textOb
    
# Create push button
class PushButton:
    def __init__(self, window, font, text, position):
        # Input values
        self.window = window
        self.font = font
        self.text = text        
        self.position = position
        # Default values
        self.wordWrap = True
        self.fontMetrics = QFontMetrics(font)        
        self.positionAdjust = None
        self.Vcenter = None
        self.Hcenter = None
        self.buttonPadding = 7
        self.textAlignment = Qt.AlignLeft | Qt.AlignVCenter | Qt.TextWordWrap 
        # Constructor functions
        self.getActualPosition()
        self.getVandHcenter()

    def getActualPosition(self):
        bounding_rect = self.fontMetrics.boundingRect(0,0,int(self.position[2]),int(self.position[3]), self.textAlignment, self.text)       
        self.positionAdjust = [int(self.position[0]), int(self.position[1]), \
                                int(bounding_rect.width()+self.buttonPadding*2), int(bounding_rect.height()+self.buttonPadding*2)]

    def getVandHcenter(self):
        self.Hcenter = self.positionAdjust[0] + self.positionAdjust[2]/2
        self.Vcenter = self.positionAdjust[1] + self.positionAdjust[3]/2

    def centerAlign_V(self):
        self.positionAdjust[1] = int(self.positionAdjust[1] - self.positionAdjust[3]/2)

    def centerAlign_H(self):
        self.positionAdjust[0] = int(self.positionAdjust[0] - self.positionAdjust[2]/2)

    def rightAlign(self,rightPoint):
        diff = (self.positionAdjust[0] + self.positionAdjust[2]) - rightPoint 
        self.positionAdjust[0] = self.positionAdjust[0] - diff
            
    def makeButton(self):
        button = QPushButton(self.text, self.window)
        button.setGeometry(*(int(x) for x in self.positionAdjust))    
        button.setFont(self.font)
        button.setStyleSheet("QPushButton { text-align: center; }")
        return button    
    
# Create edit text box   
class EditText:
    def __init__(self, window, font, startingText, position):
        # Default values
        self.padding = 10
        self.textAlignment = Qt.AlignCenter | Qt.AlignVCenter
        self.fontMetrics = QFontMetrics(font)
        # Inputs
        self.window = window
        self.font = font
        self.startingText = startingText
        self.position = position  
        # Functions
        self.getActualPosition()

    def getActualPosition(self):
        bounding_rect = self.fontMetrics.boundingRect(0,0,0,0, self.textAlignment, self.startingText)       
        self.positionAdjust = [int(self.position[0]), int(self.position[1]), \
                                int(bounding_rect.width()+self.padding*2), int(bounding_rect.height()+self.padding)]

    def forceWidth(self):
        self.positionAdjust[2] = self.position[2]

    def centerAlign_V(self):
        self.positionAdjust[1] = int(self.positionAdjust[1] - self.positionAdjust[3]/2)

    def centerAlign_H(self):
        self.positionAdjust[0] = int(self.positionAdjust[0] - self.positionAdjust[2]/2)
            
    def makeEditTextBox(self):        
        editBox = QLineEdit(self.window) # Make edit box
        editBox.setText(self.startingText)
        editBox.setFont(self.font)              
        editBox.setFixedWidth(self.positionAdjust[2])  # Set the width of the text box to fit the text, with added padding
        editBox.setAlignment(self.textAlignment) 
        editBox.setGeometry(*(int(x) for x in self.positionAdjust))
        return editBox    
    
def centerWindowOnScreen(window, app):
    frameGm = window.frameGeometry()
    screen = app.primaryScreen()
    centerPoint = screen.availableGeometry().center()
    frameGm.moveCenter(centerPoint)
    window.move(frameGm.topLeft())   

  