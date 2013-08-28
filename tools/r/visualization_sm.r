
root <- "/Users/bogdanv/github/conferenceMetrics/"
outPath <- "/Users/bogdanv/icse-harmful/grlz/camera-ready/figures/"

source("/Users/bogdanv/github/conferenceMetrics/tools/r/miniPlot.r")

genPlot <- function(metric, pdfname, root, outPath, ylim, maxy, ylab, axis2, legendy, cex, startLine, underLineWidth){
  data <- read.csv(paste(root,"metrics/", metric, ".csv", sep=""), sep=";")
  
  pdf(paste(outPath, pdfname, sep=""), width=13, height=7)
  
  layout(matrix(c(1,1,1,2,1,1,1,3,1,1,1,4,5,6,7,8,9,10,11,12), 5, 4, byrow = TRUE))
  par(mar=c(2,1,2,1))
  par(oma=c(1,1,0,1))
  
  trends(root, metric, ylab, ylim, axis2, legendy, cex)
  
#   conferences = c("ASE", "CSMR", "FASE", "FSE", "GPCE", "ICPC", "ICSE", "ICSM", "MSR", "SCAM", "WCRE")
  
  miniPlot(data, "ASE", maxy, colors[1], startLine, underLineWidth, axis2)
  miniPlot(data, "CSMR", maxy, colors[2], startLine, underLineWidth, axis2)
  miniPlot(data, "FASE", maxy, colors[3], startLine, underLineWidth, axis2)
  miniPlot(data, "FSE", maxy, colors[4], startLine, underLineWidth, axis2)
  miniPlot(data, "GPCE", maxy, colors[5], startLine, underLineWidth, axis2)
  miniPlot(data, "ICPC", maxy, colors[6], startLine, underLineWidth, axis2)
  miniPlot(data, "ICSE", maxy, colors[7], startLine, underLineWidth, axis2)
  miniPlot(data, "ICSM", maxy, colors[8], startLine, underLineWidth, axis2)
  miniPlot(data, "MSR", maxy, colors[9], startLine, underLineWidth, axis2)
  miniPlot(data, "SCAM", maxy, colors[10], startLine, underLineWidth, axis2)
  miniPlot(data, "WCRE", maxy, colors[11], startLine, underLineWidth, axis2)
  
  dev.off()
  
}

colors = c("#332288", "#6699CC", "#88CCEE", "#661100", "#44AA99", "#117733", "#999933", "#DDCC77", "#CC6677", "#882255", "#AA4499")

genPlot("C", "sm_numPC_2013.pdf", root, outPath, c(0,100), 100, "#C(c,y)", c(0, 25, 50, 75, 100), 105, 1.5, 10, 6)
genPlot("SP", "sm_SP_2013.pdf", root, outPath, c(0,550), 500, "#SP(c,y)", c(0, 100, 200, 300, 400, 500), 550, 1.5, 8.5, 6)
genPlot("RL", "sm_RL_2013.pdf", root, outPath, c(0,13), 13, "RL(c,y)", c(0, 3, 6, 9, 12), 13, 1.5, 8.5, 6)
genPlot("RNC1", "sm_RNC1_2013.pdf", root, outPath, c(0,1.1), 1, "RNC(c,y,1)", c(0, 0.25, 0.50, 0.75, 1), 1.15, 1.5, 9, 6)
genPlot("RNA4", "sm_RNA4_2013.pdf", root, outPath, c(0,1.1), 1, "RNA(c,y,4)", c(0, 0.25, 0.50, 0.75, 1), 1.15, 1.5, 7.5, 6)
genPlot("RPNA4", "sm_RPNA4_2013.pdf", root, outPath, c(0,1.1), 1, "RPNA(c,y,4)", c(0, 0.25, 0.50, 0.75, 1), 1.15, 1.5, 7.5, 6)
genPlot("RAC0", "sm_RAC0_2013.pdf", root, outPath, c(0,1), 1, "RAC(c,y,0)", c(0, 0.25, 0.50, 0.75, 1), 1.01, 1.5, 10, 6)
genPlot("RCnA4", "sm_RCnA4_2013.pdf", root, outPath, c(0,1), 1, "RCnA4(c,y,0)", c(0, 0.25, 0.50, 0.75, 1), 1.01, 1.5, 7.5, 6)
genPlot("SR4", "sm_SR4_2013.pdf", root, outPath, c(0,2.5),2.5, "SR(c,y,4)", c(0, 0.5, 1, 1.5, 2), 2.5, 1.5, 7, 5.8)


