from PyQt5.QtGui import QFont, QTextDocument, QFontMetrics
from PyQt5.QtWidgets import QLabel, QScrollArea 
from PyQt5.QtCore import Qt

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

def calculateTextboxDim(text, width, font=None, textAlignment=None):
    
    # Create a QTextDocument to measure text
    doc = QTextDocument()
    
    # Set the text width
    doc.setTextWidth(width)
    
    # Apply text font
    if font:
        doc.setDefaultFont(font)
    
    # Set the text
    doc.setPlainText(text)
    
    # Set text alignment
    if textAlignment:
        text_option = doc.defaultTextOption()
        text_option.setAlignment(textAlignment)
        doc.setDefaultTextOption(text_option)
    
    # Calculate the required height for the document
    height = doc.size().height()
    
    return height

def centerWindowOnScreen(window, app):
    frameGm = window.frameGeometry()
    screen = app.primaryScreen()
    centerPoint = screen.availableGeometry().center()
    frameGm.moveCenter(centerPoint)
    window.move(frameGm.topLeft())   

class MakeTextWithMaxHeight:
    def __init__(self, window, text, leftPos, topPos, width, maxHeight, font, textAlignment):
        # Parameters
        self.window = window
        self.text = text
        self.leftPos = leftPos
        self.topPos = topPos
        self.width = width
        self.maxHeight = maxHeight
        self.font = font
        self.textAlignment = textAlignment
        self.setWordWrap = True
        # Methods        
        self.textHeight = self.getTextHeight()        
        if self.textHeight > self.maxHeight:
            self.textPos = (leftPos,topPos,width,self.maxHeight)
            self.showText()
            self.makeVerticalScrollBar()
        else:
            self.textPos = (leftPos,topPos,width,self.textHeight)
            self.showText()                    

    def getTextHeight(self):
        
        # Create a QTextDocument to measure text
        doc = QTextDocument()
        
        # Set the text width
        doc.setTextWidth(self.width)
        
        # Apply text font
        if self.font:
            doc.setDefaultFont(self.font)
        
        # Set the text
        doc.setPlainText(self.text)
        
        # Set text alignment
        if self.textAlignment:
            text_option = doc.defaultTextOption()
            text_option.setAlignment(self.textAlignment)
            doc.setDefaultTextOption(text_option)
        
        # Calculate the required height for the document
        height = doc.size().height()
        
        return height
    
    def showText(self):
        self.textBox = QLabel(self.text,self.window)
        self.textBox.setWordWrap(self.setWordWrap) 
        self.textBox.setAlignment(self.textAlignment) 
        self.textBox.setGeometry(*(int(x) for x in self.textPos))  
        self.textBox.setFont(self.font)          

    def makeVerticalScrollBar(self):
        self.scroll_area = QScrollArea(self.window)
        self.scroll_area.setWidgetResizable(True)  
        self.scroll_area.setWidget(self.textBox)  
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  
        self.scroll_area.setGeometry(*(int(x) for x in self.textPos))    

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