import sys
import pydot
import os

from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.accessibility import accessibility, connected_components
from pygraph.algorithms.critical import transitive_edges

# Output path
imgPath = os.path.abspath("/Users/bogdanv/icse-harmful/grlz/camera-ready/figures")

# Data input (manual)


def tldGraph(edgeList, dotPath, aspectRatio):
	# Graph creation
	gr = digraph()

	# Compute nodes from list of edges
	nodes = set()
	for edge in edgeList:
		nodes.add(edge[0])
		nodes.add(edge[1])

	# Add nodes to graph
	gr.add_nodes(list(nodes))

	# Add edges to graph
	for edge in edgeList:
		gr.add_edge(edge)

	# Compute transitive edges
	tr = transitive_edges(gr)

	# Only display non-transitive edges
	ntrEdges = set(list(edgeList)).difference(set(tr))

	# Visualization
	dgr = pydot.Dot(graph_type='digraph')
	dgr.set_ranksep(0.2)
	dgr.set_nodesep(0.05)
	# dgr.set_ratio(1)
	dgr.set_ratio(aspectRatio)
	dgr.set_margin(0)
	# dgr.set_aspect(1) # AW < 14
	dgr.set_node_defaults(fontname="Arial")

	for edge in ntrEdges:
		dgr.add_edge(pydot.Edge(edge[0], edge[1]))

	# Draw as PDF
	dgr.write_pdf(dotPath)


# SP(c,y)
edgeList = [("ASE", "CSMR"), ("ASE", "FASE"), ("ASE", "GPCE"), ("ASE", "ICPC"), ("ASE", "MSR"), \
		("ASE", "SCAM"), ("ASE", "WCRE"), ("CSMR", "SCAM"), ("FASE", "GPCE"), ("FASE", "ICPC"), \
		("FASE", "SCAM"), ("FSE", "GPCE"), ("FSE", "ICPC"), ("FSE", "MSR"), ("FSE", "SCAM"), \
		("FSE", "WCRE"), ("ICSE", "ICSM"), ("ICSE", "MSR"), ("ICSE", "SCAM"), ("ICSE", "WCRE"), \
		("ICSM", "MSR"), ("ICSM", "SCAM"), ("ICSM", "WCRE"), ("ICSE", "ASE"), ("FSE", "CSMR"), \
		("ICSE", "CSMR"), ("ICSM", "CSMR"), ("FSE", "FASE"), ("ICSE", "FASE"), ("ICSE", "FSE"), \
		("ICSE", "GPCE"), ("ICSM", "GPCE"), ("ICSE", "ICPC"), ("ICSM", "ICPC"), ("WCRE", "SCAM")]
dotPath = os.path.join(imgPath, "tilde_sp.pdf")
tldGraph(edgeList, dotPath, 1)


# C(c,y)
edgeList = [("ASE", "FASE"), ("ASE", "FSE"), ("ASE", "GPCE"), ("CSMR", "FASE"), ("CSMR", "FSE"), \
		("CSMR", "GPCE"), ("ICSM", "MSR"), ("ICSM", "SCAM"), ("ICSM", "WCRE"), ("ICSM", "ASE"), \
		("ICPC", "FASE"), ("ICSE", "FASE"), ("ICSM", "FASE"), ("SCAM", "FASE"), ("WCRE", "FASE"), \
		("ICPC", "FSE"), ("ICSE", "FSE"), ("ICSM", "FSE"), ("SCAM", "FSE"), ("WCRE", "FSE"), \
		("ICPC", "GPCE"), ("ICSE", "GPCE"), ("ICSM", "GPCE"), ("SCAM", "GPCE"), ("WCRE", "GPCE"), \
		("ICSM", "ICPC"), ("ICSM", "ICSE")]
dotPath = os.path.join(imgPath, "tilde_numPC.pdf")
tldGraph(edgeList, dotPath, 0.75)

# RL(c,y)
edgeList = [("ASE", "CSMR"), ("ASE", "ICPC"), ("ASE", "ICSM"), ("ASE", "MSR"), ("ASE", "SCAM"), \
		("ASE", "WCRE"), ("CSMR", "SCAM"), ("FASE", "GPCE"), ("FASE", "ICPC"), ("FASE", "ICSM"), \
		("FASE", "MSR"), ("FASE", "SCAM"), ("FASE", "WCRE"), ("FSE", "GPCE"), ("FSE", "ICPC"), \
		("FSE", "ICSM"), ("FSE", "MSR"), ("FSE", "SCAM"), ("FSE", "WCRE"), ("GPCE", "ICPC"), \
		("GPCE", "MSR"), ("GPCE", "SCAM"), ("ICSE", "ICSM"), ("ICSE", "MSR"), ("ICSE", "SCAM"), \
		("ICSE", "WCRE"), ("ICSM", "MSR"), ("ICSM", "SCAM"), ("ICSE", "ASE"), ("FASE", "CSMR"), \
		("FSE", "CSMR"), ("ICSE", "CSMR"), ("ICSE", "FASE"), ("ICSE", "GPCE"), ("ICSE", "ICPC"), \
		("ICSM", "ICPC"), ("WCRE", "SCAM")]
