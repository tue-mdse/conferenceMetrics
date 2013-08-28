
linesNoDots <- function(root, filename, metric, ylim, axis2, legendy, hline=FALSE){
  data = read.csv(paste(root, "metrics/", filename, ".csv", sep=""), sep=";")
  
  wide.confs = c("ICSE", "FSE", "ASE", "FASE")
  narrow.confs = c("MSR", "ICSM", "CSMR", "WCRE", "ICPC", "GPCE", "SCAM")
  
  wide.pch = 0
  narrow.pch = 20
  
  wide.lty = 1
  narrow.lty = 5
    
  conferences = c("ASE", "CSMR", "FASE", "FSE", "GPCE", "ICPC", "ICSE", "ICSM", "MSR", "SCAM", "WCRE")
  colors = c("#332288", "#6699CC", "#88CCEE", "#661100", "#44AA99", "#117733", "#999933", "#DDCC77", "#CC6677", "#882255", "#AA4499")
  # colors <- c(colors()[55], colors()[27], colors()[33], colors()[90], colors()[81], 
  #     colors()[31], colors()[121], colors()[142], colors()[50], colors()[36], colors()[12])
  
  pdf(paste(root,"visualisation/",filename,".pdf",sep=""), width=9, height=6)

  par(mar=c(2,4,0,0), oma=c(0,0,0,0))   
  plot(data$year, type="n", xlim=c(min(data$year), max(data$year)), ylim=ylim, axes=FALSE, xlab="", ylab=metric)

  axis(1, at=data$year, xlab="")
  axis(2, at=axis2)
  if (hline){
    abline(h=1, col="gray", lty=2)
  }
  
  legend.lty = c()
  
  for (i in 1:length(conferences)){
    c = conferences[i]
    pch = ifelse(c %in% wide.confs, wide.pch, narrow.pch)
    lty = ifelse(c %in% wide.confs, wide.lty, narrow.lty)
    legend.lty = c(legend.lty, lty)
    
    lines(data$year, data[[c]], type="l", lwd=2, lty=lty, col=colors[i], 
          pch=pch, bg=colors[i], cex=1.25)
  }  
  
  legend(min(data$year), legendy, conferences[1:6], cex=0.8, col=colors[1:6], lty=legend.lty[1:6], lwd=3, seg.len=4, horiz=TRUE, bty="n")
  legend(min(data$year), (0.95*legendy), conferences[7:11], cex=0.8, col=colors[7:11], lty=legend.lty[7:11], lwd=3, seg.len=4, horiz=TRUE, bty="n")

  dev.off()
  
}
