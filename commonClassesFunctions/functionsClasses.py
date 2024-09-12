from PyQt5.QtGui import QFont, QTextDocument, QFontMetrics
from PyQt5.QtWidgets import QLabel, QScrollArea, QPushButton
from PyQt5.QtCore import Qt

class Fonts:
    def __init__(self):
        # Initialize fonts
        self.font_tiny = None
        self.font_small = None
        self.font_small_italic = None
        self.font_small_italic_bold = None
        self.font_medium = None
        self.font_large = None
        self.font_large_bold = None
        # Default values
        self.fontFamily = "Arial"
    
    def makeFonts(self):
        self.font_tiny = QFont(self.fontFamily, 8, QFont.Normal, False)
        self.font_small = QFont(self.fontFamily, 9, QFont.Normal, False)
        self.font_small_italic = QFont(self.fontFamily, 9, QFont.Normal, True)
        self.font_small_italic_bold = QFont(self.fontFamily, 9, QFont.Bold, True)
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
        self.textPos = None
        # Methods        
        self.textHeight = self.getTextHeight()   
        self.getTextPos()                   

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
    
    def getTextPos(self):
        if self.textHeight > self.maxHeight:
            self.textPos = (self.leftPos,self.topPos,self.width,self.maxHeight)
        else:
            self.textPos = (self.leftPos,self.topPos,self.width,self.textHeight)

    def centerH(self):
            self.textPos = (self.textPos[0] - (self.width / 2), self.textPos[1],self.textPos[2],self.textPos[3])

    def makeText(self):
        self.showText()
        if self.textHeight > self.maxHeight:                    
            self.makeVerticalScrollBar()               
    
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

    def editText(self):
        self.textBox.setText(self.text)

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
        textOb.show()
        return textOb
    
# Create a single line push button
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
        self.textAlignment = Qt.AlignVCenter | Qt.TextWordWrap | Qt.AlignHCenter
        # Constructor functions
        self.getActualPosition()
        self.getVandHcenter()

    def getActualPosition(self):
        if self.position[2] == 0: # if width given
            text_width = self.fontMetrics.horizontalAdvance(self.text)             
        else:
            text_width = self.position[2]              
        text_height = self.fontMetrics.height()                
        self.positionAdjust = [int(self.position[0]), int(self.position[1]), \
                                int(text_width+self.buttonPadding*2), int(text_height+self.buttonPadding*2)]

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
        button.setStyleSheet("QPushButton { text-align: center }")
        return button       