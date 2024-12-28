from PyQt5.QtGui import QFont, QTextDocument, QFontMetrics
from PyQt5.QtWidgets import QLabel, QScrollArea, QPushButton, QApplication
from PyQt5.QtCore import Qt, QLibraryInfo, QCoreApplication
import json
import os
import psutil
import signal
import platform
import subprocess
import time
import sys
import ast

class Fonts:
    def __init__(self):
        # Initialize fonts
        self.font_tiny = None
        self.font_small = None
        self.font_small_italic = None
        self.font_small_italic_bold = None
        self.font_medium = None
        self.font_mediumLarge = None
        self.font_mediumLargeBold = None
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
        self.font_mediumLarge = QFont(self.fontFamily, 14, QFont.Normal, False)
        self.font_mediumLargeBold = QFont(self.fontFamily, 14, QFont.Bold, False)
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

def centerWindowOnScreen(window):
    frameGm = window.frameGeometry()
    # screen = app.primaryScreen()
    screen = QApplication.primaryScreen()
    centerPoint = screen.availableGeometry().center()
    frameGm.moveCenter(centerPoint)
    window.move(frameGm.topLeft())   

class MakeTextWithMaxHeight:
    def __init__(self, window, text, leftPos, topPos, width, maxHeight, font, textAlignment):
        # Parameters
        self.window = window 
        self.text = text    
        self.width = width  
        self.maxHeight = maxHeight 
        self.textPos = (leftPos,topPos,width,maxHeight)    
        self.font = font
        self.textAlignment = textAlignment
        self.setWordWrap = True
        self.getTextHeight()
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
        self.height = doc.size().height()         
    
    def getTextPos(self):
        if self.height <= self.maxHeight:
            self.textPos = (self.textPos[0],self.textPos[1],self.textPos[2],self.height)

    def centerH(self):
        self.textPos = (self.textPos[0] - (self.width / 2), self.textPos[1],self.textPos[2],self.textPos[3])              

    def adjustTextProperties(self):        
        self.textBox.setWordWrap(self.setWordWrap) 
        self.textBox.setAlignment(self.textAlignment) 
        self.textBox.setGeometry(*(int(x) for x in self.textPos))  
        self.textBox.setFont(self.font)          

    def makeVerticalScrollBar(self):
        self.scroll_area = QScrollArea(self.window)
        self.scroll_area.setWidgetResizable(True)     
        self.scroll_area.setGeometry(*(int(x) for x in self.textPos)) 
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn) # This is turned on when needed        
        self.scroll_area.show()  # Ensure it is shown
       
    def showText(self):
        if self.height > self.maxHeight:
            self.makeVerticalScrollBar()
            self.textBox = QLabel(self.text,self.scroll_area) # add text to scroll area
            self.scroll_area.setWidget(self.textBox)
            self.adjustTextProperties()
        else:
            self.textBox = QLabel(self.text,self.window) # add text to main window
            self.adjustTextProperties()
            self.textBox.show()  # Ensure it is shown
         
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
        if self.position[2] > 0:
            bounding_rect = self.fontMetrics.boundingRect(0,0,int(self.position[2]),int(self.position[3]), self.textAlignment | Qt.TextWordWrap, self.text)       
        else:
            bounding_rect = self.fontMetrics.boundingRect(0,0,int(self.position[2]),int(self.position[3]), self.textAlignment, self.text)       
        self.positionAdjust = [int(self.position[0]), int(self.position[1]), int(bounding_rect.width()), int(bounding_rect.height())]

    def getVandHcenter(self):
        self.Hcenter = self.positionAdjust[0] + self.positionAdjust[2]/2
        self.Vcenter = self.positionAdjust[1] + self.positionAdjust[3]/2

    def centerAlign_V(self):
        self.positionAdjust[1] = int(self.positionAdjust[1] - self.positionAdjust[3]/2)

    def centerAlign_H(self):
        self.positionAdjust[0] = int(self.positionAdjust[0] - self.positionAdjust[2]/2)

    def alignBottom(self):
        self.positionAdjust[1] = int(self.positionAdjust[1] - self.positionAdjust[3])
            
    def makeTextObject(self):
        textOb = QLabel(self.text, self.window)
        textOb.setWordWrap(True)    
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
        self.buttonPadding_H = 7
        self.buttonPadding_V = 7                
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
                                int(text_width+self.buttonPadding_H*2), int(text_height+self.buttonPadding_V*2)]

    def getVandHcenter(self):
        self.Hcenter = self.positionAdjust[0] + self.positionAdjust[2]/2
        self.Vcenter = self.positionAdjust[1] + self.positionAdjust[3]/2

    def centerAlign_V(self):
        self.positionAdjust[1] = int(self.positionAdjust[1] - self.positionAdjust[3]/2)

    def centerAlign_H(self):
        self.positionAdjust[0] = int(self.positionAdjust[0] - self.positionAdjust[2]/2)

    def rightAlign(self):
        self.positionAdjust[0] = self.positionAdjust[0] - self.positionAdjust[2] 

    def bottomAlign(self):
        self.positionAdjust[1] = self.positionAdjust[1] - self.positionAdjust[3]

    def setButtonPadding(self, padding_H, padding_V): # for adjusting the button padding
        self.buttonPadding_H = padding_H
        self.buttonPadding_V = padding_V
        self.getActualPosition() 
        self.getVandHcenter()      
            
    def makeButton(self):
        button = QPushButton(self.text, self.window)
        button.setGeometry(*(int(x) for x in self.positionAdjust))    
        button.setFont(self.font)
        button.setStyleSheet("QPushButton { text-align: center }")
        return button       
    
