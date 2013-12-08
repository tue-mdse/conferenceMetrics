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


for conference in conferences:
    g = open(os.path.join(dataPath, 'normalised-pc', '%s.csv' % conference), 'wb')
    writer = UnicodeWriter(g)

    f1 = open(os.path.join(dataPath, 'pc', '%s.csv' % conference), 'rb')
    reader1 = UnicodeReader(f1)    
    for row in reader1:
        year = row[0]
        track = row[1]
        if track == 'main':
            pc = ','.join([normaliseName(name) for name in row[2].split(',') if len(normaliseName(name))])
            writer.writerow([year, track, pc])
    g.close()

exit()

#conferences = ['ase']

allAuthorsSet = set()

for conference in conferences:
    f1 = open(os.path.join(dataPath, 'bht2csv', '%s_papers.csv' % conference), 'rb')
    reader1 = UnicodeReader(f1)    
    for row in reader1:
        allAuthorsSet.update([normaliseName(name) for name in row[1].split(',') if len(normaliseName(name))])


for conference in conferences:
    print conference.upper()
    authorsSet = set()

    # All papers
    f1 = open(os.path.join(dataPath, 'bht2csv', '%s_papers.csv' % conference), 'rb')
    reader1 = UnicodeReader(f1)
    
    for row in reader1:
        year = int(row[0])
        authorsSet.update([normaliseName(name) for name in row[1].split(',') if len(normaliseName(name))])
        
    # PC members
    f2 = open(os.path.join(dataPath, 'pc', '%s.csv' % conference), 'rb')
    reader2 = UnicodeReader(f2)
    
    pcSet = set()
    
    for row in reader2:
        year = int(row[0])
        track = row[1]
        name = normaliseName(row[2])
        if len(name) and track=='main':
            pcSet.add(name)
            
    print len(pcSet.difference(authorsSet)), 'unresolved out of', len(pcSet)
    
    suggestions = set()
    
    autho = authorsSet
#    autho = allAuthorsSet
    
    for pcName in sorted(pcSet.difference(autho)):
#        print pcName
        candidates = []
        s1 = set([p.lower() for p in pcName.split() if p.find('.')==-1])
        for author in sorted(autho):
            s2 = set([p.lower() for p in author.split() if p.find('.')==-1])
            if s1 == s2:
                candidates.append(author)
#                print '\t', author
        if len(candidates) == 1:
            suggestions.add((pcName, candidates[0]))
        else:
            try:
                aid = reverseLookup[pcName]
                name = directLookup[aid]
            except:
                print pcName, candidates     
#                pass
        
    print
    for (a,b) in sorted(suggestions):
        print '\t\'%s\':\'%s\',' % (a, b)


