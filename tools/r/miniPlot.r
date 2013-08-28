
miniPlot = function(data, conference, ymax, titlecol, startLine, underLineWidth, axis2sm){
  vals = data.frame(year=data$year, val=data[[conference]])
  d2 = data
  d2$year = NULL
  
  nColors = 12
  
  years = as.character(rev(data$year))
#   m = max(vals$val, na.rm=T)
  m = max(d2, na.rm=T)
  colorWidth = m/nColors
  
  #   d3 = data.frame(matrix(ncol = length(years), nrow = m))
  d3 = data.frame(matrix(ncol = length(years), nrow = nColors))
  names(d3) = years
  for (col in 1:length(d3)){
    y = as.numeric(years[col])
    row = which(vals$year==y)
    v = vals$val[row]
    if (is.na(v)){
#       r = rep(NA, m)
      r = rep(NA, nColors)
    }else{
#       r = c(rep(1, v), rep(NA, (m-v)))
      if (m>3){
        fullParts = rep(colorWidth, floor(v/colorWidth))
        rest = v-(colorWidth * floor(v/colorWidth))
      
        if (rest != 0){
          r = c(fullParts, rest, rep(NA, (nColors-length(fullParts)-1)))
        }else{
          r = c(fullParts, rep(NA, (nColors-length(fullParts))))
        }
      }else{
        v2 = v*100
        c2 = colorWidth * 100
        fullParts = rep(c2, floor(v2/c2))
        rest = v2-(c2 * floor(v2/c2))
        
        if (rest != 0){
          r = c(fullParts/100, rest/100, rep(NA, (nColors-length(fullParts)-1)))
        }else{
          r = c(fullParts/100, rep(NA, (nColors-length(fullParts))))
        }
      }
      
    }
    d3[[col]] = r
  }
  
  wide.confs = c("ICSE", "FSE", "ASE", "FASE")
  narrow.confs = c("MSR", "ICSM", "CSMR", "WCRE", "ICPC", "GPCE", "SCAM")
  
  wide.lty = 1
  narrow.lty = 5
  lty = ifelse(conference %in% wide.confs, wide.lty, narrow.lty)
  
  colfunc = colorRampPalette(c("#E5F5E0", "#004A02"))
  
  #   bp = barplot(rev(vals$val), axes=F, ylim=c(0,ymax), main=conference, col=heat.colors(7))
  #   bp = barplot(as.matrix(d3), axes=F, ylim=c(0,ymax), main=conference, col=heat.colors(75), border=NA)
  #   bp = barplot(as.matrix(d3), axes=F, ylim=c(0,ymax), main=conference, col=rainbow(90,start=.7,end=.1), border=NA)
  #   bp = barplot(as.matrix(d3), axes=F, ylim=c(0,ymax), main=conference, col=cm.colors(nColors), border=NA)
  bp = barplot(as.matrix(d3), axes=F, ylim=c(0,ymax), main="", col=colfunc(nColors), border=NA)
  title(main=conference, col.main=titlecol)
  segments(startLine, ymax, (startLine+underLineWidth), ymax, col= titlecol, lty=lty, lwd=4)
  
  
  axis(1, at=bp, labels=rev(data$year))
  if (m>3){
    axis(2, at=seq(0,ymax,round(ymax/10)))
  }else{
    axis(2, at=axis2sm)
  }
}


trends <- function(root, filename, metric, ylim, axis2, legendy, cex, hline=FALSE){
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
  
  #   pdf(paste(root,"visualisation/",filename,".pdf",sep=""), width=9, height=6)
  
  #   par(mar=c(2,4,0,0), oma=c(0,0,0,0))   
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
  
  #C : 1.5
  #SP : 1.2
  
  labels = c("ASE ", "CSMR ", "FASE ", "FSE ", "GPCE ", "ICPC ", "ICSE ", "ICSM ", "MSR ", "SCAM ", "WCRE ")
  legend(min(data$year), legendy, labels[1:6], cex=cex, col=colors[1:6], text.col=colors[1:6], lty=legend.lty[1:6], lwd=3, seg.len=3, horiz=TRUE, bty="n")
  legend(min(data$year), (0.94*legendy), labels[7:11], cex=cex, col=colors[7:11], text.col=colors[7:11], lty=legend.lty[7:11], lwd=3, seg.len=3, horiz=TRUE, bty="n")
  
}
