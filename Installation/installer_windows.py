import subprocess
import os
import time

class runInstaller_windows():
    def __init__(self):
        # Parameters
        self.exeName_runProgram = 'Background' # name of installed exe file for background (runProgram) stuff
        self.exeName_userInput = 'UserInput' # name of installed exe file for the user input stuff (start/stop/edit program, etc)
        self.dependencyFolders = ['addEditWords', 'RunProgram', 'commonClassesFunctions', 'StartStopProgram'] # name of all main folders in project, where functions/classes are grabbed from
        # Methods
        self.getPathsForExecutables()
        self.getDependencyFolderPaths()
        self.createSubprocessArgsForDependencies()
        self.getDependencies()
        self.createExececutable_userIput()
        self.createExcecutable_runProgram()
        self.runInstaller_inno()

    def getPathsForExecutables(self):
        self.curDir = os.path.dirname(os.path.abspath(__file__))
        # User input executable paths
        self.dir_userInput = os.path.join(self.curDir, '..', 'StartStopProgram','startStopProgram_main.py') # path of python file to be made into executable
        self.dir_executable_userInput = os.path.join(self.curDir, '..', 'dist') # path for excecutable
        # Program running executable paths
        self.dir_runProgram = os.path.join(self.curDir, '..', 'RunProgram','runProgram_main.py') # path of python file to be made into executable
        self.dir_executable_runProgram = os.path.join(self.curDir, '..', 'dist') # path for excecutable        

    def getDependencyFolderPaths(self):        
        self.dependencyFolderPaths = [os.path.join(self.curDir, '..', folder) for folder in self.dependencyFolders] # list comprehension        

    def createSubprocessArgsForDependencies(self):
        self.addDependenciesArgs = " ".join(
            [f'--add-data "{path};{os.path.basename(path)}"' for path in self.dependencyFolderPaths]
        )

    def getDependencies(self):
        # List of dynamic dependencies to collect
        dependencies = ['PyQt5', 'psutil', 'win32com.client', 'platform', 'json', 'os', 'time', 'datetime', 're', 'subprocess']        
        # Generate --collect-all arguments dynamically
        self.dependencyArgs =  " ".join([f'--collect-all {dep}' for dep in dependencies])    

    def createExececutable_userIput(self):                                
        subprocess.run(
            f'pyinstaller --onedir {self.addDependenciesArgs} '
            f'{self.dependencyArgs} '
            f'--debug=imports '  # Debugging mode to analyze missing dependencies
            f'"{self.dir_userInput}" --distpath "{self.dir_executable_userInput}" '
            f'--name "{self.exeName_userInput}"',
                shell=True
            )
        
    def createExcecutable_runProgram(self):        
        subprocess.run(
            f'pyinstaller --onedir {self.addDependenciesArgs} '        
            f'{self.dependencyArgs} '
            f'--debug=imports '  # Debugging mode to analyze missing dependencies    
            f'"{self.dir_runProgram}" --distpath "{self.dir_executable_runProgram}" '
            f'--name "{self.exeName_runProgram}"',
            shell=True
        )
        
    def runInstaller_inno(self):
        # Path to Inno Setup Compiler
        inno_compiler_path = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" # or path of inno installer program
        # Path to .iss file
        iss_file_path = os.path.join(self.curDir,"installer_windows_inno.iss")
        subprocess.run([inno_compiler_path, iss_file_path])

if __name__ == "__main__":
    runInstaller_windows()