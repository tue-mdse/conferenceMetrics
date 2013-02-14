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

from sqlalchemy import MetaData


def cleanStart(engine):
    meta = MetaData(bind=engine)
    
    '''Reflect: get the tables currently in the database''' 
    meta.reflect(engine)
    
#    print 'DB contains tables:'
#    for t in metadata.sorted_tables:
#        print '\t', t.name
    
    '''Drop all tables (fresh start)'''
    meta.drop_all(engine)
    print 'Database structure reset'
    
