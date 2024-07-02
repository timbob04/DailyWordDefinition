
# Intial
# Functions for:
# 1) Getting the words and finding the right one - class, with methods getWOD and getROD
# 2) Making the API
# 3) Collecting any user input and adjusting the word/definition/code list

import os
import json

from PresentWordsAndDefinitions_functionsClasses import readJSONfile, WODandDef, RODandDef 

def main():
    
    # Get path of accessory files
    base_dir = os.path.dirname(os.path.abspath(__file__))
    accessoryFiles_dir = os.path.join(base_dir, '..', 'accessoryFiles')
    # Write time to run program to .txt file
    curFilePath = os.path.join(accessoryFiles_dir, 'WordsDefsCodes.json')

    # Read WordsDefsCodes.json
    data = readJSONfile(curFilePath)

    # Get WOD and its definition (and update JSON file accordingly)
    curWODandDef = WODandDef(data, curFilePath)
    WOD, WOD_definition = curWODandDef.getAndreturnWOD()

    # Get ROD and its definition (and update JSON file accordingly)
    curRODandDef = RODandDef(data, curFilePath)
    ROD, ROD_definition = curRODandDef.getAndreturnROD()
 
    # print(f"WOD is: {WOD}.  Def is: {WOD_definition}")
    # print(f"Rod is: {ROD}.  Def is: {ROD_definition}")


main()    