from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
metadata = Base.metadata


author_paper = Table('author_paper', metadata,
                     Column('author_id', Integer, ForeignKey('authors.id')),
                     Column('paper_id', Integer, ForeignKey('papers.id')))


class PCMember(Base):
    __tablename__ = 'pc_members'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    
    conferences = association_proxy("pcmemberships", "conference")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<PCMember('%s')>" % (self.name)


class Conference(Base):
    __tablename__ = 'conferences'
    id = Column(Integer, primary_key=True)
    acronym = Column(String(20), nullable=False)
    name = Column(String(200))
    impact = Column(Integer)

#    '''Many to many PCMember<->Conference'''
    pcmembers = association_proxy("pcmemberships", "pcmember")

    def __init__(self, acronym, impact, name=None):
        self.acronym = acronym
        self.impact = impact
        self.name = name

    def __repr__(self):
        return "<Conference('%s')>" % (self.acronym)


class SubmissionsCount(Base):
    __tablename__ = 'submissions'
    id = Column(Integer, primary_key=True)
    conference_id = Column(Integer, ForeignKey('conferences.id'))
    year = Column(Integer)
    number = Column(Integer)

    conference = relationship(Conference, backref="submissions")

    def __init__(self, year, number):
        self.year = year
        self.number = number


class PCMembership(Base):
    __tablename__ = 'pc_membership'
    id = Column(Integer, primary_key=True)
    pcmember_id = Column(Integer, ForeignKey('pc_members.id'))
    conference_id = Column(Integer, ForeignKey('conferences.id'))
    year = Column(Integer)
    track = Column(String(100))
    
    def __init__(self, year, track):
        self.year = year
        self.track = track
    
    conference = relationship(Conference, backref="pcmemberships")
    pcmember = relationship(PCMember, backref="pcmemberships")    


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Author('%s')>" % (self.name)


class Paper(Base):
    __tablename__ = 'papers'
    id = Column(Integer, primary_key=True)
    conference_id = Column(Integer, ForeignKey('conferences.id'))
    year = Column(Integer)
    title = Column(String(500))
    pages = Column(String(10))
    num_pages = Column(Integer)
    session_h2 = Column(String(100))
    session_h3 = Column(String(100))
    main_track = Column(Boolean)
    
    '''Many to many Author<->Paper'''
    authors = relationship('Author', secondary=author_paper, backref='papers')

    '''One to many Conference<->Paper'''
    conference = relationship("Conference", backref=backref('papers', order_by=id))

    def __init__(self, conference, year, title, pages, num_pages, session_h2, session_h3, selected=False):
        self.conference = conference
        self.year = year
        self.title = title
        self.pages = pages
        self.num_pages = num_pages
        self.session_h2 = session_h2.strip()
        self.session_h3 = session_h3.strip()
        self.main_track = selected

    def __repr__(self):
        return "<Paper('%s, %d, %s')>" % (self.conference, self.year, self.title)


def initDB(engine):
    metadata.create_all(engine) 
    print 'Database structure created'
    
    
