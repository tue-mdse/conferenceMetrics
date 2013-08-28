
root <- "/Users/bogdanv/github/conferenceMetrics/"
outPath <- "/Users/bogdanv/icse-harmful/grlz/camera-ready/figures/"

make_scatter_plot <- function(filename1, metric1, filename2, metric2, xmax, ymax){
  data1 <- read.csv(paste(root,"metrics/", filename1, ".csv", sep=""), sep=";")
  newnames <- c(names(data1)[1])
  for (name in names(data1[2:length(data1)])){
    newnames <- c(newnames, paste(name, "_1", sep=""))
  }
  names(data1) <- newnames
  
  data2 <- read.csv(paste(root,"metrics/", filename2, ".csv", sep=""), sep=";")
  newnames <- c(names(data2)[1])
  for (name in names(data2[2:length(data2)])){
    newnames <- c(newnames, paste(name, "_2", sep=""))
  }
  names(data2) <- newnames
  
  data <- merge(data1, data2)
  
  wide.confs = c("ICSE", "FSE", "ASE", "FASE")
  narrow.confs = c("MSR", "ICSM", "CSMR", "WCRE", "ICPC", "GPCE", "SCAM")
  
  wide.pch = 0
  narrow.pch = 20
  
  wide.lty = 1
  narrow.lty = 5
  
  wide.cex = 1.25
  narrow.cex = 1.75
  
  conferences = c("ASE", "CSMR", "FASE", "FSE", "GPCE", "ICPC", "ICSE", "ICSM", "MSR", "SCAM", "WCRE")
  colors = c("#332288", "#6699CC", "#88CCEE", "#661100", "#44AA99", "#117733", "#999933", "#DDCC77", "#CC6677", "#882255", "#AA4499")
    
  pdf(paste(outPath, paste(filename1,"_",filename2,sep=""),".pdf",sep=""), width=10, height=6)
  #content(xmax, ymax)
  
  #content <- function(xmax, ymax){
    par(mar=c(4,4,0,0), oma=c(0,0,0,0))   
    plot(data$year, type="n", xlim=c(0,xmax), ylim=c(0,ymax), axes=FALSE, xlab=metric1, ylab=metric2)
    # grid(NULL, NULL, col = "lightgray", lty = "dotted", lwd = 2, equilogs = FALSE)
    axis(1, at=c(0, xmax/4, xmax/2, 3*xmax/4, xmax))
#     axis(2, at=c(0, ymax/4, ymax/2, 3*ymax/4, ymax))
    axis(2, at=c(0, 0.25, 0.5, 0.75, 1))
    
    legend.lty = c()
    legend.pch = c()
    
    x = c()
    y = c()
    
    for (i in 1:length(conferences)){
      c = conferences[i]
      pch = ifelse(c %in% wide.confs, wide.pch, narrow.pch)
#       lty = ifelse(c %in% wide.confs, wide.lty, narrow.lty)
      lty = wide.lty
      cex = ifelse(c %in% wide.confs, wide.cex, narrow.cex)
      legend.lty = c(legend.lty, lty)
      legend.pch = c(legend.pch, pch)
      
      x = c(x, data[[paste(c,"_1", sep="")]])
      y = c(y, data[[paste(c,"_2", sep="")]])
      ct = cor.test(data[[paste(c,"_1", sep="")]], data[[paste(c,"_2", sep="")]])
      #print(names(ct))
      print(paste(conferences[i], ct$estimate, ct$p.value))
      #print(ct)
      
      points(data[[paste(c,"_1", sep="")]], data[[paste(c,"_2", sep="")]], 
             col=colors[i], pch=pch, bg=colors[i], cex=cex)    
    }
    
#     legend(0, ymax, conferences, cex=0.8, col=colors, lty=rep(1, length(conferences)), 
#            lwd=rep(10, length(conferences)), horiz=TRUE, bty="n")#, pch=plotchar)
    
    labels = c("ASE ", "CSMR ", "FASE ", "FSE ", "GPCE ", "ICPC ", "ICSE ", "ICSM ", "MSR ", "SCAM ", "WCRE ")    
    legend(0, (ymax), labels[1:6], cex=0.8, col=colors[1:6], lty=legend.lty[1:6], lwd=10, horiz=TRUE, bty="n")
    legend(0, (0.95*ymax), labels[7:11], cex=0.8, col=colors[7:11], lty=legend.lty[7:11], lwd=10, horiz=TRUE, bty="n")
#     , seg.len=2.9, lwd=3, lwd=3
  #}
  
  dev.off()
  
  print(cor.test(x,y))
  
}


# Inbreeding and PC turnover
make_scatter_plot("RAC0", "RAC(c,y,0)", "RNC1", "RNC(c,y,1)", 0.8, 1.1)

# Author turnover and PC turnover
# make_scatter_plot("NC1", "#NC(c,y,1)", "NA1", "#NA(c,y,1)", 50, 240)

