
# Intial
# Functions for:
# 1) Getting the words and finding the right one - class, with methods getWOD and getROD
# 2) Making the API
# 3) Collecting any user input and adjusting the word/definition/code list

import os
import json

def firstFalse_WOD_shown(data):
    for index, word in enumerate(data):
        if not word['WOD_shown']:
            return index
    return None  

def main():
    
    # Get path of accessory files
    base_dir = os.path.dirname(os.path.abspath(__file__))
    accessoryFiles_dir = os.path.join(base_dir, '..', 'accessoryFiles')
    # Write time to run program to .txt file
    curFilePath = os.path.join(accessoryFiles_dir, 'WordsDefsCodes.json')

    # Read WordsDefsCodes.json
    with open(curFilePath, 'r') as file:
        data = json.load(file)

    # Check to see if the entire list of words has been presented (for this round)
    allWordsPrevShown = all(word['WOD_shown'] for word in data)

    # Get WOD and update word list accordingly
    if (allWordsPrevShown):
        for word in data[1:]: # change all 'WOD_shown' to false, except the first
            word['WOD_shown'] = False
        pos = 0    
    else:
        pos = firstFalse_WOD_shown(data)
        data[pos]['WOD_shown'] = True



    WOD = data[pos]['word']
    definition = data[pos]['definition']

    
    print(f"{WOD}: {definition}")


    with open(curFilePath, 'w') as file:
        json.dump(data, file, indent=4)     

    print()   

    




main()    