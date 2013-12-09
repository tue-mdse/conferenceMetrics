# List of edges for the ~T graphs, and results of wide-narrow comparison

#metric = "C"

root <- "/Users/bogdanv/github/conferenceMetrics/"
outPath <- "/Users/bogdanv/icse-harmful/grlz/camera-ready/graphs/"

analysis <- function(metric){
  metrics <- read.csv(paste(root, "metrics/", metric, ".csv", sep=""), sep=";")
  #metrics <- na.omit(metrics)
  
  icse <- metrics$ICSE[is.na(metrics$ICSE) == FALSE]
  icsm <- metrics$ICSM[is.na(metrics$ICSM) == FALSE]
  csmr <- metrics$CSMR[is.na(metrics$CSMR) == FALSE]
  wcre <- metrics$WCRE[is.na(metrics$WCRE) == FALSE]
  icpc <- metrics$ICPC[is.na(metrics$ICPC) == FALSE]
  fse <- metrics$FSE[is.na(metrics$FSE) == FALSE]
  fase <- metrics$FASE[is.na(metrics$FASE) == FALSE]
  ase <- metrics$ASE[is.na(metrics$ASE) == FALSE]
  gpce <- metrics$GPCE[is.na(metrics$GPCE) == FALSE]
  msr <- metrics$MSR[is.na(metrics$MSR) == FALSE]
  scam <- metrics$SCAM[is.na(metrics$SCAM) == FALSE]
  
  # Combined samples
  # ----------------
  v <- c(icse, icsm, csmr, wcre, icpc, fse, fase, ase, gpce, msr, scam)
  #length(v)
  
  # Tag each element
  # ------------------
  lblICSE <- rep("ICSE", length(icse))
  lblICSM <- rep("ICSM", length(icsm))
  lblCSMR <- rep("CSMR", length(csmr))
  lblWCRE <- rep("WCRE", length(wcre))
  lblICPC <- rep("ICPC", length(icpc))
  lblFSE <- rep("FSE", length(fse))
  lblFASE <- rep("FASE", length(fase))
  lblASE <- rep("ASE", length(ase))
  lblGPCE <- rep("GPCE", length(gpce))
  lblMSR <- rep("MSR", length(msr))
  lblSCAM <- rep("SCAM", length(scam))
  
  # Combined tags
  # ---------------
  lbl <- c(lblICSE, lblICSM, lblCSMR, lblWCRE, 
           lblICPC, lblFSE, lblFASE, lblASE, 
           lblGPCE, lblMSR, lblSCAM)
  #length(lbl)
  
  # Data frame
  # ----------
  data <- data.frame(v, lbl)
  
  source(paste(root, "tools/r/mctp.r", sep=""))
  
  res <- mctp(data$v~data$lbl, data=data, type="Tukey", asy.method="fisher")
  #res$Analysis # This produces the tables with p-values in the appendix
  
  #head(res$Analysis)
  #head(rownames(res$Analysis))
  
  filename = paste(outPath, "tld_edges_", metric, ".csv", sep="")
  
  s_xy <- subset(res$Analysis, Upper < 0)
  names <- strsplit(rownames(s_xy), " - ")
  if (length(names) > 0){
    for (i in 1:length(names)){
      cat(paste("(\"",names[[i]][2],"\",",sep=""), paste("\"",names[[i]][1],"\")",sep=""), "\n")
      cat(paste(names[[i]][2],names[[i]][1],sep=";"), file=filename, sep="\n", append=TRUE)
    }
  }
  
  s_yx <- subset(res$Analysis, Lower > 0)
  names <- strsplit(rownames(s_yx), " - ")
  if (length(names) > 0){
    for (i in 1:length(names)){
      cat(paste("(\"",names[[i]][1],"\",",sep=""), paste("\"",names[[i]][2],"\")",sep=""), "\n")
      cat(paste(names[[i]][1],names[[i]][2],sep=";"), file=filename, sep="\n", append=TRUE)
    }
  }
  
}

wideVsNarrow <- function(metric){
  metrics <- read.csv(paste(root,"metrics/", metric, ".csv", sep=""), sep=";")
  #metrics <- na.omit(metrics)
  
  icse <- metrics$ICSE[is.na(metrics$ICSE) == FALSE]
  icsm <- metrics$ICSM[is.na(metrics$ICSM) == FALSE]
  csmr <- metrics$CSMR[is.na(metrics$CSMR) == FALSE]
  wcre <- metrics$WCRE[is.na(metrics$WCRE) == FALSE]
  icpc <- metrics$ICPC[is.na(metrics$ICPC) == FALSE]
  fse <- metrics$FSE[is.na(metrics$FSE) == FALSE]
  fase <- metrics$FASE[is.na(metrics$FASE) == FALSE]
  ase <- metrics$ASE[is.na(metrics$ASE) == FALSE]
  gpce <- metrics$GPCE[is.na(metrics$GPCE) == FALSE]
  msr <- metrics$MSR[is.na(metrics$MSR) == FALSE]
  scam <- metrics$SCAM[is.na(metrics$SCAM) == FALSE]
  
  wide <- c(icse, fse, ase, fase)
  narrow <- c(icsm, wcre, icpc, csmr, gpce, msr, scam)
  all <- c(wide, narrow)
  
  lblWide <- rep("wide", length(wide))
  lblNarrow <- rep("narrow", length(narrow))
  lblA <- c(lblWide, lblNarrow)
  d <- data.frame(all, lblA)
  head(d)
  
  library(nparcomp)
  res <- npar.t.test(all~lblA, data = d, alternative = "two.sided")
  res$Analysis
}

analysis("SP")
analysis("C")
analysis("RL")
analysis("RNC1")
analysis("RNA4")
analysis("RPNA4")
analysis("RAC0")
analysis("RCnA4")
analysis("SR4")
# analysis("numPC")
# analysis("RCAnPC4b")

wideVsNarrow("SP")
wideVsNarrow("C")
wideVsNarrow("RL")
wideVsNarrow("RNC1")
wideVsNarrow("RNA4")
wideVsNarrow("RPNA4")
wideVsNarrow("RAC0")
wideVsNarrow("RCnA4")
wideVsNarrow("SR4")
# wideVsNarrow("RCAnPC4b")
