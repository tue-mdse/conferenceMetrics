# This Python file uses the following encoding: utf-8

import os
import sys
sys.path.append('..')
# from folderUtils import MyFolder
from dictUtils import MyDict
from unicodeMagic import UnicodeReader, UnicodeWriter
from unidecode import unidecode
from nameMap import nameMap
from nameMagic import normaliseName, directLookup, reverseLookup


dataPath = os.path.abspath("../../../data")


conferences = ['icse', 'icsm', 'wcre', 'csmr', 'msr', 'gpce', 'fase', 'icpc', 'fse', 'scam', 'ase']
# conferences = ['msr']
# conferences = sys.argv[1:]

for conference in conferences:
    
    print conference
    
    f = open(os.path.join(dataPath, 'bht2csv', '%s_papers.csv' % conference), 'rb')
    reader = UnicodeReader(f)
    
    g = open(os.path.join(dataPath, 'normalised-papers', '%s.csv' % conference), 'wb')
    writer = UnicodeWriter(g)


    for row in reader:
        year = row[0]
        authors = []
        for name in row[1].split(','):
            cleanName = normaliseName(name)
            if len(cleanName):
                authors.append(cleanName)
        authors = ','.join(authors)
        writer.writerow([year, authors] + row[2:])

    g.close()
