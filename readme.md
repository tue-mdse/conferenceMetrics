#Bibliometrics for software engineering conferences#
===

###Contents###

This is a database of papers and programme committee members for software engineering conferences. It contains more than ten years of history for each of the following conferences:

- **ICSE**, International Conference on Software Engineering
- **ICSM**, IEEE International Conference on Software Maintenance
- **ASE**, IEEE/ACM International Conference on Automated Software Engineering
- **FSE**, ACM SIGSOFT Symposium on the Foundations of Software Engineering
- **FASE**, International Conference on Fundamental Approaches to Software Engineering
- **MSR**, Working Conference on Mining Software Repositories
- **WCRE**, Working Conference on Reverse Engineering
- **CSMR**, European Conference on Software Maintenance and Reengineering
- **GPCE**, Generative Programming and Component Engineering
- **ICPC**, IEEE International Conference on Program Comprehension
- **SCAM**, International Working Conference on Source Code Analysis & Manipulation

The data is stored in a MySQL database (see the [SQL dump](https://github.com/tue-mdse/conferenceMetrics/blob/master/conferences_dblp.sql.gz)) with the following schema:

<img align="center" width="100%" src="https://raw.github.com/tue-mdse/conferenceMetrics/master/model.png">

Alternatively, the database can be recreated (hence easily extended) from CSV files using Python and the SQLAlchemy Object Relational Mapper using the scripts included (more details below).

###Data provenance###

- Papers and authors: the [DBLP](http://www.dblp.org/db/) data dump. Papers which were part of the main (research) track have been (manually) marked as such in the `main_track` column. 
- Number of submssions: Tao Xie's [software engineering conference statistics](http://people.engr.ncsu.edu/txie/seconferences.htm); foreword to proceedings.
- Composition of programme committee: conference websites (disambiguation was performed to align the spelling used on the different websites to that found in DBLP).

In some cases the DBLP data also contains the session title(s) for a given paper. For example, for [papers published at ICSE 2012](http://www.informatik.uni-trier.de/~ley/db/conf/icse/icse2012.html), a session title (such as `Technical Research`, originally encoded as an HTML `h2` header and recorded in the `session_h2` column) and a session subtitle (such as `Fault Handling`, originally encoded as an HTML `h3` header and recorded in the `session_h3` column) is available. When available, such titles could be used to automatically filter out papers if so desired for a certain bibliometric analysis.






