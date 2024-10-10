import json

class Sizes_addEditWords:
    def __init__(self):
        self.padding_small = None
        self.padding_medium = None
        self.padding_large = None
        self.APIwidth = None
        self.APIheight = None
        self.width_toggle = None

    def defineSizes(self):
        self.padding_small = 5
        self.padding_medium = 10
        self.padding_large = 20
        self.APIwidth = 1400
        self.APIheight = 1000
        self.width_toggle = 22

def addWordToJSONfile(fileName,data,QLineEditText_word,QLineEditText_Def):

    # Get the word and definition from the QLineEdit text lines
    newWord = QLineEditText_word.text()
    newDef = QLineEditText_Def.text()

    # Make the new word/def json entry
    new_entry = {
    "word": newWord,
    "definition": newDef,
    "WOD_shown": False,
    "is_POD": False,
    "POD_shown": False
    }

    # Append new word/def to current word/def json list
    data.append(new_entry)

    # Save new list with new word/def
    with open(fileName, 'w') as file:
        json.dump(data, file, indent=4)         