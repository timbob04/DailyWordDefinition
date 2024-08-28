from PyQt5.QtGui import QFont, QTextDocument

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