dotPath = os.path.join(imgPath, "tilde_rl.pdf")
tldGraph(edgeList, dotPath, 1)

# RNC(c,y,1)
edgeList = [("FASE", "ICPC"), ("FASE", "ICSM"), ("FASE", "MSR"), ("FASE", "SCAM"), ("FASE", "WCRE"), \
		("FSE", "ICPC"), ("FSE", "ICSM"), ("FSE", "MSR"), ("FSE", "SCAM"), ("FSE", "WCRE"), \
		("GPCE", "ICPC"), ("GPCE", "ICSM"), ("GPCE", "MSR"), ("GPCE", "SCAM"), ("GPCE", "WCRE"), \
		("ICSE", "ICSM"), ("ICSE", "MSR"), ("ICSE", "SCAM"), ("ICSE", "WCRE"), ("FASE", "ASE"), \
		("FSE", "ASE"), ("GPCE", "ASE"), ("ICSE", "ASE"), ("FASE", "CSMR"), ("FSE", "CSMR"), \
		("GPCE", "CSMR"), ("ICSE", "CSMR"), ("ICSE", "ICPC")]
dotPath = os.path.join(imgPath, "tilde_rnc1.pdf")
tldGraph(edgeList, dotPath, 1)

# RNA(c,y,4)
edgeList = [("ASE", "ICPC"), ("ASE", "ICSM"), ("FASE", "ICPC"), ("FASE", "ICSE"), ("FASE", "ICSM"), \
		("FASE", "WCRE")]
dotPath = os.path.join(imgPath, "tilde_rna4.pdf")
tldGraph(edgeList, dotPath, 1)

# RPNA(c,y,4) - openness
edgeList = [("ASE", "WCRE"), ("FASE", "ICPC"), ("FASE", "ICSE"), ("FASE", "ICSM"), ("FASE", "MSR"), \
		("FASE", "WCRE"), ("SCAM", "WCRE"), ("SCAM", "ICPC")]
dotPath = os.path.join(imgPath, "tilde_rpna4.pdf")
tldGraph(edgeList, dotPath, 1)

# RAC(c,y,0) - introversion
edgeList = [("ASE", "FASE"), ("CSMR", "FASE"), ("CSMR", "FSE"), ("ICPC", "ICSE"), ("ICPC", "ASE"), \
		("ICSM", "ASE"), ("MSR", "ASE"), ("WCRE", "ASE"), ("ICPC", "CSMR"), ("MSR", "CSMR"), \
		("WCRE", "CSMR"), ("ICPC", "FASE"), ("ICSE", "FASE"), ("ICSM", "FASE"), ("MSR", "FASE"), \
		("SCAM", "FASE"), ("WCRE", "FASE"), ("ICPC", "FSE"), ("ICSM", "FSE"), ("MSR", "FSE"), \
		("SCAM", "FSE"), ("WCRE", "FSE"), ("ICPC", "GPCE"), ("ICSM", "GPCE"), ("MSR", "GPCE"), \
		("SCAM", "GPCE"), ("WCRE", "GPCE"), ("ICSM", "ICSE"), ("MSR", "ICSE"), ("SCAM", "ICSE"), \
		("WCRE", "ICSE")]
dotPath = os.path.join(imgPath, "tilde_rac0.pdf")
tldGraph(edgeList, dotPath, 1)

# RCnA(c,y,4) - representativeness of PC
edgeList = [("ASE", "ICPC"), ("ASE", "ICSM"), ("ASE", "MSR"), ("ASE", "WCRE"), ("CSMR", "ICPC"), \
		("CSMR", "ICSM"), ("CSMR", "MSR"), ("CSMR", "WCRE"), ("FASE", "ICPC"), ("FASE", "ICSM"), \
		("FASE", "MSR"), ("FASE", "WCRE"), ("FSE", "ICPC"), ("FSE", "ICSM"), ("FSE", "MSR"), \
		("FSE", "WCRE"), ("GPCE", "MSR"), ("GPCE", "WCRE"), ("ICSE", "MSR"), ("ICSE", "WCRE"), \
		("ICSM", "MSR"), ("ICSM", "WCRE")]
dotPath = os.path.join(imgPath, "tilde_rcna4.pdf")
tldGraph(edgeList, dotPath, 1)

# SR4 - sustainability ratio
edgeList = [("FASE", "ICPC"), ("FASE", "SCAM"), ("FSE", "SCAM"), ("ICSE", "ICSM"), ("ICSE", "MSR"), \
		("ICSE", "SCAM"), ("ICSE", "WCRE"), ("ICSM", "SCAM"), ("ICSE", "ASE"), ("ICSE", "CSMR"), \
		("ICSE", "ICPC")]
dotPath = os.path.join(imgPath, "tilde_sr4.pdf")
tldGraph(edgeList, dotPath, 0.5)



# ---------------------
# dot = write(gr)
# gvv = gv.readstring(dot)
# gv.layout(gvv,'dot')
# gv.render(gvv,'png','europe.png')