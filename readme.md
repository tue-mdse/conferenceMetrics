Bibliometrics for software engineering conferences
==============================================================

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

Alternatively, the database can be recreated (hence easily extended) from CSV files using Python and the SQLAlchemy Object Relational Mapper using the scripts included.

Data provenance:

- Papers and authors: the [DBLP](http://www.dblp.org/db/) data dump. Papers which were part of the main (research) track have been (manually) marked as such in the `main_track` column.
- Number of submssions: Tao Xie's [software engineering conference statistics](http://people.engr.ncsu.edu/txie/seconferences.htm); foreword to proceedings.
- Composition of programme committee: conference websites (disambiguation was performed to align the spelling used on the different websites to that found in DBLP).





