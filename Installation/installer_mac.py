import subprocess
import os
from commonClassesFunctions.utils import getBaseDir, getImports_recursive, get_needed_imports
import time
from PyQt5.QtCore import QLibraryInfo
import shutil

class runInstaller_mac():
    def __init__(self):
        # Parameters - exe file names (to be installed)
        self.exeName_userEntryPoint = 'Daily_Word_Definition'
        self.exeName_loadingProgramConsole = 'LoadingProgramConsole'        
        self.exeName_startStopEditProgram = 'StartStopEditProgram' 
        self.exeName_startingProgramConsole = 'StartingProgramConsole'
        self.exeName_WordDefAPI = 'WordDefAPI'
        self.exeName_TimingLoop = 'TimingLoop'
        # Parameters - paths to python files that are being made into executables - paths relative to project folder
        self.pyPath_userEntryPoint = 'DailyWordDefinition.py'
        self.pyPath_loadingProgramConsole = os.path.join('RunProgram','loadingProgram.py')
        self.pyPath_startStopEditProgram = os.path.join('StartStopProgram','main.py')
        self.pyPath_startingProgramConsole = os.path.join('RunProgram','startingProgramConsole.py')
        self.pyPath_WordDefAPI = os.path.join('RunProgram','generateAPI.py')
        self.pyPath_TimingLoop = os.path.join('RunProgram','backgroudTimingLoop.py')
        # Parameters - other
        self.installerPath = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" # inno installer path
        self.vEnvFolder = os.path.expanduser("~/PythonProjects/WordDef/.venv")     
        # Methods
        self.deleteBinAndBuildFolders()
        self.getPathsForExecutables()
        self.createExececutable_userEntryPoint()
        self.createExececutable_loadingProgramConsole()
        #self.createExececutable_startStopEditProgram()
        #self.createExececutable_startingProgramConsole()
        #self.createExececutable_wordDefAPI()
        #self.createExececutable_TimingLoop()
        # self.runInstaller_inno()

    def deleteBinAndBuildFolders(self):
        for folder in ["bin", "build"]:
            if os.path.exists(folder) and os.path.isdir(folder):
                shutil.rmtree(folder)      

    def getPathsForExecutables(self):
        print('\nGetting exe paths')
        time.sleep(1) 
        self.curDir = getBaseDir()
        # bin folder
        self.binFol = os.path.join(self.curDir, '..', 'bin')
        # userEntryPoints exe paths (where from and where to)
        self.pyPathFull_userEntryPoint = os.path.join(self.curDir, '..' , self.pyPath_userEntryPoint) # path of python file to be made into executable
        # loadingProgramConsole exe paths (where from and where to)
        self.pyPathFull_loadingProgramConsole = os.path.join(self.curDir, '..' , self.pyPath_loadingProgramConsole) # path of python file to be made into executable
        # startStopEditProgram exe paths (where from and where to)
        self.pyPathFull_startStopEditProgram = os.path.join(self.curDir, '..' , self.pyPath_startStopEditProgram) # path of python file to be made into executable                 
        # startingProgramConsole exe paths (where from and where to)
        self.pyPathFull_startingProgramConsole = os.path.join(self.curDir, '..' , self.pyPath_startingProgramConsole) # path of python file to be made into executable
        # WordDefAPI exe paths (where from and where to)
        self.pyPathFull_WordDefAPI = os.path.join(os.path.join(self.curDir, '..', self.pyPath_WordDefAPI)) # path of python file to be made into executable
        # TimingLoop exe paths (where from and where to)
        self.pyPathFull_TimingLoop = os.path.join(os.path.join(self.curDir, '..', self.pyPath_TimingLoop)) # path of python file to be made into executable

    def getDependencies_plusExtra(self, file_path):
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
        datas_cmd = [f'--add-data={os.path.join(project_root, folder)}:{folder}' for folder in subfolders]

        # Include Qt plugins
        pyqt5_plugins_path = QLibraryInfo.location(QLibraryInfo.PluginsPath)
        
        if not pyqt5_plugins_path or not os.path.exists(pyqt5_plugins_path):
            raise FileNotFoundError(f"Qt plugins path not found: {pyqt5_plugins_path}")

        datas_cmd.append(f'--add-data={pyqt5_plugins_path}:PyQt5/Qt5/plugins')

        # Dynamic hidden imports from getImports_recursive
        dynamic_hidden_imports, _ = getImports_recursive(file_path)

        # Explicit PyQt5 hidden imports
        explicit_pyqt5_imports = [
            'PyQt5.QtWidgets',
            'PyQt5.QtCore',
            'PyQt5.QtGui',
            'PyQt5.Qt',
            'PyQt5.QtPrintSupport',
        ]

        # Combine dynamic and explicit imports
        hidden_imports_cmd = [f'--hidden-import={dep}' for dep in set(dynamic_hidden_imports).union(explicit_pyqt5_imports)]

        # Debugging output
        print("Datas CMD:", datas_cmd)
        print("\nHidden Imports CMD:", hidden_imports_cmd)

        return datas_cmd + hidden_imports_cmd
    
    def getDependencies(self, file_path):
        dynamic_hidden_imports = get_needed_imports(file_path)
        hidden_imports_list = [f'--hidden-import={dep}' for dep in dynamic_hidden_imports]
        print("Hidden Imports List:", hidden_imports_list)  # Debugging
        time.sleep(1)
        return hidden_imports_list

    def createExececutable_userEntryPoint(self):
        print('\nCreating Daily Word Definition executable')
        time.sleep(1)        
        dependencyArguments = self.getDependencies(self.pyPathFull_userEntryPoint)
        result = subprocess.run([
            "pyinstaller", "--onedir", "--noupx", "--clean", "--windowed",
            "--name", self.exeName_userEntryPoint,
            "--distpath", self.binFol,
            self.pyPathFull_userEntryPoint
        ] + dependencyArguments, capture_output=True, text=True)
        self.printResult(result,self.exeName_userEntryPoint)

    def createExececutable_loadingProgramConsole(self):
        print('\nCreating LoadingProgramConsole executable')
        time.sleep(1)        
        dependencyArguments = self.getDependencies(self.pyPathFull_loadingProgramConsole)
        result = subprocess.run([
            "pyinstaller", "--onedir", "--noupx", "--clean", "--windowed",
            "--name", self.exeName_loadingProgramConsole,
            "--distpath", self.binFol,
            self.pyPathFull_loadingProgramConsole
        ] + dependencyArguments, capture_output=True, text=True)
        self.printResult(result,self.exeName_loadingProgramConsole)

    def createExececutable_startStopEditProgram(self):
        print('\nCreating StartStopEditProgram executable')
        time.sleep(1)        
        dependencyArguments = self.getDependencies_plusExtra(self.pyPathFull_startStopEditProgram)
        result = subprocess.run([
            "pyinstaller", "--onedir", "--noupx", "--clean", "--windowed",
            "--name", self.exeName_startStopEditProgram,
            "--distpath", self.binFol,
            self.pyPathFull_startStopEditProgram
        ] + dependencyArguments, capture_output=True, text=True)
        self.printResult(result,self.exeName_startStopEditProgram)

    def createExececutable_startingProgramConsole(self):
        print('\nCreating startingProgramConsole executable')
        time.sleep(1)        
        dependencyArguments = self.getDependencies(self.pyPathFull_startingProgramConsole)
        result = subprocess.run([
            "pyinstaller", "--onedir", "--noupx", "--clean", "--windowed",
            "--name", self.exeName_startingProgramConsole,
            "--distpath", self.binFol,
            self.pyPathFull_startingProgramConsole
        ] + dependencyArguments, capture_output=True, text=True)
        self.printResult(result,self.exeName_startingProgramConsole)

    def createExececutable_wordDefAPI(self):
        print('\nCreating WordDefAPI executable')
        time.sleep(1)        
        dependencyArguments = self.getDependencies_plusExtra(self.pyPathFull_WordDefAPI)
        result = subprocess.run([
            "pyinstaller", "--onedir", "--noupx", "--clean", "--windowed",
            "--name", self.exeName_WordDefAPI,
            "--distpath", self.binFol,
            self.pyPathFull_WordDefAPI
        ] + dependencyArguments, capture_output=True, text=True)  
        self.printResult(result,self.exeName_WordDefAPI)
                    
    def createExececutable_TimingLoop(self):
        print('\nCreating TimingLoop executable')
        time.sleep(1)        
        dependencyArguments = self.getDependencies(self.pyPathFull_TimingLoop)
        result = subprocess.run([
            "pyinstaller", "--onedir", "--noupx", "--clean", "--windowed",
            "--name", self.exeName_TimingLoop,
            "--distpath", self.binFol,
            self.pyPathFull_TimingLoop
        ] + dependencyArguments, capture_output=True, text=True)
        self.printResult(result,self.exeName_TimingLoop)

    def printResult(self,result,exeName):
        if result.returncode != 0:
            print(f"Error creating {exeName}:")
            print(result.stderr)
        else:
            print(f"{exeName} created successfully.")
        
    def runInstaller_inno(self):
        print('\nRunning inno installer')
        time.sleep(1)            
        # Path to Inno Setup Compiler
        inno_compiler_path = self.installerPath
        # Path to .iss file
        iss_file_path = os.path.join(self.curDir, '..', 'Installation', 'installer_windows_inno.iss')
        print(f"\n\\iss_file_path path: {iss_file_path}\n\n")
        time.sleep(2)            
        subprocess.run([inno_compiler_path, iss_file_path])



