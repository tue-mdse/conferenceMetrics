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

from sqlalchemy import func
from initDB import Paper, Conference, PCMembership, SubmissionsCount


class ConferenceMetrics():
    def __init__(self, session, conference):
        self.session = session
        self.name = conference
        
        # Helper data structures
        (self.authorsPerYear, self.yearsPerAuthor) = self.__extractAuthors();  # Look up the authors that published in a particular year
        self.papersPerYear = self.__extractPapers();    # Look up the papers (paper = list of authors) published in a particular year
        self.pcPerYear = self.__extractPC();            # Look up the PC members for a particular year
        self.coreAuthors = self.__computeCore(self.yearsPerAuthor)
        self.membersPerYear = self.__computeMembers();         # Conference members per year (union of authors and PC members)
        
        # Metrics
        self.AP = self.__computeAP();   # Number of accepted papers per year
        self.SP = self.__computeSP();   # Number of submissions per year
        self.RA = self.__computeRA();   # Acceptance rate: #acc/#subm
        self.RL = self.__computeRL();   # Review load: #subm/#PCmem
        self.A = self.__computeA();     # Number of authors per year
        self.C = self.__computeC();     # Number of PC members per year
        self.CM = self.__computeCM();     # Number of community members per year
        
        self.CnA4 = self.__computeCnA(4);   # Number of PC members for a given year that have never been authors between y-n and y-1
        self.RCnA4 = self.__computeRCnA(4); # Wild-Card Ratio: %PC members for a given year that have never been authors between y-n and y-1 (sliding window)
        
        self.APC0 = self.__computeAPC(0);   # Number of papers published in a given year that have at least one PC member from y-n..y as author
        
        self.RAC0 = self.__computeRAC(0);   # Inbreeding ratio (IR): fraction of papers published in a given year that have at least one PC member from y-n..y as author
        self.RAC4 = self.__computeRAC(4)
        
        self.NC1 = self.__computeNC(1);     # ([N]ew [C]ommittee) PC Turnover: number of PC members for a given year that have not been on the PC between y-n and y-1
        self.NC4 = self.__computeNC(4)
        self.RNC1 = self.__computeRNC(1);   # PC Turnover Ratio: fraction of PC members for a given year that have not been on the PC between y-n and y-1
        self.RNC4 = self.__computeRNC(4)
        
        self.NA1 = self.__computeNA(1);     # Author Turnover: number of authors for a given year that have not been author between y-n and y-1
        self.NA4 = self.__computeNA(4);
        self.RNA1 = self.__computeRNA(1);   # Author Turnover Ratio: fraction of authors for a given year that have not been author between y-n and y-1
        self.RNA4 = self.__computeRNA(4);
        
        self.PNA4 = self.__computePNA(4);   # Number of papers published in a given year for which none of the co-authors has published here between y-n and y-1
        self.RPNA4 = self.__computeRPNA(4); # Fraction of the papers published in a given year for which none of the co-authors has published here between y-n and y-1
        
        self.SR4 = self.__computeSR(4); # Sustainability ratio
        
        self.SC1 = self.__computeSC(1);     # ([S]ame [C]ommittee) = number of PC members for a given year that have also served on the PC between y-n and y-1
        self.SymRelC1 = self.__computeSymRelC(1); # Relative number of PC members in common (symmetric version) = Absolute number of PC members in common / Size of the union of PC(c,y) and PC(c,y-1)
        self.AsymRelC1 = self.__computeAsymRelC(1); # Relative number of recurrent PC members (asymmetric version) = Absolute number of PC members in common / Size of PC(c,y) = percentage of PC members for c in year y that were also PC member in year y-1
        
        self.SA1 = self.__computeSA(1);     # ([S]ame [A]uthors)
        self.SymRelA1 = self.__computeSymRelA(1); # 
        self.AsymRelA1 = self.__computeAsymRelA(1); #
        
        self.SCM1 = self.__computeSCM(1);     # ([S]ame [C]onference[M]embers)
        self.SymRelCM1 = self.__computeSymRelCM(1); # 
        self.AsymRelCM1 = self.__computeAsymRelCM(1) #
            
    def getMetric(self, metric, k=None):
        if metric == 'AP':
            return self.AP
        
        elif metric == 'SP':
            return self.SP
        
        elif metric == 'RA':
            return self.RA
        
        elif metric == 'RL':
            return self.RL
        
        elif metric == 'A':
            return self.A
        
        elif metric == 'C':
            return self.C
        
        elif metric == 'CM':
            return self.CM
        
        elif metric == 'CnA':
            if k is not None and k == 4:
                return self.CnA4
            else:
                return self.__computeCnA(k)
        
        elif metric == 'RCnA':
            if k is not None:
                if k == 4:
                    return self.RCnA4
                else:
                    return self.__computeRCnA(k)
        
        elif metric == 'APC':
            if k is not None:
                if k == 0:
                    return self.APC0
                else:
                    return self.__computeAPC(k)
            
        elif metric == 'RAC':
            if k is not None:
                if k == 0:
                    return self.RAC0
                elif k == 4:
                    return self.RAC4
                else:
                    return self.__computeRAC(k)
                
        elif metric == 'NC':
            if k is not None:
                if k == 1:
                    return self.NC1
                elif k == 4:
                    return self.NC4
                else:
                    return self.__computeNC(k)
                
        elif metric == 'SC':
            if k is not None:
                if k == 1:
                    return self.SC1
                else:
                    return self.__computeSC(k)
                
        elif metric == 'SymRelC':
            if k is not None:
                if k == 1:
                    return self.SymRelC1
                else:
                    return self.__computeSymRelC(k)
            
        elif metric == 'AsymRelC':
            if k is not None:
                if k == 1:
                    return self.AsymRelC1
                else:
                    return self.__computeAsymRelC(k)
                
        elif metric == 'SA':
            if k is not None:
                if k == 1:
                    return self.SA1
                else:
                    return self.__computeSA(k)
                
        elif metric == 'SymRelA':
            if k is not None:
                if k == 1:
                    return self.SymRelA1
                else:
                    return self.__computeSymRelA(k)
            
        elif metric == 'AsymRelA':
            if k is not None:
                if k == 1:
                    return self.AsymRelA1
                else:
                    return self.__computeAsymRelA(k)
                
        
        elif metric == 'SCM':
            if k is not None:
                if k == 1:
                    return self.SCM1
                else:
                    return self.__computeSCM(k)
                
        elif metric == 'SymRelCM':
            if k is not None:
                if k == 1:
                    return self.SymRelCM1
                else:
                    return self.__computeSymRelCM(k)
            
        elif metric == 'AsymRelCM':
            if k is not None:
                if k == 1:
                    return self.AsymRelCM1
                else:
                    return self.__computeAsymRelCM(k)        
        
            
        elif metric == 'RNC':
            if k is not None:
                if k == 1:
                    return self.RNC1
                elif k == 4:
                    return self.RNC4
                else:
                    return self.__computeRNC(k)
            
        elif metric == 'NA':
            if k is not None:
                if k == 1:
                    return self.NA1
                elif k == 4:
                    return self.NA4
                else:
                    return self.__computeNA(k)
            
        elif metric == 'RNA':
            if k is not None:
                if k == 1:
                    return self.RNA1
                elif k == 4:
                    return self.RNA4
                else:
                    return self.__computeRNA(k)
                
        elif metric == 'PNA':
            if k is not None:
                if k == 4:
                    return self.PNA4
                else:
                    return self.__computePNA(k)
            
        elif metric == 'RPNA':
            if k is not None:
                if k == 4:
                    return self.RPNA4
                else:
                    return self.__computeRPNA(k)
                    
        elif metric == 'SR':
            if k is not None:
                if k == 4:
                    return self.SR4
                else:
                    return self.__computeSR(k)
                    
 
            
    def __extractAuthors(self):
        """Look up the authors that published in a particular year"""
        d = {}
        y = {}
        for paper in self.session.query(Paper).\
                            join(Conference).\
                            filter(Conference.acronym == self.name).\
                            filter(Paper.main_track == True):
            year = paper.year
            if year not in d.keys():
                d[year] = set()
            for author in paper.authors:
                d[year].add(author.name)
                if y.has_key(author.name):
                    y[author.name].add(year)
                else:
                    y[author.name] = set([year])
                
        return (d, y)
            
            
            
    def __computeMembers(self):
        """Conference members for conference c for a given year:
        = union of conference authors and PC members"""
        d = {}
        for year in set(self.authorsPerYear.keys()).intersection(set(self.pcPerYear.keys())):
            d[year] = self.authorsPerYear[year].union(self.pcPerYear[year])
        return d


            
    def __computeCore(self, yearsPerName):
        """Compute core persons (authors, PC members = frequent flyers)"""
        corePeople = {}
        """Core people stretch up to five years in the past, given a certain edition of the conference.
        Conditions for authors:
        - (co)authored papers in at least 3 out of the 5 most recent editions, or
        - (co)authored papers in at least 2 out the the 3 most recent editions
        Analogously for PC members
        => I can only compute core people starting with the third edition of the conference."""
        years = set()
        for name in yearsPerName.keys():
            years.update(yearsPerName[name])
        years = sorted(years, key = lambda year: -year) # descending
        # at least 2 out the the 3 most recent editions
        for idx1, year in enumerate(years[:-2]):
            idx2 = idx1 + 3
            for name in yearsPerName.keys():
                if len(yearsPerName[name].intersection(set(years[idx1:idx2]))) >= 2:
                    try:
                        corePeople[year].add(name)
                    except:
                        corePeople[year] = set()
                        corePeople[year].add(name)
        # at least 3 out of the 5 most recent editions
        for idx1, year in enumerate(years[:-4]):
            idx2 = idx1 + 5
            for name in yearsPerName.keys():
                if len(yearsPerName[name].intersection(set(years[idx1:idx2]))) >= 3:
                    try:
                        corePeople[year].add(name)
                    except:
                        corePeople[year] = set()
                        corePeople[year].add(name)
            
        return corePeople
            
    
    def __extractPapers(self):
        """Look up the papers (paper = list of authors) published in a particular year"""
        d = {}
        for paper in self.session.query(Paper).\
                            join(Conference).\
                            filter(Conference.acronym == self.name).\
                            filter(Paper.main_track == True):
            year = paper.year
            if year not in d.keys():
                d[year] = []
            d[year].append(set([author.name for author in paper.authors]))
        return d
    
          
    def __computeA(self):
        """Number of authors per year"""
        a = self.authorsPerYear
        d = {}
        for year in a.keys():
            d[year] = len(a[year])
        return d
    
            
    def __extractPC(self):
        """Look up the PC members for a particular year"""
        d = {}
        for pcm in self.session.query(PCMembership).\
                            join(Conference).\
                            filter(Conference.acronym == self.name):
            year = pcm.year
            if year not in d.keys():
                d[year] = set()
            d[year].add(pcm.pcmember.name)
        return d


    def __computeC(self):
        """Number of PC members per year"""
        d = {}
        pc = self.pcPerYear
        for year in pc.keys():
            d[year] = len(pc[year])
        return d


    def __computeCM(self):
        """Number of community members per year"""
        d = {}
        for year in self.membersPerYear.keys():
            d[year] = len(self.membersPerYear[year])
        return d
    

    def __computeSP(self):
        '''Compute the number of submissions per conference per year'''
        d = {}
        for y, n in self.session.query(SubmissionsCount.year, SubmissionsCount.number).\
                            filter(SubmissionsCount.conference_id == Conference.id).\
                            filter(Conference.acronym == self.name).\
                            all():
            d[y] = n
        return d


    def __computeAP(self):
        d = {}
        '''Compute the number of accepted papers per conference per year'''
        for y, n in self.session.query(Paper.year, func.count(Paper.id)).\
                                filter(Paper.conference_id == Conference.id).\
                                filter(Paper.main_track == True).\
                                filter(Conference.acronym == self.name).\
                                group_by(Paper.year).\
                                all():
            d[y] = n
        return d


    def __computeRA(self):
        """Acceptance rate: #acc/#subm"""
        d = {}
        sp = self.SP
        ap = self.AP
        for year in set(sp.keys()).intersection(set(ap.keys())):
            d[year] = float(ap[year]) / float(sp[year])
        return d


    def __computeRL(self):
        """Reviewer load: #subm/#PCmem"""
        d = {}
        c = self.pcPerYear
        sp = self.SP
        for year in set(sp.keys()).intersection(set(c.keys())):
            d[year] = float(sp[year]) / float(len(c[year]))
        return d        


    def __absWindowDiff(self, data, k):
        d = {}
        years = sorted(data.keys())
        for year in years[k:]:
            previous = set()
            for y in [y for y in years[years.index(year)-k: years.index(year)]]:
                previous.update(data[y])
            d[year] = len(data[year].difference(previous))
        return d


    def __absWindowIntersect(self, data, k):
        d = {}
        years = sorted(data.keys())
        for year in years[k:]:
            previous = set()
            for y in [y for y in years[years.index(year)-k: years.index(year)]]:
                previous.update(data[y])
            d[year] = len(data[year].intersection(previous))
        return d
    
    
    def __ratioWindowDiff(self, data, k):
        d = {}
        years = sorted(data.keys())
        for year in years[k:]:
            previous = set()
            for y in [y for y in years[years.index(year)-k: years.index(year)]]:
                previous.update(data[y])
            d[year] = float(len(data[year].difference(previous))) / float(len(data[year]))
        return d
    
    
    def __ratioWindowIntersectAsym(self, data, k):
        d = {}
        years = sorted(data.keys())
        for year in years[k:]:
            previous = set()
            for y in [y for y in years[years.index(year)-k: years.index(year)]]:
                previous.update(data[y])
            d[year] = float(len(data[year].intersection(previous))) / float(len(data[year]))
        return d
    
    
    def __ratioWindowIntersectSym(self, data, k):
        d = {}
        years = sorted(data.keys())
        for year in years[k:]:
            previous = set()
            for y in [y for y in years[years.index(year)-k: years.index(year)]]:
                previous.update(data[y])
            d[year] = float(len(data[year].intersection(previous))) / float(len(previous))
        return d


    def __computeAPC(self, k=0):
        """Number of papers published in a given year that have at least one PC member from y-n..y as author"""
        papers = self.papersPerYear
        pc = self.pcPerYear
        pcAuthored = {}
        years = sorted(set(pc.keys()).intersection(papers.keys()))
        for year in years[k:]:
            pcAuthored[year] = 0
            previous = set()
            for y in [y for y in years[years.index(year)-k: years.index(year)+1]]:
                previous.update(pc[y])
            for paper in papers[year]:
                if len(paper.intersection(previous)):
                    pcAuthored[year] += 1
        return pcAuthored


    def __computeRAC(self, k):
        """Inbreeding ratio (IR): fraction of papers published in a given year that have at least one PC member from y-n..y as author"""
        pcAuthored = self.__computeAPC(k)
        papers = self.papersPerYear
        d = {}
        for year in pcAuthored.keys():
            d[year] = float(pcAuthored[year]) / float(len(papers[year]))
        return d
          
          
    def __computeCnA(self, k=4):
        """Number of PC members for a given year that have never been authors between y-n and y-1"""
        authors = self.authorsPerYear
        pc = self.pcPerYear
        d = {}
        years = sorted(set(pc.keys()).intersection(authors.keys()))
        for year in years[k:]:
            d[year] = 0
            previous = set()
            for y in [y for y in years[years.index(year)-k: years.index(year)]]:
                previous.update(authors[y])
            d[year] = len(pc[year].difference(previous))
        return d
    
    
    def __computeRCnA(self, k=4):
        """Wild-Card Ratio: %PC members for a given year that have never been authors between y-n and y-1"""
        pc = self.pcPerYear
        count = self.__computeCnA(k)
        d = {}
        for year in count.keys():
            d[year] = float(count[year]) / float(len(pc[year]))
        return d
        
            
    def __computeNA(self, k):
        """Author Turnover: number of authors for a given year that have not been author between y-n and y-1"""
        return self.__absWindowDiff(self.authorsPerYear, k)


    def __computeRNA(self, k):
        """Author Turnover Ratio: fraction of authors for a given year that have not been author between y-n and y-1"""
        return self.__ratioWindowDiff(self.authorsPerYear, k)


    def __computeNC(self, k):
        """PC Turnover: number of PC members for a given year that have not been on the PC between y-n and y-1"""
        return self.__absWindowDiff(self.pcPerYear, k)


    def __computeSC(self, k):
        """Absolute number of PC members in common in successive versions of the conference 
        = Size of the intersection of PC(c,y) and PC(c,y-k)"""
        return self.__absWindowIntersect(self.pcPerYear, k)
    
    
    def __computeSymRelC(self, k):
        """Relative number of PC members in common (symmetric version) 
        = Absolute number of PC members in common / Size of the union of PC(c,y) and PC(c,y-k)"""
        return self.__ratioWindowIntersectSym(self.pcPerYear, k)
    
    
    def __computeAsymRelC(self, k):
        """Relative number of recurrent PC members (asymmetric version) 
        = Absolute number of PC members in common / Size of PC(c,y) 
        = percentage of PC members for c in year y that were also PC member in year y-1"""
        return self.__ratioWindowIntersectAsym(self.pcPerYear, k)



    def __computeSA(self, k):
        return self.__absWindowIntersect(self.authorsPerYear, k)
    
    def __computeSymRelA(self, k):
        return self.__ratioWindowIntersectSym(self.authorsPerYear, k)
    
    def __computeAsymRelA(self, k):
        return self.__ratioWindowIntersectAsym(self.authorsPerYear, k)


    def __computeSCM(self, k):
        return self.__absWindowIntersect(self.membersPerYear, k)
    
    def __computeSymRelCM(self, k):
        return self.__ratioWindowIntersectSym(self.membersPerYear, k)
    
    def __computeAsymRelCM(self, k):
        return self.__ratioWindowIntersectAsym(self.membersPerYear, k)


    def __computeRNC(self, k):
        """PC Turnover Ratio: fraction of PC members for a given year that have not been on the PC between y-n and y-1"""
        return self.__ratioWindowDiff(self.pcPerYear, k)


    def __computePNA(self, k):
        """Number of papers published in a given year for which none of the co-authors has published here between y-n and y-1"""
        papers = self.papersPerYear
        authors = self.authorsPerYear
        d = {}
        years = sorted(set(authors.keys()).intersection(papers.keys()))
        for year in years[k:]:
            d[year] = 0
            previous = set()
            for y in [y for y in years[years.index(year)-k: years.index(year)]]:
                previous.update(authors[y])
            for paper in papers[year]:
                if len(paper.intersection(previous)) == 0:
                    d[year] += 1
        return d
    
    
    def __computeRPNA(self, k):
        """Fraction of the papers published in a given year for which none of the co-authors has published here between y-n and y-1"""
        papers = self.papersPerYear
        before = self.__computePNA(k)
        d = {}
        for year in before.keys():
            d[year] = float(before[year])/ float(len(papers[year]))
        return d


    def __computeSR(self, k):
        """Sustainability ratio"""
        core = self.coreAuthors        
        pc = self.pcPerYear
        sr = {}
        years = sorted(set(core.keys()).intersection(pc.keys()))
        for year in years[k:]:
            previous = set()
            for y in [y for y in years[years.index(year)-k: years.index(year)+1]]:
                previous.update(pc[y])
            unsungHeroes = set(core[year]).difference(previous)
            sr[year] = float(len(unsungHeroes)) / float(len(pc[year]))
        return sr
    
    