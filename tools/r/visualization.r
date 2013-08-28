# Copyright 2012-2013
# Eindhoven University of Technology (Bogdan Vasilescu and Alexander Serebrenik) and
# University of Mons (Tom Mens)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
root <- "/Users/bogdanv/github/conferenceMetrics/"

make_plot <- function(filename, metric, ylim, axis2, legendy, hline=FALSE){
  data <- read.csv(paste(root, "metrics/", filename, ".csv", sep=""), sep=";")
  # head(data)
  
  conferences <- c("MSR", "ICSM", "ICSE", "CSMR", "WCRE", "ICPC", "FSE", "FASE", "ASE", "GPCE", "SCAM")
#   colors <- c(colors()[55], colors()[27], colors()[33], colors()[90], colors()[81], colors()[31], colors()[121],
#               colors()[142], colors()[50], colors()[36], colors()[12])
  colors = c("#332288", "#6699CC", "#88CCEE", "#661100", "#44AA99", "#117733", "#999933", "#DDCC77", "#CC6677", "#882255", "#AA4499")
  #plotchar <- c(15, 0, 16, 17, 23, 1, 2, 5, 25)
  #plotchar <- c(17, 0, 17, 17, 17, 0, 0, 0, 17)
  plotchar <- c(20, 20, 0, 20, 20, 20, 0, 0, 0, 20, 20)
  ltys = c(5, 5, 1, 5, 5, 5, 1, 1, 1, 5, 5)
  #ltys = c(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
  #plotchar <- c(20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20)
  
  pdf(paste(root,"visualisation/",filename,".pdf",sep=""), width=9, height=6)
  
  #layout(matrix(c(1,2,3,4,5,6,7,8,9,10,11,0), nrow = 4, ncol = 3, byrow = TRUE))
  
#   content <- function(ylim, axis2, legendy){
    
      par(mar=c(2,4,0,0), oma=c(0,0,0,0))   
      plot(data$year, type="n", xlim=c(min(data$year), max(data$year)), ylim=ylim, axes=FALSE, xlab="", ylab=metric)
      #plot(data$year, data[[conferences[i]]], type="n", xlim=c(min(data$year), max(data$year)), ylim=ylim, xlab="", ylab=conferences[i])
      # grid(NULL, NULL, col = "lightgray", lty = "dotted", lwd = 2, equilogs = FALSE)
      axis(1, at=data$year, xlab="")
      axis(2, at=axis2)
      if (hline){
        abline(h=1, col="gray", lty=2)
      }
       
  for (i in 1:length(conferences)){
    lines(data$year, data[[conferences[i]]], type="l", lwd=1.5, lty=ltys[i], col=colors[i], 
            pch=plotchar[i], bg=colors[i], cex=1.25)
#       cat(paste(conferences[i], mean(data[[conferences[i]]], na.rm=TRUE),sep=" "), "\n")
    }
#     cat("\n")
#     legend(min(data$year), legendy, conferences, cex=0.8, col=colors, lty=rep(1, length(conferences)), 
#            lwd=rep(10, length(conferences)), horiz=TRUE, bty="n")#, pch=plotchar)
    
    legend(min(data$year), legendy, conferences[1:6], cex=0.8, col=colors[1:6], lty=rep(1, 6), 
           lwd=rep(10, 6), horiz=TRUE, bty="n")#, pch=plotchar)
    legend(min(data$year), (0.95*legendy), conferences[7:11], cex=0.8, col=colors[7:11], lty=rep(1, 5), 
           lwd=rep(10, 5), horiz=TRUE, bty="n")#, pch=plotchar)
#   }
  
#   content(ylim, axis2, legendy)
  dev.off()
  
  # png(paste(root,"visualisation/",filename,".png",sep=""), width=12, height=6, units="in", res=200)#, pointsize=1)
  # content(ylim, axis2, legendy)
  # dev.off()
}

source("/Users/bogdanv/github/conferenceMetrics/tools/r/linesNoDots.r")

# Number of PC members
linesNoDots(root, "C", "#C(c,y)", c(0,100), c(0, 25, 50, 75, 100), 101)


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

# Submissions
make_plot("SP", "#SP(c,y)", c(0,500), c(0, 100, 200, 300, 400, 500), 500)

# Review load
make_plot("RL", "RL(c,y)", c(0,12), c(0, 3, 6, 9, 12), 12)




library(ggplot2)
library(reshape2)
library(ggthemes)

tol11qualitative=c("#332288", "#6699CC", "#88CCEE", "#661100", "#44AA99", "#117733", "#999933", "#DDCC77", "#CC6677", "#882255", "#AA4499")

