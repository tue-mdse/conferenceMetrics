from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from initDB import Paper, Person, Conference, PCMembership, SubmissionsCount, person_paper
import os
from unicodeMagic import UnicodeReader, UnicodeWriter
from metrics import ConferenceMetrics

dataPath = os.path.abspath("../../")
metricsPath = os.path.join(dataPath, 'metrics') 

engine = create_engine('mysql://root@localhost/conferences?charset=utf8')

'''Create a session for this connection'''
Session = sessionmaker(engine)
session = Session()

'''Which conferences are in the db'''
conferences = [c.acronym for c in session.query(Conference).all()]

'''Compute the metrics'''
print 'Computing metrics for conferences:'
metrics = {}
for conference in conferences:   
    print conference
    metrics[conference] = ConferenceMetrics(session, conference)
print



def tabulate(metric, k=None):
    allYears = set()
    for conferenceName in conferences:
        allYears.update(metrics[conferenceName].getMetric(metric,k).keys())

    header = ['year'] + [c.upper() for c in conferences]
    headerStr = [str(item) for item in header]
    print '\t'.join(headerStr)
    for year in reversed(sorted(allYears)):
        row = [year]
        for conferenceName in conferences:
            try:
                row.append('%.03f' % metrics[conferenceName].getMetric(metric,k)[year])
            except:
                row.append('')
        rowStr = [str(item) for item in row]
        print '\t'.join(rowStr)



def tabulate2CSV(outPath, metric, k=None, type='float'):
    allYears = set()
    for conferenceName in conferences:
        allYears.update(metrics[conferenceName].getMetric(metric,k).keys())

    f = open(outPath, 'wb')
    writer = UnicodeWriter(f)
    header = ['year'] + [c.upper() for c in conferences]
    headerStr = [str(item) for item in header]
    writer.writerow(headerStr)
    for year in reversed(sorted(allYears)):
        row = [year]
        for conferenceName in conferences:
            try:
                if type == 'float':
                    row.append('%.03f' % metrics[conferenceName].getMetric(metric,k)[year])
                elif type == 'int':
                    row.append(metrics[conferenceName].getMetric(metric,k)[year])
            except:
                row.append('')
        rowStr = [str(item) for item in row]
        writer.writerow(rowStr)
    f.close()    


tabulate2CSV(os.path.join(metricsPath, 'AP.csv'), 'AP', type='int')
tabulate2CSV(os.path.join(metricsPath, 'SP.csv'), 'SP', type='int')
tabulate2CSV(os.path.join(metricsPath, 'RA.csv'), 'RA')
tabulate2CSV(os.path.join(metricsPath, 'RL.csv'), 'RL')
tabulate2CSV(os.path.join(metricsPath, 'C.csv'), 'C', type='int')
tabulate2CSV(os.path.join(metricsPath, 'A.csv'), 'A', type='int')
tabulate2CSV(os.path.join(metricsPath, 'CnA4.csv'), 'CnA', 4, type='int')
tabulate2CSV(os.path.join(metricsPath, 'RCnA4.csv'), 'RCnA', 4)
tabulate2CSV(os.path.join(metricsPath, 'APC0.csv'), 'APC', 0, type='int')
tabulate2CSV(os.path.join(metricsPath, 'RAC0.csv'), 'RAC', 0)
tabulate2CSV(os.path.join(metricsPath, 'RAC4.csv'), 'RAC', 4)
tabulate2CSV(os.path.join(metricsPath, 'RNC1.csv'), 'RNC', 1)
tabulate2CSV(os.path.join(metricsPath, 'RNC4.csv'), 'RNC', 4)
tabulate2CSV(os.path.join(metricsPath, 'RNA1.csv'), 'RNA', 1)
tabulate2CSV(os.path.join(metricsPath, 'RNA4.csv'), 'RNA', 4)
tabulate2CSV(os.path.join(metricsPath, 'RPNA4.csv'), 'RPNA', 4)
        
