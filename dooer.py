SAMPLES = 1000
RFRATE = 1.7
BSHARPE = 2.376844

import numpy as np
import random as rand
import statistics as stats
stocks = np.genfromtxt("data.csv", delimiter=",") 
stocksreturns = np.genfromtxt("dataresults.csv", delimiter=",")
index = np.genfromtxt("dataindex.csv", delimiter=",")
indexreturns = np.genfromtxt("dataindexresults.csv", delimiter=",")
houses = np.genfromtxt("hw1data.csv", delimiter=",")


#household #finwealth #stocktotal #stockdirect #stockindirect #numstocks #weight
trsrl = 0
trl = 0
masterlist = []
for i in range(len(houses)):
    if houses[i][3] == 0:
        minilist = [0, 0, houses[i][6]]
        masterlist.append(minilist)

    else:
        w_index = (houses[i][4])/houses[i][2]
        w_stock = 1 - w_index
        w_pstock = 0
        nstock = houses[i][5]
        if w_stock != 0:
            w_pstock = w_stock/nstock
            running = 0
            runningstddev = 0
            for sample in range(SAMPLES):
                indxs = np.random.permutation(len(stocks))[:int(nstock)]
                final = w_index * indexreturns
                for indx in indxs:
                    final = final + (w_pstock*stocksreturns[indx])
                running = running + final

                monthly_returns = []
                for j in range(119):
                    buffer = w_index * index[j]
                    for indx in indxs:
                        buffer = buffer + (w_pstock*stocks[indx][j])
                    monthly_returns.append((buffer-1)*100)

                stddev = stats.stdev(monthly_returns)
                runningstddev += stddev

            running = running/SAMPLES
            running = pow(running,.1)
            #monthly return stddev
            runningstddev = runningstddev/SAMPLES
            #annualized expectied excess earnings
            #running = ((running - 1) * 100) - RFRATE
            running = ((pow(indexreturns,.1) - 1) * 100) - RFRATE
            samplesharpe = running/runningstddev
            rsrl = 1 - (samplesharpe/BSHARPE)
            print(rsrl)
            rl = w_stock*((BSHARPE*runningstddev) - running)
            trsrl += rsrl * houses[i][6]
            trl += rl * houses[i][6]
            #print(rsrl)
            minilist = [rsrl, rl, houses[i][6]]
            masterlist.append(minilist)

TOTAL_WEIGHT = 0
for i in range(len(masterlist)):
    TOTAL_WEIGHT += masterlist[i][2]


print(TOTAL_WEIGHT)

trsrl = trsrl/TOTAL_WEIGHT
trl = trl/TOTAL_WEIGHT
print(trsrl)
print(trl)

sortedrsrl = sorted(masterlist, key=lambda d: d[0])
#print(sortedrsrl)
quants = [.25, .5, .75, .9, .95, .99]
for q in quants:
    rquant = 0

    for i in range(len(sortedrsrl)):
        rquant += sortedrsrl[i][2]
        if rquant > q*TOTAL_WEIGHT:
            print(sortedrsrl[i][0])
            break

sortedrl = sorted(masterlist, key=lambda d: d[1])
#print(sortedrsrl)
quants = [.25, .5, .75, .9, .95, .99]
for q in quants:
    rquant = 0

    for i in range(len(sortedrl)):
        rquant += sortedrl[i][2]
        if rquant > q*TOTAL_WEIGHT:
            print(sortedrl[i][1])
            break



#25, 50, 75, 90 ,95, 99
#print(trsrl)
#print(trl)






