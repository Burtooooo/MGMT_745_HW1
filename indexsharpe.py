RFRATE = 1.7
import numpy as np
import random as rand
import statistics as stats

index = np.genfromtxt("dataindex.csv", delimiter=",")
stocks = np.genfromtxt("data.csv", delimiter=",") 
stocksreturns = np.genfromtxt("dataresults.csv", delimiter=",")


tenreturn = 3.194267535226669619
tr = (pow(tenreturn, .1)-1)*100

monthly_returns = []

for i in range(119):
    monthly_returns.append((index[i]-1)*100)

stddev = stats.stdev(monthly_returns)
tr = tr - RFRATE
print(tr)
print(tr/stddev)
#Benchmark sharpe = 1.7860169152501317


running = 0
for j in range(len(stocks)):
    sr = (100*(pow(stocksreturns[j], .1)-1)-RFRATE)/(stats.stdev(([(i-1)*100 for i in stocks[j]])))
    running += sr
#print(running/len(stocks)


mret = []
for i in range(119):
    buffer = 0
    for j in range(len(stocks)):
        buffer += (stocks[j][i]-1)*100
    mret.append(buffer/len(stocks))

sr = 0
for i in range(len(stocks)):
    sr += stocksreturns[i]

print(stats.stdev(mret))
sr = (pow(sr/len(stocks), .1)-1) * 100
print(sr/stats.stdev(mret))
