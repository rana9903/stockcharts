#!/usr/bin/env python
#
#  Copyright (c) 2007-2008, Corey Goldberg (corey@goldb.org)
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
from ystock import *
import time
import datetime
import math
import re
from pylab import *
import numpy as np

"""
sample usage:
>>> import ystockquote

>>> print ystockquote.get_price('GOOG')
529.46
"""
# symbol_all = ['XIU.TO', 'XEG.TO', 'CNQ.TO', 'SU.TO','SVY.TO','CPG.TO','TLM.TO','NOK','F', 'BB.TO', 'XGD.TO','AGI.TO', 'BTO.TO','THI.TO', 'POT.TO', 'MFC.TO', ]
# symbol_oil = ['XEG.TO', 'CNQ.TO', 'SU.TO', 'CPG.TO']
_oil        =  ['XEG.TO', 'SU.TO', 'CNQ.TO','SVY.TO','CPG.TO','TLM.TO']
_gold       = ['XGD.TO','AGI.TO', 'G.TO', 'ABX.TO' ]
_tech       = ['F','NOK','FB','BB.TO']
_lowrisk    =  ['MFC.TO', 'THI.TO', 'XFN.TO']
_all        = ['XFN.TO','XEG.TO', 'COS.TO','SU.TO', 'CNQ.TO','SVY.TO','CPG.TO','XGD.TO','AGI.TO', 'G.TO', 'ABX.TO','MFC.TO', 'BB.TO']

#symbol = ['THI.TO','XEG.TO']
data        = []
today       =time.strftime("%Y%m%d")
fromDate    ="20141120" 


def filldata(stock_symbol):
    global data
# Get historical data 
    data = get_historical_prices(stock_symbol, fromDate, today)
    #Adding Extra Columns 
    data[0].append("Average High") 
    data[0].append("Average Low") 
    data[0].append("Action") 
    """
    Updating the list with todays Data
    """
    if (time.strftime("%Y-%m-%d") not in data[1][0]):
        today_data= get_all(stock_symbol)
        data.insert(1,[])
        data[1].append(time.strftime("%Y-%m-%d"))
        data[1].append(today_data['open'])
        data[1].append(today_data['days_high'])
        data[1].append(today_data['days_low'])
        data[1].append(today_data['last_price'])
        data[1].append(today_data['volume'])
        data[1].append(today_data['adj_close'])
    
    
#Calculating Average High
def averagehigh(average):
    averagehigh=0
    for listitem in average:
        if listitem[0] != "Date":
            averagehigh = averagehigh+ float (listitem[2])
    return  "{0:10.3f}".format(float(averagehigh/len(average)))

#Calculating Average Low
def averagelow(average):
    averagelow=0
    for listitem in average:
        if listitem[0] != "Date":
            averagelow = averagelow+ float (listitem[3])
    return "{0:10.3f}".format(float(averagelow/len(average)))
"""
Adding last 10 days average high
Adding Bull vs Bear in graphCIBC R/EST 'FRAC
"""
def addavgHighandLow():
    global data
    start =1
    end = 10
    while (start+11)<len(data):
        datseg = data[start:(start+end)]
        data[start].append(averagehigh(datseg)) 
        data[start].append(averagelow(datseg)) 
        # data[start].append(averagelow(datseg))
        if float(data[start][3]) > float(data[start][7]):
            data[start].append("BULL")
        elif float(data[start][2]) < float(data[start][8]): 
            data[start].append("BEAR")  
        else:
            data[start].append("----")
        start +=1

# data.append(get_all("SU.TO"))
# Printing the results 
def printData():
    global data
    # print data
    print "-" * 120 
    for row in data:
        if len(row)>9:
            # print "{0:^10} {1:>10} {2:>10} {3:>10} {4:>10} {5:>15} {6:>15} {7:>10} {8:>10} {9:>10}".\
            #     format(str(row[0]), str(row[1]), str(row[2]),str(row[3]),str(row[4]),\
            #     str(row[7]), str(row[8]), str(row[6]), str(row[5]), str(row[9]))
            print "{0:^10} {1:>10} {2:>10} {3:>10} {4:>10} {5:>15} {6:>15}".\
                format(str(row[0]), str(row[1]), str(row[2]),str(row[3]),str(row[4]),\
                str(row[5]), str(row[9]))
        if "Date" in row[0]:
            print "-" * 120 

# Drawing the plot
def drawPlot(plotdata,ticker):
    global data
    high=[]
    low =[]
    avghigh=[]
    avglow =[]
    closing =[]
    volume = []
    daysopen = []
    x =[]
    i =0;
    for row in plotdata:
        # print row 
        if len(row)>9 and ("Date" not in row[0]):
            high.append(float (row[2]))
            low.append(float (row[3]))
            avghigh.append(float(row[7]))
            avglow.append(float(row[8]))
            closing.append(float(row[4]))
            daysopen.append(float(row[1]))
            volume.append(row[5])
            i+=1
            x.append(i) 
    high.reverse()
    low.reverse()
    avghigh.reverse()
    avglow.reverse()
    closing.reverse()
    daysopen.reverse()
    


    
    fig = plt.figure()
    

    ax1 = fig.add_axes([0.05, 0.05, 0.9, 0.9])  # left, bottom, width, height (range 0 to 1)
    # ax2 =  fig.add_axes([0.05,0.05,.9,.2]
    ax1.plot(x, high,'g--o', x, low,'r-o', x,avghigh,'k-o', x, avglow,'k-o', x, closing, 'b--o', x, daysopen, 'c--o', linewidth=2.0)
    ax1.set_title(ticker)
    ax1.yaxis.tick_right()
    # ax1.set_yticklabels(np.arange(min(low)-1, max(high)+1, 0.05))
    ax1.set_xlim(0,i+1)
    ax1.set_ylim(min(low)-.01, max(high)+0.1)
    ax1.xaxis.set_major_locator(MultipleLocator(1))
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_major_locator(MultipleLocator(min(avglow)/300))
    ax1.yaxis.set_minor_locator(MultipleLocator(min(avglow)/100))
    ax1.grid(which='major', axis='x', linewidth=0.25, linestyle='-', color='0.75')
    ax1.grid(which='minor', axis='x', linewidth=0.75, linestyle='-', color='0.75')
    ax1.grid(which='major', axis='y', linewidth=0.40, linestyle='-', color='0.75')
    ax1.grid(which='minor', axis='y', linewidth=0.75, linestyle='-', color='0.75')

    show()

for ticker in _all:
    filldata(ticker)
    addavgHighandLow()
    printData()
    drawPlot(data, ticker)
