import subprocess
import os

class runInstaller_windows():
    def __init__(self):
        # Parameters
        self.exeName_runProgram = 'Background'
        self.exeName_userInput = 'UserInput'
        # Methods
        self.getPaths()
        self.createExcecutable_userIput()
        self.createExcecutable_runProgram()
        self.runInstaller_inno()

    def getPaths(self):
        self.curDir = os.path.dirname(os.path.abspath(__file__))
        # User input executable paths
        self.dir_userInput = os.path.join(self.curDir, '..', 'StartStopProgram','startStopProgram_main.py') # path of python file to be made into executable
        self.dir_executable_userInput = os.path.join(self.curDir, '..', 'dist') # path for excecutable
        # Program running executable paths
        self.dir_runProgram = os.path.join(self.curDir, '..', 'RunProgram','runProgram.py') # path of python file to be made into executable
        self.dir_executable_runProgram = os.path.join(self.curDir, '..', 'dist') # path for excecutable

    def createExcecutable_userIput(self):        
        subprocess.run(
            f'pyinstaller --onefile "{self.dir_userInput}" --distpath "{self.dir_executable_userInput}" --name "{self.exeName_userInput}"',
            shell=True
        )

    def createExcecutable_runProgram(self):        
        subprocess.run(
            f'pyinstaller --onefile "{self.dir_runProgram}" --distpath "{self.dir_executable_runProgram}" --name "{self.exeName_runProgram}"',
            shell=True
        )    

    def runInstaller_inno(self):
        # Path to Inno Setup Compiler
        inno_compiler_path = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" # or path of inno installer program
        # Path to .iss file
        iss_file_path = os.path.join(self.curDir,"appInstaller_inno.iss")
        subprocess.run([inno_compiler_path, iss_file_path])


if __name__ == "__main__":
    runInstaller_windows()