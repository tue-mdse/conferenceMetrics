"""Copyright 2012-2013
Eindhoven University of Technology (Bogdan Vasilescu and Alexander Serebrenik) and
University of Mons (Tom Mens)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from unicodeMagic import UnicodeReader
from unidecode import unidecode
from initDB import Paper, Person, Conference, PCMembership, SubmissionsCount
from resetDB import cleanStart
from initDB import initDB
from initDB import Base

from nameMap import nameMap


dataPath = os.path.abspath("../../data")

conferences = ['icse', 'icsm', 'wcre', 'csmr', 'msr', 'gpce', 'fase', 'icpc', 'fse', 'scam', 'ase']

# Conference impact computed for the entire period 2000-2013
# http://shine.icomp.ufam.edu.br/index.php
impact = {
    'ICSE':117, 
    'ICSM':53, 
    'WCRE':43,
    'CSMR':40,
    'MSR':32,
    'GPCE':37,
    'FASE':42,
    'ICPC':43,
    'FSE':59,
    'SCAM':15,
    'ASE':55,
}


engine = create_engine('mysql://root@localhost/conferences?charset=utf8')

# Reset the database (drop all tables)
cleanStart(engine)

# Create the table structure
initDB(engine)


# Create an engine and get the metadata
#Base = declarative_base(engine)
metadata = Base.metadata

# Create a session for this conference
Session = sessionmaker(engine)
session = Session()


print 'Loading papers:'
for conferenceName in conferences:
    acronym = conferenceName
    print acronym.upper()
    
    # Create a new conference object
    conference = Conference(acronym.upper(), impact[acronym.upper()])
    session.add(conference)
    
    # Load the data into a csv reader
    f = open(os.path.join(dataPath, 'normalised-papers', '%s.csv' % conferenceName), 'rb')
    reader = UnicodeReader(f)
    
    for row in reader:
        # Deconstruct each row
        year = int(row[0])
        author_names = [a.strip() for a in row[1].split(',')]
        title = row[2]
        pages = row[3]
        try:
            num_pages = int(row[4])
        except:
            num_pages = 0
        session_h2 = unidecode(row[5]).strip()
        session_h3 = unidecode(row[6]).strip()
        try:
            selected = row[7]
        except:
            print row
            exit()
        
        # Create new paper and add it to the session
        if selected == 'selected':
            paper = Paper(conference, year, title, pages, num_pages, session_h2, session_h3, True)
        else:
            paper = Paper(conference, year, title, pages, num_pages, session_h2, session_h3)
        session.add(paper)
        
        # Add the authors
        for author_name in author_names:
            try:
                author_name = nameMap[author_name]
            except:
                pass
            try:
                # I already have this author in the database
                author = session.query(Person).\
                        filter_by(name=author_name).\
                        one()
            except:
                # New author; add to database
                author = Person(author_name)
                session.add(author)

            paper.authors.append(author)


# --- Update 8/12/2013 ---
# Record also the role of PC members (PC Chair or General Chair)
f = open(os.path.join(dataPath, 'SE-conf-roles.csv'), 'rb')
reader = UnicodeReader(f)
header = reader.next()
roles = {}

def confName(conf):
    if conf == 'ESEC/FSE':
        return 'FSE'
    elif conf == 'CSMR-WCRE':
        return 'CSMR'
    else:
        return conf
     
for row in reader:
    conf = confName(row[0].strip()).lower()
    year = int(row[1])
    name = '%s %s' % (row[2].strip(), row[3].strip())
    try:
        name = nameMap[name]
    except:
        pass
    role = row[5]
    if role == 'Organiser':
        role = 'PC member main track'
    
    if '?' not in name and role != 'Challenge Chair' and role != 'Data Chair':
        roles[(name, conf, year)] = role
    
#Conference;Year;First Name;Last Name;Sex;Role
#CSMR;2013;Anthony ;Cleve;Male;Program Chair
#CSMR;2013;Filippo;Ricca;Male;Program Chair
#CSMR;2013;Maura;Cerioli;Female;General Chair
# -----------------------


print 'Loading PC members:'
for conferenceName in conferences:
    acronym = conferenceName
    print acronym.upper()
    
    # Get the conference object
    try:
        # I already have this PC conference in the database
        conference = session.query(Conference).\
                filter_by(acronym=acronym).\
                one()
    except:
        # New conference; add to database
        conference = Conference(acronym.upper())
        session.add(conference)
        
    # Load the data into a csv reader
    f = open(os.path.join(dataPath, 'normalised-pc', '%s.csv' % acronym.lower()), 'rb')
    reader = UnicodeReader(f)

    # --- Update 8/12/2013 ---
    withRole = set([(name, year) for (name, conf, year) in roles.keys() if conf==acronym])
    # -----------------------
    
    for row in reader:
        # Deconstruct each row
        year = int(row[0])
        role = row[1]
        pcMemberName = row[2].strip()
        
        # --- Update 8/12/2013 ---        
        if roles.has_key((pcMemberName, acronym, year)):
            role = roles[(pcMemberName, acronym, year)]
            try:
                withRole.remove((pcMemberName, year))
            except:
                pass
        else:
            role = 'PC member main track'
        # ----------------------- 
    
        if len(pcMemberName):
            # Get the PC member object
            try:
                # I already have this PC member in the database
                pcMember = session.query(Person).\
                        filter_by(name=pcMemberName).\
                        one()
            except:
                # New person; add to database
                pcMember = Person(pcMemberName)
                session.add(pcMember)

            try:
                membership = session.query(PCMembership).\
                        filter_by(year=year).\
                        filter_by(role=role).\
                        filter_by(pcmember=pcMember).\
                        filter_by(conference=conference).\
                        one()
            except:
                # New, add to database
                membership = PCMembership(year, role)
    
                membership.pcmember = pcMember
                membership.conference = conference
                session.add(membership)
      
    # --- Update 8/12/2013 ---
    print sorted(withRole)
    # -----------------------


print 'Loading acceptance ratios:'
f = open(os.path.join(dataPath, 'numSubmissions.csv'), "rb")
reader = UnicodeReader(f)
header = reader.next()
subm = {}
for row in reader:
    year = int(row[0])
    for idx,val in enumerate(row[1:]):
        conf = header[idx+1]
        try:
            count = int(val)
            if conf not in subm.keys():
                subm[conf] = {}
            subm[conf][year] = count
        except:
            pass
        
        
for conferenceName in conferences:
    print conferenceName.upper()
    conference = session.query(Conference).\
            filter_by(acronym=conferenceName.upper()).\
            one()
        
    for (year,count) in subm[conferenceName.upper()].items():
        numSubm = SubmissionsCount(year, count)
        numSubm.conference = conference
        session.add(numSubm)


session.commit()


print 'Finished loading data'