data <- read.csv(paste(root,"metrics/C.csv", sep=""), sep=";")
data$year = format(paste(data$year, '-01-01 12:00:00 UTC',sep=''), format = "%Y-%B-%D %H:%M:%S")
data$year <- as.POSIXct(data$year)#, format = "%Y-%B-%D %H:%M:%S")
data2 = data.frame(year=data$year, FSE=data$FSE, ICSE=data$ICSE, ICSM=data$ICSM, ASE=data$ASE,
                   WCRE=data$WCRE, CSMR=data$CSMR, ICPC=data$ICPC, FASE=data$FASE, GPCE=data$GPCE,
                   SCAM=data$SCAM, MSR=data$MSR)
head(data2)
tail(data2)
conferences <- c("FSE", "ICSE", "ICSM", "ASE", "WCRE", "CSMR", "ICPC", "FASE", "GPCE", "SCAM", "MSR")

m = melt(data2, id.vars = "year")
head(m)
#levels(m$variable)
#m$variable <- factor(m$variable, levels = c("FSE", "ICSM", "ICSE", "CSMR", "WCRE", "ICPC", "MSR", "FASE", "ASE", "GPCE", "SCAM")) #rev(levels(m$variable)))
#names(dat), order=-as.numeric(variable)

ggplot(m, aes(x=year, y=value, group=variable, fill=variable)) +
  geom_area() +
  xlab("Date") + ylab("#C(c,y)") +
  ggtitle("") + 
  #scale_color_discrete(name = "Trophic Level") + 
  #scale_colour_brewer() +
  scale_x_datetime() + 
  theme_few() + 
  theme(legend.position=c(0.05, 0.7)) +
  scale_fill_manual(values=tol11qualitative, name="Conference", 
                     breaks=rev(conferences),
                     labels=rev(conferences))



attach(mtcars)
layout(matrix(c(1,2,3,4,5,6,7,8,9,10,11,0), nrow = 4, ncol = 3, byrow = TRUE))
hist(wt)
hist(mpg)
hist(disp)




p4 <- 
  ggplot(subset(ChickWeight, Time==21), aes(x=weight, fill=Diet)) +
  geom_histogram(colour="black", binwidth=50) +
  facet_grid(Diet ~ .) +
  ggtitle("Final weight, by diet") +
  theme(legend.position="none")

p4

head(tips)
ggplot(data=tips, aes(x=day)) + geom_bar(stat="bin")
# Equivalent to this, since stat="bin" is the default:
ggplot(data=tips, aes(x=day)) + geom_bar()

head(data)
head(m)

ggplot(m, aes(x=year, fill=variable)) +
  geom_bar(stat="identity", position="dodge") +
  facet_grid(variable ~ .) +
  ggtitle("Final weight, by diet") +
  theme(legend.position="none")



