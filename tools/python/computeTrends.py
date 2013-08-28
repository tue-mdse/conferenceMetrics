# This Python file uses the following encoding: utf-8

import sys
import os
from scipy.stats.stats import kendalltau, spearmanr, pearsonr
from unicodeMagic import UnicodeReader

dataPath = os.path.abspath("../../")
metricsPath = os.path.join(dataPath, 'metrics') 

metric = sys.argv[1]

f = open(os.path.join(metricsPath, '%s.csv' % metric), 'rb')
reader = UnicodeReader(f)
header = reader.next()
# year;ICSE;ICSM;WCRE;CSMR;MSR;GPCE;FASE;ICPC;FSE;SCAM;ASE
conferences = header[1:]

data = {}

for row in reader:
    year = int(row[0])
    for idx, val in enumerate(row[1:]):
        conference = conferences[idx]
        if len(val):
            if data.has_key(conference):
                data[conference].append((year,float(val)))
            else:
                data[conference] = [(year,float(val))]
            
print '---', metric, '---'
res = []
for conference in sorted(conferences):
    vals = sorted(data[conference], key=lambda elem:elem[0])
    x = []
    y = []
    for (year, val) in vals:
        x.append(year)
        y.append(val)
    
    (tau, pval) = spearmanr(x,y)
    res.append((conference, tau, pval))
    
res = sorted(res, key=lambda elem:-elem[1])
for (conference, tau, pval) in res:
    if pval<0.05:
        print '\t'.join([conference, '%.3f'%tau, '%.8f'%pval, str(pval<0.05)])
for (conference, tau, pval) in res:
    if pval>=0.05:
        print '\t'.join([conference, '%.3f'%tau, '%.8f'%pval, str(pval<0.05)])