library('quantmod')

#Toyota <- as.xts(read.zoo('7203.T_stock.csv', header=TRUE, sep=','))
#SoftBank <- as.xts(read.zoo('9984.T_stock.csv', header=TRUE, sep=','))
Ganho <- as.xts(read.zoo('3765.Q_stock.csv', header=TRUE, sep=','))

candleChart(Ganho['2013-04::'])
