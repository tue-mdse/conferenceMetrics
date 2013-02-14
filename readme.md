# Bibliometrics for software engineering conferences
---

### Contents

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

The data is stored in a MySQL database (see the [SQL dump](https://github.com/tue-mdse/conferenceMetrics/blob/master/data/conferences.sql.gz)) with the following schema:

<img align="center" width="90%" src="https://raw.github.com/tue-mdse/conferenceMetrics/master/visualisation/model.png">

Alternatively, the database can be recreated (hence easily extended) from CSV files using Python and the SQLAlchemy Object Relational Mapper using the scripts included (more details below).

### Data provenance

- Papers and authors: the [DBLP](http://www.dblp.org/db/) data dump. Papers which were part of the main (research) track have been (manually) marked as such in the `main_track` column. The conference impact factor (the `impact` column from the `conferences` table) is the [SHINE h-index](http://shine.icomp.ufam.edu.br/index.php) for the period 2000-2012.
- Number of submssions: Tao Xie's [software engineering conference statistics](http://people.engr.ncsu.edu/txie/seconferences.htm); foreword to proceedings.
- Composition of programme committee: conference websites, only programme committee members for the main tracks have been included. Disambiguation was performed to align the spelling used on the different websites to that found in DBLP.

In some cases the DBLP data also contains the session title(s) for a given paper. For example, for [papers published at ICSE 2012](http://www.informatik.uni-trier.de/~ley/db/conf/icse/icse2012.html), a session title (such as `Technical Research`, originally encoded as an HTML `h2` header and recorded in the `session_h2` column) and a session subtitle (such as `Fault Handling`, originally encoded as an HTML `h3` header and recorded in the `session_h3` column) is available. When available, such titles could be used to automatically filter papers if so desired for a certain bibliometric analysis.

## Using the database

Most simply, you can import the [SQL dump](https://github.com/tue-mdse/conferenceMetrics/blob/master/data/conferences.sql.gz) into your favourite database management system (tested on MySQL) and start querying.

Alternatively, you can take a look at how the database was created using MySQL, Python and SQLAlchemy, and use these mechanisms also for querying. This will allow you to easily extend the database or update its schema. This assumes you have a MySQL server running, and SQLAlchemy installed.

Python scripts:

- `initDB.py`: declares the database schema using Python classes (will be automatically mapped to tables by SQLAlchemy).
- `populateDB.py`: reads data about the papers and programme committees for each conference and loads it into the database.
- `metrics.py`: defines a metrics model and how to compute the metrics. To account for the different ages of the conferences, we use sliding window metrics. For example,
	- author turnover *RNA(c,y,k)*: fraction of authors at conference *c* in year *y* that have not been author between *y-k* and *y-1*.
	- programme committee turnover *RNC(c,y,k)*: fraction of PC of *c* in year *y* that have not served on the PC between *y-k* and *y-1*.
	- *inbreeding* ratio *RAC(c,y,k)*: fraction of papers published at *c* in year *y* co-authored by PC members from *y-k* to *y*.
  
   For a complete list of metrics check [this list](https://github.com/tue-mdse/conferenceMetrics/blob/master/metrics/metrics.md), or see [this preprint](http://www.win.tue.nl/mdse/conferences/SCP13.pdf).
- `queryDB.py`: queries the database, computes the metrics defined in the metrics model, and outputs the results to CSV files. For an example of a visualisation of these results, we include the `visualisation.r` R script that produces the following plot for *RAC(c,y,0)*, the fraction of papers each year co-authored by PC members from that year.

<img align="center" width="100%" src="https://raw.github.com/tue-mdse/conferenceMetrics/master/visualisation/RAC0.png">
