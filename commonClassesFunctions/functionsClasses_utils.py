import json
import os
import psutil
import signal
import platform
import subprocess
import time
import sys
import ast

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

def get_needed_imports(file_path):
    """
    Identify only the directly needed imports for a given file.
    Returns a set of required imports (modules and symbols).
    """
    with open(file_path, "r") as file:
        tree = ast.parse(file.read())

    # Extract all used names (symbols) in the file
    used_names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    needed_imports = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                # Include only if the module name is used
                if alias.name.split('.')[0] in used_names:
                    needed_imports.add(alias.name)

        elif isinstance(node, ast.ImportFrom):
            module = node.module
            for alias in node.names:
                full_name = f"{module}.{alias.name}" if module else alias.name
                # Include only if the imported name is used
                if alias.name in used_names or (module and module.split('.')[0] in used_names):
                    needed_imports.add(full_name)

    return needed_imports

