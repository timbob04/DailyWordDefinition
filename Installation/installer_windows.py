import subprocess
import os
from commonClassesFunctions.functionsClasses import getBaseDir, getImports_recursive
import time

class runInstaller_windows():
    def __init__(self):
        # Parameters - exe file names (to be installed)
        self.exeName_userEntryPoint = 'Daily_Word_Definition'
        self.exeName_startStopEditProgram = 'StartStopEditProgram' 
        self.exeName_WordDefAPI = 'WordDefAPI'
        self.exeName_TimingLoop = 'TimingLoop'
        # Parameters - paths to python files relative to project folder - files that are being made into exe files
        self.pyPath_userEntryPoint = 'DailyWordDefinition.py'
        self.pyPath_startStopEditProgram = os.path.join('StartStopProgram','startStopProgram_main.py')
        self.pyPath_WordDefAPI = os.path.join('RunProgram','runProgram_generateAPI.py')
        self.pyPath_TimingLoop = os.path.join('RunProgram','runProgram_timingLoop.py')
        # Parameters - other
        self.installerPath = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" # inno installer path
        self.vEnvFolder = r"C:\Users\timot\PythonProjects\WordDef\venv"
        # Methods
        self.getPathsForExecutables()
        self.createExececutable_userEntryPoint()
        self.createExececutable_startStopEditProgram()
        self.createExececutable_wordDefAPI()
        self.createExececutable_TimingLoop()
        self.runInstaller_inno()

    def getPathsForExecutables(self):
        print('\n\nGetting exe paths\n\n')
        time.sleep(1) 
        self.curDir = getBaseDir()
        # userEntryPoints exe paths (where from and where to)
        self.pyPathFull_userEntryPoint = os.path.join(self.curDir, '..' , self.pyPath_userEntryPoint) # path of python file to be made into executable
        self.exePath_userEntryPoint = os.path.join(self.curDir, '..', 'bin') # path for excecutable
        # startStopEditProgram exe paths (where from and where to)
        self.pyPathFull_startStopEditProgram = os.path.join(self.curDir, '..' , self.pyPath_startStopEditProgram) # path of python file to be made into executable
        self.exePath_startStopEditProgram = os.path.join(self.curDir, '..', 'bin') # path for excecutable                     
        # WordDefAPI exe paths (where from and where to)
        self.pyPathFull_WordDefAPI = os.path.join(os.path.join(self.curDir, '..', self.pyPath_WordDefAPI)) # path of python file to be made into executable
        self.exePath_WordDefAPI = os.path.join(self.curDir, '..', 'bin') # path for excecutable        
        # TimingLoop exe paths (where from and where to)
        self.pyPathFull_TimingLoop = os.path.join(os.path.join(self.curDir, '..', self.pyPath_TimingLoop)) # path of python file to be made into executable
        self.exePath_TimingLoop = os.path.join(self.curDir, '..', 'bin') # path for excecutable        

    def getDependencies(self, file_path):
        # List of specific subfolders to include
        subfolders = [
            "StartStopProgram",
            "RunProgram",
            "commonClassesFunctions",
            "addEditWords",
        ]

        # Get the project root
        project_root = os.path.abspath(os.path.join(getBaseDir(), ".."))

        # Add each subfolder
        datas_cmd = " ".join([f'--add-data="{os.path.join(project_root, folder)}:{folder}"' for folder in subfolders])

        # Include Qt plugins
        pyqt5_plugins_path = os.path.join(self.vEnvFolder, "Lib", "site-packages", "PyQt5", "Qt5", "plugins")
        if not os.path.exists(pyqt5_plugins_path):
            raise FileNotFoundError(f"Qt plugins path not found: {pyqt5_plugins_path}")
        datas_cmd += f' --add-data="{pyqt5_plugins_path}:PyQt5/Qt/plugins"'

        # Dynamic hidden imports from getImports_recursive
        dynamic_hidden_imports, _ = getImports_recursive(file_path)

        # Explicit PyQt5 hidden imports
        explicit_pyqt5_imports = [
            'PyQt5.QtWidgets',
            'PyQt5.QtCore',
            'PyQt5.QtGui',
            'PyQt5.Qt',
            'PyQt5.QtPrintSupport',
            'win32com',
            'win32com.client',
        ]

        # Combine dynamic and explicit imports
        hidden_imports = set(dynamic_hidden_imports).union(explicit_pyqt5_imports)
        hidden_imports_cmd = " ".join([f'--hidden-import={dep}' for dep in hidden_imports])

        # Debugging output
        print("Datas CMD:", datas_cmd)
        print("Hidden Imports CMD:", hidden_imports_cmd)

        return f"{hidden_imports_cmd} {datas_cmd}"

    def createExececutable_userEntryPoint(self):
        print('\n\nCreating Daily Word Definition.exe\n\n')
        time.sleep(1)        
        dependencyArguments = self.getDependencies(self.pyPathFull_userEntryPoint)
        result = subprocess.run(
            f'pyinstaller --onefile --noupx --clean --console '
            f'{dependencyArguments} '
            # f'--debug=imports '  # Debugging mode to analyze missing dependencies
            f'"{self.pyPathFull_userEntryPoint}" --distpath "{self.exePath_userEntryPoint}" '
            f'--name "{self.exeName_userEntryPoint}"',
                shell=True,
                capture_output=True,
                text=True
            )
        self.printResult(result,self.exeName_userEntryPoint)

    def createExececutable_startStopEditProgram(self):
        print('\n\nCreating StartStopEditProgram.exe\n\n')
        time.sleep(1)        
        dependencyArguments = self.getDependencies(self.pyPathFull_startStopEditProgram)
        result = subprocess.run(
            f'pyinstaller --onefile --noupx --clean --console '
            f'{dependencyArguments} '
            # f'--debug=imports '  # Debugging mode to analyze missing dependencies
            f'"{self.pyPathFull_startStopEditProgram}" --distpath "{self.exePath_startStopEditProgram}" '
            f'--name "{self.exeName_startStopEditProgram}"',
                shell=True,
                capture_output=True,
                text=True
            )
        self.printResult(result,self.exeName_startStopEditProgram)


    def createExececutable_wordDefAPI(self):
        print('\n\nCreating WordDefAPI.exe\n\n')
        time.sleep(1)        
        dependencyArguments = self.getDependencies(self.pyPathFull_WordDefAPI)
        result = subprocess.run(
            #f'pyinstaller --onefile --noconsole '
            f'pyinstaller --onefile --noupx --clean --console '
            f'{dependencyArguments} '
            # f'--debug=imports '  # Debugging mode to analyze missing dependencies
            f'"{self.pyPathFull_WordDefAPI}" --distpath "{self.exePath_WordDefAPI}" '
            f'--name "{self.exeName_WordDefAPI}"',
                shell=True,
                capture_output=True,
                text=True
            )    
        self.printResult(result,self.exeName_WordDefAPI)
                    
    def createExececutable_TimingLoop(self):
        print('\n\nCreating TimingLoop.exe\n\n')
        time.sleep(1)        
        dependencyArguments = self.getDependencies(self.pyPathFull_TimingLoop)
        result = subprocess.run(
            f'pyinstaller --onefile --noupx --clean --console '
            f'{dependencyArguments} '
            # f'--debug=imports '  # Debugging mode to analyze missing dependencies
            f'"{self.pyPathFull_TimingLoop}" --distpath "{self.exePath_TimingLoop}" '
            f'--name "{self.exeName_TimingLoop}"',
                shell=True,
                capture_output=True,
                text=True
            )   
        self.printResult(result,self.exeName_TimingLoop)

    def printResult(self,result,exeName):
        if result.returncode != 0:
            print(f"Error creating {exeName}:")
            print(result.stderr)
        else:
            print(f"{exeName} created successfully.")

        
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