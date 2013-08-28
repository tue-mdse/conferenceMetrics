# Function for plotting colors side-by-side
pal <- function(col, border = "light gray", ...){
  n <- length(col)
  plot(0, 0, type="n", xlim = c(0, 1), ylim = c(0, 1),
       axes = FALSE, xlab = "", ylab = "", ...)
  rect(0:(n-1)/n, 0, 1:n/n, 1, col = col, border = border)
}

tol14rainbow=c("#882E72", "#B178A6", "#D6C1DE", "#1965B0", "#5289C7", "#7BAFDE", "#4EB265", "#90C987", "#CAE0AB", "#F7EE55", "#F6C141", "#F1932D", "#E8601C", "#DC050C")

tol11rainbow=c("#882E72", "#252525", "#D6C1DE", "#1965B0", "#7BAFDE", "#4EB265", "#CAE0AB", "#F7EE55", "#F6C141", "#F1932D", "#DC050C")

rainbow12equal = c("#BF4D4D", "#BF864D", "#BFBF4D", "#86BF4D", "#4DBF4D", "#4DBF86", "#4DBFBF", "#4D86BF", "#4D4DBF", "#864DBF", "#BF4DBF", "#BF4D86")
rich12equal = c("#000040", "#000093", "#0020E9", "#0076FF", "#00B8C2", "#04E466", "#49FB25", "#E7FD09", "#FEEA02", "#FFC200", "#FF8500", "#FF3300")

length(tol11rainbow)
pal(tol11rainbow)


pal(tol14rainbow)
pal(rich12equal)


mine = c("#000000", "#000093", "#5289C5","#882E72", "#B178A6", "#F7EE55", "#F6C141", "#F1932D", "#DC050C", "#4EB265", "#CAE0AB")
pal(mine)


redmono = c("#99000D", "#CB181D", "#EF3B2C", "#FB6A4A", "#FC9272", "#FCBBA1", "#FEE0D2", "#FFF5F0")
greenmono = c("#005A32", "#238B45", "#41AB5D", "#74C476", "#A1D99B", "#C7E9C0", "#E5F5E0", "#F7FCF5")
bluemono = c("#084594", "#2171B5", "#4292C6", "#6BAED6", "#9ECAE1", "#C6DBEF", "#DEEBF7", "#F7FBFF")
grey8mono = c("#000000","#252525", "#525252", "#737373", "#969696", "#BDBDBD", "#D9D9D9", "#F0F0F0")
grey6mono = c("#242424", "#494949", "#6D6D6D", "#929292", "#B6B6B6", "#DBDBDB")

pal(greenmono)


tol11qualitative=c("#332288", "#6699CC", "#88CCEE", "#44AA99", "#117733", "#999933", "#DDCC77", "#661100", "#CC6677", "#882255", "#AA4499")
tol11qualitative=c("#332288", "#6699CC", "#88CCEE", "#661100", "#44AA99", "#117733", "#999933", "#DDCC77", "#CC6677", "#882255", "#AA4499")

tol12qualitative=c("#332288", "#6699CC", "#88CCEE", "#44AA99", "#117733", "#999933", "#DDCC77", "#661100", "#CC6677", "#AA4466", "#882255", "#AA4499")
pal(tol12qualitative)

pal(tol11qualitative)


library(RColorBrewer)
pal(brewer.pal(80,"Blues"))


bpd <- matrix(c(1,seq(0,1,l=64),2,
                1,seq(0,1,l=64),5,
                1,seq(0,1,l=64),7),
              nc=3)
mycols <- c('blue',rainbow(64,start=0,end=.4)[64:1],'orange') 
mycols <- c('blue',heat.colors(64),'orange') 
barplot(bpd,col=mycols,border=NA) 

pal(c('green',rainbow(64,start=0,end=.4)[64:1],'red'))


tmp <- rbinom(10, 100, 0.78) 
mp <- barplot(tmp, space=0, ylim=c(0,100)) 
tmpfun <- colorRamp( c('green','yellow',rep('red',8)) ) 
mat <- 1-row(matrix( nrow=100, ncol=10 ))/100 
tmp2 <- tmpfun(mat) 
mat2 <- as.raster( matrix( rgb(tmp2, maxColorValue=255), ncol=10) ) 
for(i in 1:10) mat2[ mat[,i] >= tmp[i]/100, i] <- NA 
rasterImage(mat2, mp[1] - (mp[2]-mp[1])/2, 0, mp[10] + (mp[2]-mp[1])/2, 100, 
            interpolate=FALSE) 
barplot(tmp, col=NA, add=TRUE, space=0) 




library(RColorBrewer)
par(mar = c(0, 4, 0, 0))
display.brewer.all()
brewer.pal(8, "Set2")


greenmono = c("#005A32", "#238B45", "#41AB5D", "#74C476", "#A1D99B", "#C7E9C0", "#E5F5E0", "#F7FCF5")
pal(greenmono)

colfunc <- colorRampPalette(c("#005A32", "#E5F5E0"))
colfunc <- colorRampPalette(c("#E5F5E0", "#005A32"))
pal(colfunc(10))



