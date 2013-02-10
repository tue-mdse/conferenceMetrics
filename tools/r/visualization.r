
root <- "../../"

make_plot <- function(filename, metric, ylim, axis2, legendy, hline=FALSE){
  data <- read.csv(paste(root,"metrics/", filename, ".csv", sep=""), sep=";")
  # head(data)
  
  conferences <- c("MSR", "ICSM", "ICSE", "CSMR", "WCRE", "ICPC", "FSE", "FASE", "ASE", "GPCE", "SCAM")
  colors <- c(colors()[55], colors()[27], colors()[33], colors()[90], colors()[81], colors()[31], colors()[121],
              colors()[142], colors()[50], colors()[36], colors()[12])
  #plotchar <- c(15, 0, 16, 17, 23, 1, 2, 5, 25)
  #plotchar <- c(17, 0, 17, 17, 17, 0, 0, 0, 17)
  #plotchar <- c(20, 20, 0, 20, 20, 20, 0, 0, 0, 20, 20)
  plotchar <- c(20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20)
  
  content <- function(ylim, axis2, legendy){
    par(mar=c(2,4,0,0), oma=c(0,0,0,0))   
    plot(data$year, type="n", xlim=c(min(data$year), max(data$year)), ylim=ylim, axes=FALSE, xlab="", ylab=metric)
    # grid(NULL, NULL, col = "lightgray", lty = "dotted", lwd = 2, equilogs = FALSE)
    axis(1, at=data$year, xlab="")
    axis(2, at=axis2)
    if (hline){
      abline(h=1, col="gray", lty=2)
    }
    for (i in 1:length(conferences)){
      lines(data$year, data[[conferences[i]]], type="b", lwd=1.5, lty=1, col=colors[i], 
            pch=plotchar[i], bg=colors[i], cex=1.25)
      cat(paste(conferences[i], mean(data[[conferences[i]]], na.rm=TRUE),sep=" "), "\n")
    }
    cat("\n")
    legend(min(data$year), legendy, conferences, cex=0.8, col=colors, lty=rep(1, length(conferences)), 
           lwd=rep(10, length(conferences)), horiz=TRUE, bty="n")#, pch=plotchar)
    
  }
  
  pdf(paste(root,"visualisation/",filename,".pdf",sep=""), width=12, height=6)
  content(ylim, axis2, legendy)
  dev.off()
  
  png(paste(root,"visualisation/",filename,".png",sep=""), width=12, height=6, units="in", res=200)#, pointsize=1)
  content(ylim, axis2, legendy)
  dev.off()
}

# PC turnover
make_plot("RNC1", "RNC(c,y,1)", c(0,1), c(0, 0.25, 0.50, 0.75, 1), 1.01)
make_plot("RNC4", "RNC(c,y,4)", c(0,1), c(0, 0.25, 0.50, 0.75, 1), 1.01)

# Author turnover
make_plot("RNA1", "RNA(c,y,1)", c(0,1), c(0, 0.25, 0.50, 0.75, 1), 1.01)
make_plot("RNA4", "RNA(c,y,4)", c(0,1), c(0, 0.25, 0.50, 0.75, 1), 1.01)

# Representativeness of PC
make_plot("RCnA4", "RCnA(c,y,4)", c(0,1), c(0, 0.25, 0.50, 0.75, 1), 1.01)

# Openness
make_plot("RPNA4", "RPNA(c,y,4)", c(0,1), c(0, 0.25, 0.50, 0.75, 1), 1.01)

# Inbreeding
make_plot("RAC0", "RAC(c,y,0)", c(0,1), c(0, 0.25, 0.50, 0.75, 1), 1.01)

# Number of PC members
make_plot("C", "#C(c,y)", c(0,100), c(0, 25, 50, 75, 100), 101)

# Submissions
make_plot("SP", "#SP(c,y)", c(0,500), c(0, 100, 200, 300, 400, 500), 500)

# Review load
make_plot("RL", "RL(c,y)", c(0,12), c(0, 3, 6, 9, 12), 12)

