import time
from RunProgram.runProgram_timingControl import TimingControl
from commonClassesFunctions.functionsClasses_utils import PID, get_exe_path
import subprocess

class RunExe():
    def __init__(self, exeFilePath, dep):
        # parameters
        self.exeFilePath = exeFilePath
        self.dep = dep # class dependencies
        # Methods
        self.getOS()
        self.console_YN = self.Console_YN(dep)       
        self.runExe()
           
    def getOS(self):
        self.curOS = self.dep.platform.system()        

    class Console_YN():
        def __init__(self,dep):
            # parameters
            self.dep = dep
            self.openConsole_YN = False                           
            # Methods
            self.getPath()
            self.loadDataFromPath()
            self.isDataTrueOrFalse()

        def getPath(self):
            # Get path of accessory files
            base_dir = self.dep.getBaseDir()
            accessoryFiles_dir = self.dep.os.path.join(base_dir, '..', 'accessoryFiles')
            # Path to save PID
            self.filePath = self.dep.os.path.join(accessoryFiles_dir, "openConsoleForExe_YN.txt") 
    
        def loadDataFromPath(self):
            self.data = 0
            if self.dep.os.path.exists(self.filePath):            
                with open(self.filePath, "r") as f:
                    self.data = int(f.read().strip())

        def isDataTrueOrFalse(self):
            if self.data == 1:
                self.openConsole_YN = True
                
    def runExe(self):        
        if self.curOS == 'Windows':
            if self.console_YN.openConsole_YN:
                self.dep.subprocess.Popen([self.exeFilePath], creationflags=self.dep.subprocess.CREATE_NEW_CONSOLE)                
            else:
                self.dep.subprocess.Popen([self.exeFilePath], creationflags=self.dep.subprocess.DETACHED_PROCESS)
        elif self.curOS == 'Darwin':
            if self.console_YN.openConsole_YN:
                self.dep.subprocess.Popen(["open", "-a", "Terminal", self.exeFilePath])
            else:
                self.dep.subprocess.Popen([self.exeFilePath], preexec_fn=self.dep.os.setsid)
        elif self.curOS == 'Linux':
            if self.console_YN.openConsole_YN:
                self.dep.subprocess.Popen(["gnome-terminal", "--", self.exeFilePath])
            else:
                self.dep.subprocess.Popen([self.exeFilePath], preexec_fn=self.dep.os.setsid)                


def runApplicationTimingLoop():

    print('\nTimingLoop.exe running')

    # For checking when the API should be presented
    timingControl = TimingControl()
    
    # Make PID to indicate that this code's timing loop is running
    pid_time = PID("TimingLoop")
    pid_time.createPID()
    print("\nCreating PID for TimingLoop.exe (this exe).")
    time.sleep(1)
        
    while True:  
        print('Timing loop looping ...')                  
        if timingControl.checkIfTimeToRunProgram():            
            print('\nTime reached to run WordDefAPI')     
            time.sleep(1)
            # Close any previous instances of main API to show words/definitions
            pid_wordDefAPI = PID("WordDefAPI")
            print("\nChecking if a previou instance of WordDefAPI.exe is runnnig using its PID.")                         
            if pid_wordDefAPI.checkIfPIDisRunning():
                print("\nKilling previous instances on WordDefAPI.exe")
                time.sleep(1)
                pid_wordDefAPI.killProgram()
            # Make API to show today's word and definition
            exeFilePath = get_exe_path('WordDefAPI')
            print(f'\nRunning this exe using subprocess now:{exeFilePath}\n')
            time.sleep(1)
            subprocess.Popen([exeFilePath], creationflags=subprocess.CREATE_NEW_CONSOLE)
            # subprocess.Popen([exeFilePath], creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_CONSOLE)
            # getAndMakeAPIcontent()         
        time.sleep(5)

# Run the main function if this script is executed directly
if __name__ == "__main__":    
    runApplicationTimingLoop()