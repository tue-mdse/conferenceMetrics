# Metrics

The Python script `metrics.py` defines a metrics model and how to compute the metrics (see the tools folder). To account for differences in conference age, we use sliding window metrics. The following metrics have been implemented (*c* denotes a conference, *y* a year) in `metrics.py`, and the results are available in this folder. We use these metrics to assess the *health* of software engineering conferences in [this preprint](http://www.win.tue.nl/mdse/conferences/SCP13.pdf) submitted to Science of Computer Programming.

- *A(c,y)*, **number of Authors**
- *C(c,y)*, **number of programme Committee members**
- *AP(c,y)*, **number of Accepted Papers**
- *SP(c,y)*, **number of Submitted Papers**
- *RA(c,y)*, **acceptance rate**: *AP(c,y) / SP(c,y)*
- *RL(c,y)*, **Reviewer Load**: *SP(c,y) / C(c,y)*
- *RNA(c,y,k)*, **author turnover (Ratio of New Authors)**: fraction of authors at conference *c* in year *y* that have not been author between *y-k* and *y-1*
- *RNC(c,y,k)*, **programme committee turnover (Ratio of New programme Committee members)**: fraction of PC of *c* in year *y* that have not served on the PC between *y-k* and *y-1*
- *APC(c,y,k)*, **number of Accepted PC papers**: number of papers at *c* in year *y* co-authored by PC members from *y-k* to *y*
- *RAC(c,y,k)*, **inbreeding ratio (Ratio Accepted programme Committee papers)**: fraction of papers published at *c* in year *y* co-authored by PC members from *y-k* to *y*
- *CnA(c,y,k)*, **program Committee members never Authors**: number of PC members in year *y* that have never been authors at *c* between *y-k* and *y-1* (can serve as a measure of the **representativeness** of the PC with respect to the author community)
- *RCnA(c,y,k)*, **wild-card ratio**: the fraction of PC members in year *y* that have never been authors at *c* between *y-k* and *y-1*
- *PNA(c,y,k)*, **Papers by New Authors**: number of papers published in year *y* for which none of the co-authors has ever published at *c* between *y-k* and *y-1*
- *RPNA(c,y,k)*, **openness ratio**: fraction of papers published in year *y* for which none of the co-authors has ever published at *c* between *y-k* and *y-1*

