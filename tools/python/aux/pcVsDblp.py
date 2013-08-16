# This Python file uses the following encoding: utf-8

from lxml import etree, html
import os
import sys
sys.path.append('..')
from unicodeMagic import UnicodeReader, UnicodeWriter
from dictUtils import MyDict
from nameMap import nameMap
from unidecode import unidecode

#conference = "icse"
conference = sys.argv[1]


# This is the list of DBLP author names (>1.1M people)
# 335078;M. G. J. van den Brand, Mark G. J. van den Brand, Mark van den Brand
f = open(os.path.abspath("../../../data/dblp-author-aliases-stripped.csv"), "rb")
reader1 = UnicodeReader(f)

# Read the list into a map
# reverseLookup['M. G. J. van den Brand'] 
# 	= reverseLookup['Mark G. J. van den Brand'] 
# 	= reverseLookup['Mark van den Brand']
# 	= 335078
reverseLookup = MyDict()
for row in reader1:
    aid = int(row[0])
    aliases = [name.strip() for name in row[1].split(',')]
    for name in aliases:
        reverseLookup[name] = aid

# Read names of conference PC members
# There are two cases:
# 1. Somebody appears in the DBLP data, with the same spelling (not interesting)
# 2. Somebody does not appear in the DBLP data, or his/her name has a different spelling
g = open(os.path.abspath("../../../data/pc/%s.csv" % conference), "rb")
reader2 = UnicodeReader(g)

# Record all conference PC members whose names DO NOT match DBLP
unknowns = set()
for row in reader2:
	# First convert unicode chars
    name = unidecode(row[2])
    # Then pass through filter
    try:
        name = nameMap[name]
    except:
        pass
    # Remember name if not in DBLP
    try:
        aid = reverseLookup[name]
    except:
        unknowns.add(name)

# Start name matching between conference PC and DBLP aliases
g = open(os.path.abspath("../../../data/temp/map_%s.csv" % conference), "wb")
writer = UnicodeWriter(g)

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
                print "\'%s\': \'%s\'," % (name, key)
                writer.writerow(["\'%s\':\'%s\'," % (name, key)])
                
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
                    print "\'%s\': \'%s\'," % (name, key)
                    writer.writerow(["\'%s\':\'%s\'," % (name, key)])
                    soFarSoGood.add(name)

g.close()

# Update the unknown set again
unknowns.difference_update(soFarSoGood)

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
                    print "\'%s\': \'%s\'," % (name, key)


# for name in sorted(unknowns):
#     for key in reverseLookup.keys():
#         if key.find(name) != -1:
#             print "\'%s\': \'%s\'," % (name, key)

    
    
