# This Python file uses the following encoding: utf-8

import os
import sys
sys.path.append('..')
# from folderUtils import MyFolder
from dictUtils import MyDict
from unicodeMagic import UnicodeReader, UnicodeWriter
from unidecode import unidecode
from nameMap import nameMap


dataPath = os.path.abspath("../../../data")


# This is the list of DBLP author names (>1.1M people)
# 335078;M. G. J. van den Brand, Mark G. J. van den Brand, Mark van den Brand
f = open(os.path.join(dataPath, "dblp-author-aliases-stripped.csv"), "rb")
reader1 = UnicodeReader(f)

# Read the list into a map
# reverseLookup['M. G. J. van den Brand'] 
# 	= reverseLookup['Mark G. J. van den Brand'] 
# 	= reverseLookup['Mark van den Brand']
# 	= 335078
reverseLookup = MyDict()
# Choose a unique spelling for each name
# directLookup['M. G. J. van den Brand'] 
# 	= directLookup['Mark G. J. van den Brand'] 
# 	= directLookup['Mark van den Brand']
# 	= 'Mark van den Brand'
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
    	unknowns.add(name)
#         pass
    
    return name



# conferences = ['icse', 'icsm', 'wcre', 'csmr', 'msr', 'gpce', 'fase', 'icpc', 'fse', 'scam', 'ase']
# conferences = ['msr']
conferences = sys.argv[1:]


unknowns = set()

for conference in conferences:
    g = open(os.path.join(dataPath, 'bht2csv', '%s_papers_2013n.csv' % conference), 'wb')
    writer = UnicodeWriter(g)

    f1 = open(os.path.join(dataPath, 'bht2csv', '%s_papers_2013.csv' % conference), 'rb')
    reader1 = UnicodeReader(f1)    
    for row in reader1:
        year = row[0]
        authors = ','.join([normaliseName(name) for name in row[1].split(',') if len(normaliseName(name))])
        title = row[2]
        writer.writerow([year, authors, title, '', '', '', ''])
    g.close()

print
soFarSoGood = set()

# "Paulo R. F. Cunha": "Paulo Cunha"
# "Neil Maiden": "Neil A. M. Maiden"
# Strip middle initials, exact match on all other name parts
uselessData = MyDict()
# for each name in the DBLP data
for key in reverseLookup.keys():
	# record a version of the name without initials
    s = " ".join([p.lower() for p in key.split() if len(p) > 1 and p.find('.') == -1])
    uselessData[key] = s

# then for each of the unknowns
for name in sorted(unknowns):
    longParts = [p.lower() for p in name.split() if len(p) > 1 and p.find('.') == -1]
    # if the name contains at least two parts of sufficient length
    if len(longParts) > 1:
    	# check against each of the DBLP names
        for key in reverseLookup.keys():
        	# retrieve the version without initials
            s = uselessData[key]
            # check that the name starts and ends with the same parts
            if s.startswith(longParts[0]) and s.endswith(" %s" % longParts[-1]):
                # writer.writerow([name, key])
                # print name, key
                print "\'%s\':\'%s\'," % (name, key)
#                 writer.writerow(["\'%s\':\'%s\'," % (name, key)])
                
                # record that this is a name for which at least one match exists on DBLP
                soFarSoGood.add(name)
#            s = set([p.lower() for p in key.split() if len(p) > 1 and p.find('.') == -1])
#            if len(s) > 1:
#                if not len(s.symmetric_difference(longParts)):
#                    writer.writerow([name, key])
#                    soFarSoGood.add(name)

# remove the names for which matches have been found from the unknown set
unknowns.difference_update(soFarSoGood)


# for each of the remaining unknowns check if it is of the form 
# 'J. McHugh' ('John McHugh') - common especially for older editions
for name in sorted(unknowns):
	# split into parts
    parts2 = [p.lower() for p in name.split() if len(p)]
    parts = []
    # strip dots
    for part in parts2:
        parts += [p for p in part.split('.') if len(p)]
    
    # if exactly two parts
    if len(parts) == 2:
    	# if the first part is a letter
        if len(parts[0]) == 1:
            initial = parts[0][0]
            lastName = parts[1]
            # look for names starting with that initial and having the same last name
            for key in reverseLookup.keys():
                if key.lower().startswith(initial) and key.lower().endswith(" %s" % lastName):
                    # writer.writerow([name, key])
                    # print name, key
                    print "\'%s\':\'%s\'," % (name, key)
#                     writer.writerow(["\'%s\':\'%s\'," % (name, key)])
                    soFarSoGood.add(name)

# g.close()

# Update the unknown set again
unknowns.difference_update(soFarSoGood)

print
print 'Still unknown in the DBLP data set:'
for name in sorted(unknowns):
    print name
print

# Try more heuristics (with less confidence than before)
for name in sorted(unknowns):
	# split into name parts of length at least two and ignore parts containing dot
    longParts = set([p for p in name.split() if len(p) > 1 and p.find('.') == -1])
    # if there are at least two parts
    if len(longParts) > 1:
    	# match against DBLP names containing the same name parts, 
    	# potentially in a different order
        for key in reverseLookup.keys():
            s = set([p for p in key.split() if len(p) > 1 and p.find('.') == -1])
            if len(s) > 1:
                if not len(s.symmetric_difference(longParts)):
                    print "\'%s\':\'%s\'," % (name, key)


# exit()
# 
# #conferences = ['ase']
# 
# allAuthorsSet = set()
# 
# for conference in conferences:
#     f1 = open(os.path.join(dataPath, 'bht2csv', '%s_papers.csv' % conference), 'rb')
#     reader1 = UnicodeReader(f1)    
#     for row in reader1:
#         allAuthorsSet.update([normaliseName(name) for name in row[1].split(',') if len(normaliseName(name))])
# 
# 
# for conference in conferences:
#     print conference.upper()
#     authorsSet = set()
# 
#     # All papers
#     f1 = open(os.path.join(dataPath, 'bht2csv', '%s_papers.csv' % conference), 'rb')
#     reader1 = UnicodeReader(f1)
#     
#     for row in reader1:
#         year = int(row[0])
#         authorsSet.update([normaliseName(name) for name in row[1].split(',') if len(normaliseName(name))])
#         
#     # PC members
#     f2 = open(os.path.join(dataPath, 'pc', '%s.csv' % conference), 'rb')
#     reader2 = UnicodeReader(f2)
#     
#     pcSet = set()
#     
#     for row in reader2:
#         year = int(row[0])
#         track = row[1]
#         name = normaliseName(row[2])
#         if len(name) and track=='main':
#             pcSet.add(name)
#             
#     print len(pcSet.difference(authorsSet)), 'unresolved out of', len(pcSet)
#     
#     suggestions = set()
#     
#     autho = authorsSet
# #    autho = allAuthorsSet
#     
#     for pcName in sorted(pcSet.difference(autho)):
# #        print pcName
#         candidates = []
#         s1 = set([p.lower() for p in pcName.split() if p.find('.')==-1])
#         for author in sorted(autho):
#             s2 = set([p.lower() for p in author.split() if p.find('.')==-1])
#             if s1 == s2:
#                 candidates.append(author)
# #                print '\t', author
#         if len(candidates) == 1:
#             suggestions.add((pcName, candidates[0]))
#         else:
#             try:
#                 aid = reverseLookup[pcName]
#                 name = directLookup[aid]
#             except:
#                 print pcName, candidates     
# #                pass
#         
#     print
#     for (a,b) in sorted(suggestions):
#         print '\t\'%s\':\'%s\',' % (a, b)
# 

