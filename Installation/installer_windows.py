import subprocess
import os
from commonClassesFunctions.functionsClasses import getBaseDir, getImports_recursive
import time

class runInstaller_windows():
    def __init__(self):
        # Parameters - exe file names (to be installed)
        self.exeName_DailyWordDefinition = 'DailyWordDefinition' 
        self.exeName_WordDefAPI = 'WordDefAPI'
        self.exeName_TimingLoop = 'TimingLoop'
        # Parameters - paths to python files relative to project folder - files that are being made into exe files
        self.pyPath_DailyWordDefinition = 'DailyWordDefinition.py'
        self.pyPath_WordDefAPI = os.path.join('RunProgram','runProgram_generateAPI.py')
        self.pyPath_TimingLoop = os.path.join('RunProgram','runProgram_timingLoop.py')
        # Parameters - other
        self.installerPath = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" # inno installer path
        # Methods
        self.getPathsForExecutables()
        self.createExececutable_wordDef()
        self.createExececutable_wordDefAPI()
        self.createExececutable_TimingLoop()
        self.runInstaller_inno()

    def getPathsForExecutables(self):
        print('\n\nGetting exe path\n\n')
        time.sleep(1) 
        self.curDir = getBaseDir()
        # DailyWordDefinition exe paths (where from and where to)
        self.pyPathFull_DailyWordDefinition = os.path.join(self.curDir, '..',self.pyPath_DailyWordDefinition) # path of python file to be made into executable
        self.exePath_DailyWordDefinition = os.path.join(self.curDir, '..', 'bin') # path for excecutable
        # WordDefAPI exe paths (where from and where to)
        self.pyPathFull_WordDefAPI = os.path.join(os.path.join(self.curDir, '..', self.pyPath_WordDefAPI)) # path of python file to be made into executable
        self.exePath_WordDefAPI = os.path.join(self.curDir, '..', 'bin') # path for excecutable        
        # TimingLoop exe paths (where from and where to)
        self.pyPathFull_TimingLoop = os.path.join(os.path.join(self.curDir, '..', self.pyPath_TimingLoop)) # path of python file to be made into executable
        self.exePath_TimingLoop = os.path.join(self.curDir, '..', 'bin') # path for excecutable        

    def getDependencies(self, file_path):
        # List of dynamic dependencies to collect
        dependencies = getImports_recursive(file_path)
        # Generate --collect-all arguments dynamically
        return " ".join([f'--hidden-import {dep}' for dep in dependencies])    

    def createExececutable_wordDef(self):
        print('\n\nCreating DailyWordDefinition.exe\n\n')
        time.sleep(1)        
        dependencyArguments = self.getDependencies(self.pyPathFull_DailyWordDefinition)
        subprocess.run(
            f'pyinstaller --onefile --noconsole '
            f'{dependencyArguments} '
            # f'--debug=imports '  # Debugging mode to analyze missing dependencies
            f'"{self.pyPathFull_DailyWordDefinition}" --distpath "{self.exePath_DailyWordDefinition}" '
            f'--name "{self.exeName_DailyWordDefinition}"',
                shell=True
            )

    def createExececutable_wordDefAPI(self):
        print('\n\nCreating WordDefAPI.exe\n\n')
        time.sleep(1)        
        dependencyArguments = self.getDependencies(self.pyPathFull_WordDefAPI)
        subprocess.run(
            f'pyinstaller --onefile --noconsole '
            f'{dependencyArguments} '
            # f'--debug=imports '  # Debugging mode to analyze missing dependencies
            f'"{self.pyPathFull_WordDefAPI}" --distpath "{self.exePath_WordDefAPI}" '
            f'--name "{self.exeName_WordDefAPI}"',
                shell=True
            )    
        
    def createExececutable_TimingLoop(self):
        print('\n\nCreating TimingLoop.exe\n\n')
        time.sleep(1)        
        dependencyArguments = self.getDependencies(self.pyPathFull_TimingLoop)
        subprocess.run(
            f'pyinstaller --onefile --noconsole '
            f'{dependencyArguments} '
            # f'--debug=imports '  # Debugging mode to analyze missing dependencies
            f'"{self.pyPathFull_TimingLoop}" --distpath "{self.exePath_TimingLoop}" '
            f'--name "{self.exeName_TimingLoop}"',
                shell=True
            )    
        
    def runInstaller_inno(self):
        print('\n\nRunning inno installer\n\n')
        time.sleep(1)            
        # Path to Inno Setup Compiler
        inno_compiler_path = self.installerPath
        # Path to .iss file
        iss_file_path = os.path.join(self.curDir, '..', 'Installation', 'installer_windows_inno.iss')
        print(f"\n\iss_file_path path: {iss_file_path}\n\n")
        time.sleep(2)            
        subprocess.run([inno_compiler_path, iss_file_path])

if __name__ == "__main__":
    runInstaller_windows()