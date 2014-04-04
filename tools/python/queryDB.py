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
from initDB import Conference
import os
from unicodeMagic import UnicodeWriter
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



def tabulate2CSV(outPath, metric, k=None, datatype='float'):
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
                if datatype == 'float':
                    row.append('%.03f' % metrics[conferenceName].getMetric(metric,k)[year])
                elif datatype == 'int':
                    row.append(metrics[conferenceName].getMetric(metric,k)[year])
            except:
                row.append('')
        rowStr = [str(item) for item in row]
        writer.writerow(rowStr)
    f.close()    


def scatterPlot(outPath, metric1, metric2, k1=None, k2=None):
    f = open(outPath, 'wb')
    writer = UnicodeWriter(f)
    writer.writerow(['year', '%s%d'%(metric1,k1), '%s%d'%(metric2,k2), 'conference'])
    for conferenceName in conferences:        
        for year in reversed(sorted(set(metrics[conferenceName].getMetric(metric1,k1).keys()).intersection(set(metrics[conferenceName].getMetric(metric2,k2).keys())))):
            x = metrics[conferenceName].getMetric(metric1,k1)[year]
            y = metrics[conferenceName].getMetric(metric2,k2)[year]
            row = [year, x, y, conferenceName]
            rowStr = [str(item) for item in row]
            writer.writerow(rowStr)
    f.close()
    
    

tabulate2CSV(os.path.join(metricsPath, 'AP.csv'), 'AP', datatype='int')
tabulate2CSV(os.path.join(metricsPath, 'SP.csv'), 'SP', datatype='int')
tabulate2CSV(os.path.join(metricsPath, 'RA.csv'), 'RA')
tabulate2CSV(os.path.join(metricsPath, 'RL.csv'), 'RL')
tabulate2CSV(os.path.join(metricsPath, 'C.csv'), 'C', datatype='int')
tabulate2CSV(os.path.join(metricsPath, 'A.csv'), 'A', datatype='int')
tabulate2CSV(os.path.join(metricsPath, 'CnA4.csv'), 'CnA', 4, datatype='int')
tabulate2CSV(os.path.join(metricsPath, 'RCnA4.csv'), 'RCnA', 4)
tabulate2CSV(os.path.join(metricsPath, 'APC0.csv'), 'APC', 0, datatype='int')
tabulate2CSV(os.path.join(metricsPath, 'RAC0.csv'), 'RAC', 0)
tabulate2CSV(os.path.join(metricsPath, 'RAC4.csv'), 'RAC', 4)
tabulate2CSV(os.path.join(metricsPath, 'RNC1.csv'), 'RNC', 1)
tabulate2CSV(os.path.join(metricsPath, 'RNC4.csv'), 'RNC', 4)
tabulate2CSV(os.path.join(metricsPath, 'RNA1.csv'), 'RNA', 1)
tabulate2CSV(os.path.join(metricsPath, 'RNA4.csv'), 'RNA', 4)
tabulate2CSV(os.path.join(metricsPath, 'RPNA4.csv'), 'RPNA', 4)
tabulate2CSV(os.path.join(metricsPath, 'PNA4.csv'), 'PNA', 4)
tabulate2CSV(os.path.join(metricsPath, 'SR4.csv'), 'SR', 4)

scatterPlot(os.path.join(metricsPath, 'RAC0-RNC1.csv'), 'RAC', 'RNC', 0, 1)

tabulate2CSV(os.path.join(metricsPath, 'CM.csv'), 'CM', datatype='int')

tabulate2CSV(os.path.join(metricsPath, 'SC1.csv'), 'SC', 1, datatype='int')
tabulate2CSV(os.path.join(metricsPath, 'SymRelC1.csv'), 'SymRelC', 1)
tabulate2CSV(os.path.join(metricsPath, 'AsymRelC1.csv'), 'AsymRelC', 1)
        
tabulate2CSV(os.path.join(metricsPath, 'SA1.csv'), 'SA', 1, datatype='int')
tabulate2CSV(os.path.join(metricsPath, 'SymRelA1.csv'), 'SymRelA', 1)
tabulate2CSV(os.path.join(metricsPath, 'AsymRelA1.csv'), 'AsymRelA', 1)

tabulate2CSV(os.path.join(metricsPath, 'SCM1.csv'), 'SCM', 1, datatype='int')
tabulate2CSV(os.path.join(metricsPath, 'SymRelCM1.csv'), 'SymRelCM', 1)
tabulate2CSV(os.path.join(metricsPath, 'AsymRelCM1.csv'), 'AsymRelCM', 1)
