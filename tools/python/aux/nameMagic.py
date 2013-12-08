# This Python file uses the following encoding: utf-8

import os
import sys
sys.path.append('..')
from dictUtils import MyDict
from unicodeMagic import UnicodeReader
from unidecode import unidecode
from nameMap import nameMap


dataPath = os.path.abspath("../../../data")


# This is the list of DBLP author names (>1.1M people)
# 335078;M. G. J. van den Brand, Mark G. J. van den Brand, Mark van den Brand
f = open(os.path.join(dataPath, "dblp-author-aliases-stripped.csv"), "rb")
reader1 = UnicodeReader(f)

# Read the list into a map
# reverseLookup['M. G. J. van den Brand'] 
#     = reverseLookup['Mark G. J. van den Brand'] 
#     = reverseLookup['Mark van den Brand']
#     = 335078
reverseLookup = MyDict()
# Choose a unique spelling for each name
# directLookup['M. G. J. van den Brand'] 
#     = directLookup['Mark G. J. van den Brand'] 
#     = directLookup['Mark van den Brand']
#     = 'Mark van den Brand'
directLookup = MyDict()
for row in reader1:
    aid = int(row[0])
    aliases = [name.strip() for name in row[1].split(',')]
    for name in aliases:
        reverseLookup[name] = aid
    directLookup[aid] = aliases[-1]


# Normalizes a name using the different aliases 
# used by the same person on DBLP
def normaliseName(name):
    # Strip out accents and other unicode
    name = unidecode(name).strip()
    
    try:
        name = nameMap[name]
    except:
        pass
    
    # If on DBLP, use consistent name
    try:
        aid = reverseLookup[name]
        name = directLookup[aid]
    except:
        pass

    # Do the trick one more time to ensure
    # the previous step did not switch the name
    # (see 1005156;John C. Grundy, John Grundy)    
    try:
        name = nameMap[name]
    except:
        pass

    return name

