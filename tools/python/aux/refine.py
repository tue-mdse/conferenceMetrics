from dictUtils import MyDict
import os
import sys
sys.path.append('..')
from unicodeMagic import UnicodeReader, UnicodeWriter
from nameMap import nameMap
from unidecode import unidecode

conferenceName = 'gpce'

path_papers = "../../../data/bht2csv/%s_papers.csv" % conferenceName
path_PC = "../../../data/pc/%s.csv" % conferenceName


authorsPerYear = MyDict();     """Look up the authors that published in a particular year"""
yearsPerAuthor = MyDict();     """Look up the years in which a particular author has published"""
papersPerYear = MyDict();      """Look up the papers (paper = list of authors) published in a particular year"""
pcPerYear = MyDict();          """Look up the PC members for a particular year"""
yearsPerPC = MyDict();         """Look up the years in which a particular person has been on the PC"""


"""Normalizes a name using the lookup table and the 
different aliases used by the same person on DBLP"""
def cleanName(name, directLookup, reverseLookup):
    name = unidecode(name)
    """Try to fix typos using the lookup table"""
    try:
        name = authorMap[name]
    except:
        pass

    """If on DBLP, use consistent name"""
    try:
        aid = reverseLookup[name]
        name = directLookup[aid]
    except:
        pass
    return name


"""Helper data structures for DBLP aliases (name disambiguation)"""
reverseLookup = MyDict()
directLookup = MyDict()

"""Read list of DBLP aliases."""
path_DBLPaliases = "../../../data/dblp-author-aliases-stripped.csv"
f = open(os.path.abspath(path_DBLPaliases), "rb")
reader1 = UnicodeReader(f)
# Read the list into a map
for row in reader1:
    aid = int(row[0])
    aliases = [name.strip() for name in row[1].split(',')]
    for name in aliases:
        reverseLookup[name] = aid
    directLookup[aid] = aliases[-1]


authorsSet = set()

f = open(os.path.abspath(path_papers), "rb")
reader = UnicodeReader(f)
for row in reader:
    year = int(row[0])
    authorsStr = row[1]
    authors = [cleanName(a.strip(), directLookup, reverseLookup) for a in authorsStr.split(',')]
    authorsSet.update(authors)
f.close()

pcSet = set()

f = open(os.path.abspath(path_PC), "rb")
reader = UnicodeReader(f)
for row in reader:
    year = int(row[0])
    track = row[1]
    if track == 'main':
        name = cleanName(row[2], directLookup, reverseLookup)
        pcSet.add(name)


g = open(os.path.abspath("../../../data/temp/%s-authors.csv" % conferenceName), "wb")
writer = UnicodeWriter(g)
for author in sorted(authorsSet):
    writer.writerow([author, 'author'])
for author in sorted(pcSet):
    writer.writerow([author, 'pc'])
g.close()





