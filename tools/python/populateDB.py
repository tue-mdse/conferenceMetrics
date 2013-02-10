from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from unicodeMagic import UnicodeReader, UnicodeWriter
from unidecode import unidecode
from initDB import Base
from initDB import Paper, Person, Conference, PCMembership, SubmissionsCount
from resetDB import cleanStart
from initDB import initDB


dataPath = os.path.abspath("../../data")

conferences = ['icse', 'icsm', 'wcre', 'csmr', 'msr', 'gpce', 'fase', 'icpc', 'fse', 'scam', 'ase']

'''Conference impact computed for the entire period 2000-2012
http://shine.icomp.ufam.edu.br/index.php'''
impact = {
    'ICSE':117, 
    'ICSM':53, 
    'CSMR':40,
    'WCRE':43,
    'ICPC':43,
    'ASE':55,
    'FSE':49,
    'FASE':42,
    'GPCE':37,
    'SCAM':15,
    'MSR':32,
}


engine = create_engine('mysql://root@localhost/conferences?charset=utf8')

'''Reset the database (drop all tables)'''
cleanStart(engine)

'''Create the table structure'''
initDB(engine)


'''Create an engine and get the metadata'''
#Base = declarative_base(engine)
metadata = Base.metadata

'''Create a session for this conference'''
Session = sessionmaker(engine)
session = Session()


print 'Loading papers:'
for conferenceName in conferences:
    acronym = conferenceName
    print acronym.upper()
    
    '''Create a new conference object'''
    conference = Conference(acronym.upper(), impact[acronym.upper()])
    session.add(conference)
    
    '''Load the data into a csv reader'''
    f = open(os.path.join(dataPath, 'normalised-papers', '%s.csv' % conferenceName), 'rb')
    reader = UnicodeReader(f)
    
    for row in reader:
        '''Deconstruct each row'''
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
        selected = row[7]
        
        '''Create new paper and add it to the session'''
        if selected == 'selected':
            paper = Paper(conference, year, title, pages, num_pages, session_h2, session_h3, True)
        else:
            paper = Paper(conference, year, title, pages, num_pages, session_h2, session_h3)
        session.add(paper)
        
        '''Add the authors'''
        for author_name in author_names:
            try:
                '''I already have this author in the database'''
                author = session.query(Person).\
                        filter_by(name=author_name).\
                        one()
            except:
                '''New author; add to database'''
                author = Person(author_name)
                session.add(author)

            paper.authors.append(author)



print 'Loading PC members:'
for conferenceName in conferences:
    acronym = conferenceName
    print acronym.upper()
    
    '''Get the conference object'''
    try:
        '''I already have this PC conference in the database'''
        conference = session.query(Conference).\
                filter_by(acronym=acronym).\
                one()
    except:
        '''New conference; add to database'''
        conference = Conference(acronym.upper())
        session.add(conference)
        
    '''Load the data into a csv reader'''
    f = open(os.path.join(dataPath, 'normalised-pc', '%s.csv' % acronym.lower()), 'rb')
    reader = UnicodeReader(f)

    for row in reader:
        '''Deconstruct each row'''
        year = int(row[0])
        track = row[1]
        pcMemberName = row[2].strip()
    
        if len(pcMemberName):
            '''Get the PC member object'''
            try:
                '''I already have this PC member in the database'''
                pcMember = session.query(Person).\
                        filter_by(name=pcMemberName).\
                        one()
            except:
                '''New person; add to database'''
                pcMember = Person(pcMemberName)
                session.add(pcMember)

            try:
                membership = session.query(PCMembership).\
                        filter_by(year=year).\
                        filter_by(track=track).\
                        filter_by(pcmember=pcMember).\
                        filter_by(conference=conference).\
                        one()
            except:
                '''New, add to database'''
                membership = PCMembership(year, track)
    
                membership.pcmember = pcMember
                membership.conference = conference
                session.add(membership)
                


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
