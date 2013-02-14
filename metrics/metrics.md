# Metrics

The Python script `metrics.py` defines a metrics model and how to compute the metrics (see the tools folder). To account for differences in conference age, we use sliding window metrics. The following have been implemented:

- author turnover *RNA(c,y,k)*: fraction of authors at conference *c* in year *y* that have not been author between *y-k* and *y-1*.
- programme committee turnover *RNC(c,y,k)*: fraction of PC of *c* in year *y* that have not served on the PC between *y-k* and *y-1*.
- *inbreeding* ratio *RAC(c,y,k)*: fraction of papers published at *c* in year *y* co-authored by PC members from *y-k* to *y*.
