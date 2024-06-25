# This script will be the basis for the main exe file.
# It will check to see if the program is already running or not, and then bring up the relevant API (Start or Stop program)
# To check, I can use the binary boolean file, and also the psutil library to check to see if an exe file is currently running or not - do both to be sure

from startProgram import startProgram
from stopProgram import stopProgram

# startProgram()

stopProgram()