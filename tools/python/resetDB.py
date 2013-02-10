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
    