dat <- read.table(text="
cars    trucks  suvs
1   2   4
3   5   4
6   4   6
4   5   6
9   12  16", header=TRUE, as.is=TRUE)
dat$day <- factor(c("Mo", "Tu", "We", "Th", "Fr"), 
                  levels=c("Mo", "Tu", "We", "Th", "Fr"))

library(reshape2)
library(ggplot2)

dat
mdat <- melt(dat, id.vars="day")
head(mdat)
head(m)

data <- read.csv(paste(root,"metrics/C.csv", sep=""), sep=";")
# data$year = format(paste(data$year, '-01-01 12:00:00 UTC',sep=''), format = "%Y-%B-%D %H:%M:%S")
# data$year <- as.POSIXct(data$year)#, format = "%Y-%B-%D %H:%M:%S")
data1 = data.frame(year=data$year, CSMR=data$CSMR, WCRE=data$WCRE, ASE=data$ASE, ICSM=data$ICSM, ICSE=data$ICSE, FSE=data$FSE)
data2 = data.frame(year=data$year, MSR=data$MSR, SCAM=data$SCAM, GPCE=data$GPCE, FASE=data$FASE, ICPC=data$ICPC)
m1 = melt(data1, id.vars = "year")
m2 = melt(data2, id.vars = "year")
head(m1)
head(m2)

p1 = ggplot(m1, aes(x=year, value)) + 
  geom_bar(stat="identity", position="dodge") +
  facet_grid(variable ~ .) +
  theme(legend.position="none") + 
  theme_few()

# library(grid)
# gt <- ggplot_gtable(ggplot_build(p1))
# gt$heights[[3]] <- unit(6, "lines")
# gt$heights[[5]] <- unit(6, "lines")
# gt$heights[[7]] <- unit(6, "lines")
# gt$heights[[9]] <- unit(6, "lines")
# # gt$heights[[10]] <- unit(6, "lines")
# grid.draw(gt)


p2 = ggplot(m2, aes(x=year, value)) + 
  geom_bar(stat="identity", position="dodge") +
  facet_grid(variable ~ .) +
  theme(legend.position="none") + 
  theme_few()

# library(gridExtra)
# grid.arrange(p1, p2, ncol=2)


# library(gridExtra)
# grid.arrange(p1, p2, ncol=2, heights=c(2, 1), widths =c(1,1), as.table =TRUE)

library(wq)
layOut(list(p1, 1:6, 1),
       list(p2, 2:6, 2))


# data <- read.csv(paste(root,"metrics/C.csv", sep=""), sep=";")
# data <- read.csv(paste(root,"metrics/SP.csv", sep=""), sep=";")
data <- read.csv(paste(root,"metrics/RL.csv", sep=""), sep=";")

#data$year = format(paste(data$year, '-01-01 12:00:00 UTC',sep=''), format = "%Y-%B-%D %H:%M:%S")
#data$year <- as.POSIXct(data$year)#, format = "%Y-%B-%D %H:%M:%S")

source("/Users/bogdanv/github/conferenceMetrics/tools/r/miniPlot.r")

# par(mfcol=c(4,3))
layout(matrix(c(1,1,1,2,1,1,1,3,1,1,1,4,5,6,7,8,9,10,11,12), 5, 4, byrow = TRUE))
par(mar=c(2,1,2,1))
par(oma=c(1,1,0,1))

# trends(root, "C", "#C(c,y)", c(0,100), c(0, 25, 50, 75, 100), 105)
# trends(root, "SP", "#SP(c,y)", c(0,550), c(0, 100, 200, 300, 400, 500), 550)
trends(root, "RL", "RL(c,y)", c(0,13), c(0, 3, 6, 9, 12), 13)

# maxval = 80 # C
# maxy = 500 # SP
maxy = 12

miniPlot(data, "ASE", maxy)
miniPlot(data, "CSMR", maxy)
miniPlot(data, "FASE", maxy)
miniPlot(data, "FSE", maxy)
miniPlot(data, "GPCE", maxy)
miniPlot(data, "ICPC", maxy)
miniPlot(data, "ICSE", maxy)
miniPlot(data, "ICSM", maxy)
miniPlot(data, "MSR", maxy)
miniPlot(data, "SCAM", maxy)
miniPlot(data, "WCRE", maxy)



# library("Rgraphviz")
# conferences = c("ASE", "CSMR", "FASE", "FSE", "GPCE", "ICPC", "ICSE", "ICSM", "MSR", "SCAM", "WCRE")
# 
# gr = new("graphNEL", nodes = conferences, edgemode = "directed")
# gr = addEdge("ICSM", "MSR", gr, 1)
# gr = addEdge("ICSM", "ICSE", gr, 1)
# gr = addEdge("ICSM", "ASE", gr, 1)
# gr = addEdge("ICSM", "SCAM", gr, 1)
# gr = addEdge("ICSM", "ICPC", gr, 1)
# gr = addEdge("ICSM", "WCRE", gr, 1)
# gr = addEdge("ICSE", "FSE", gr, 1)
# gr = addEdge("ICSE", "FASE", gr, 1)
# gr = addEdge("ICSE", "GPCE", gr, 1)
# gr = addEdge("ASE", "FSE", gr, 1)
# gr = addEdge("ASE", "FASE", gr, 1)
# gr = addEdge("ASE", "GPCE", gr, 1)
# gr = addEdge("SCAM", "FSE", gr, 1)
# gr = addEdge("SCAM", "FASE", gr, 1)
# gr = addEdge("SCAM", "GPCE", gr, 1)
# gr = addEdge("ICPC", "FSE", gr, 1)
# gr = addEdge("ICPC", "FASE", gr, 1)
# gr = addEdge("ICPC", "GPCE", gr, 1)
# gr = addEdge("CSMR", "FSE", gr, 1)
# gr = addEdge("CSMR", "FASE", gr, 1)
# gr = addEdge("CSMR", "GPCE", gr, 1)
# gr = addEdge("WCRE", "FSE", gr, 1)
# gr = addEdge("WCRE", "FASE", gr, 1)
# gr = addEdge("WCRE", "GPCE", gr, 1)
# plot(gr)
# plot(gr, "neato")
# plot(gr, "twopi")


dev.off()

fse = data.frame(year=data$year, val=data$FSE)
bp = barplot(rev(fse$val), axes=F, ylim=c(0,80))
axis(1, at=data$year, labels=data$year)
axis(2, at=seq(0,80,10))

t = t(as.matrix(rev(fse$val)))
barplot(t, col=heat.colors(7))

d2 = data
d2$year = NULL
barplot(as.matrix(d2))

years = as.character(rev(data$year))
d3 = data.frame(matrix(ncol = length(years), nrow = 1))
names(d3) = years
for (col in length(d3)){
  y = as.numeric(years[col])
  row = which(vals$year==y)
  vals$val[row]
  d3[,col] = rep(1,)
}
d3[c("c","b")] = NA

d3$a = NA

barplot(as.matrix(d3), col=heat.colors(70), border=NA)