def moveStuff():

    # /bin and /bin/_interal paths
    curDir = getBaseDir()
    bin_dir = os.path.join(curDir,'..', 'bin')
    print(f'\nbin path is {bin_dir}')
    time.sleep(2)
    internal_dir = os.path.join(bin_dir,'_internal')
    print(f'\ninternal path is {internal_dir}\n')
    time.sleep(2)

    # Make _internal folder in /bin
    print('Making main _internal...')
    os.makedirs(internal_dir, exist_ok=True)
    time.sleep(2)
    print('done')

    # Loop through all folders in bin/
    for folder in os.listdir(bin_dir):
        folder_path = os.path.join(bin_dir, folder)
        exe_path = os.path.join(folder_path, folder)
        internalInternalFolder = os.path.join(bin_dir,folder,'_internal')

        if folder_path == internal_dir:
            continue

        # Delete any .app folders
        if folder.endswith(".app") and os.path.isdir(folder_path):
            print(f'\nRemoving this .app file {folder_path}...')
            time.sleep(2)
            shutil.rmtree(folder_path)
            print('done')
            continue

        if os.path.isdir(folder_path):    
            os.rename(folder_path, folder_path + "_temp")
            folder_path += "_temp"
            print(f'\nNew temp folder: {folder_path}')
            time.sleep(5)

        # Move the executable to the bin folder
        if os.path.exists(exe_path) and os.path.isfile(exe_path):
            print(f'\nMoving this executable {exe_path} to \bin...')
            time.sleep(2)
            shutil.move(exe_path, bin_dir)
            print('done')

        # Move all executable internal files into /bin/_internal
        if os.path.isdir(internalInternalFolder):
            print(f'\nMoving internal files to main _internal for {folder}...')
            time.sleep(2)
            for file in os.listdir(internalInternalFolder):
                shutil.move(os.path.join(internalInternalFolder, file), internal_dir)
            print('done')

        # Now remove the remainder of the executable folder
        if os.path.isdir(folder_path):
            print(f'\nDeleting this folder: {folder_path}...')
            shutil.rmtree(folder_path)






if __name__ == "__main__":
    runInstaller_mac()
    moveStuff()
    