def getScreenWidthHeight():
    # Get screen geometry
    screen = QApplication.primaryScreen()
    screen_geometry = screen.availableGeometry()

    # Get the screen width and height
    width = screen_geometry.width()
    height = screen_geometry.height()

    return width, height    

def readJSONfile(filepath):
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
            return data
    except (json.JSONDecodeError, FileNotFoundError, IOError):
        return None
    
class PID:
    def __init__(self,pidFileName): 
        # Starter variables  
        self.pidFileName = pidFileName    
        self.PIDfilePath = None          
        self.PIDfileExists = False      
        self.PID = None
        self.PIDrunning = False
        # Starter methds
        self.getPIDfilePath()
        self.doesPIDfileExist()
        self.getPID()

    def getPIDfilePath(self):
        # Get path of accessory files
        base_dir = getBaseDir()
        accessoryFiles_dir = os.path.join(base_dir, '..', 'accessoryFiles')
        # Path to save PID
        self.PIDfilePath = os.path.join(accessoryFiles_dir, f"{self.pidFileName}.pid") 

    def doesPIDfileExist(self):         
        self.PIDfileExists = os.path.exists(self.PIDfilePath)
        if self.PIDfileExists:
            print(f'This PID file exists: {self.PIDfilePath}')
        else:
            print(f'This PID file does not exist: {self.PIDfilePath}')

    def getPID(self):
        if self.PIDfileExists:            
            with open(self.PIDfilePath, "r") as f:
                self.PID = int(f.read().strip())  # Read and parse the PID  
        print(f'The PID file PID is {self.PID}')        

    def createPID(self):
        pid = os.getpid()
        with open(self.PIDfilePath, "w") as f:
            f.write(str(pid))                         
                
    def checkIfPIDisRunning(self):
        if not self.PIDfileExists:              
            self.PIDrunning = False
        else:        
            try:        
                self.PIDrunning = psutil.pid_exists(self.PID)        
            except Exception:
                self.PIDrunning = False
        
        print(f'When checking if PID running, the answer is: {self.PIDrunning}')    
        return self.PIDrunning
    
    def killProgramGracefully(self):
        os.kill(self.PID, signal.SIGTERM)        
        time.sleep(2) # to allow the graceful exit to happen before forcefully exiting

    def killProgramForcefully(self):
        if platform.system() == "Windows":
            # Use taskkill on Windows
            subprocess.run(["taskkill", "/PID", str(self.PID), "/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            # Use SIGKILL on Unix-based systems
            os.kill(self.PID, signal.SIGKILL)        

    def killProgram(self):
        if self.PIDrunning:
            self.killProgramGracefully()
        self.checkIfPIDisRunning()
        if self.PIDrunning: # only if the graceful killing didn't work
            self.killProgramForcefully()

    def cleanUpPID(self):
        if os.path.exists(self.PIDfilePath):
                os.remove(self.PIDfilePath)     

def getBaseDir():
    # Check if the program is running as an executable
    if getattr(sys, 'frozen', False):                
        return os.path.dirname(sys.executable)
    else:        
        return os.path.dirname(os.path.abspath(__file__))
    
def get_exe_path(exeName):    
    # Location of current execetuable
    exe_dir = getBaseDir()    
    # Get OS-specific extension
    system = platform.system()
    if system == 'Windows':
        extension = '.exe'
    else:
        extension = ''  # No extension for macOS/Linux
    # Construct the full path to the executable
    return os.path.join(exe_dir, f'{exeName}{extension}')
        
def getImports_recursive(file_path, visited=None):
    if visited is None:
        visited = set()
    if file_path in visited:
        return [], []
    visited.add(file_path)

    with open(file_path, "r") as file:
        tree = ast.parse(file.read())

    imports = []
    local_files_and_folders = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module
            for alias in node.names:
                imports.append(f"{module}.{alias.name}" if module else alias.name)
                # Handle local module paths
                module_path = module.replace('.', '/')
                if os.path.exists(f"{module_path}.py"):
                    local_files_and_folders.append(f"{module_path}.py")
                elif os.path.isdir(module_path):  # Add directories if they exist
                    local_files_and_folders.append(module_path)

    # Recursively process local files and folders
    for local_path in local_files_and_folders:
        if os.path.exists(local_path):
            sub_imports, sub_datas = getImports_recursive(local_path, visited)
            imports.extend(sub_imports)
            local_files_and_folders.extend(sub_datas)

    return list(set(imports)), list(set(local_files_and_folders))

def setPyQt5path():
    plugin_path = QLibraryInfo.location(QLibraryInfo.PluginsPath)
    os.environ["QT_PLUGIN_PATH"] = plugin_path
    QCoreApplication.setLibraryPaths([plugin_path])
