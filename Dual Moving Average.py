# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 19:59:22 2020

@author: Dell
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sicData=pd.read_excel(r'C:\Users\Dell\Desktop\data\SIC(2011-2018).xlsx',parse_dates=[0]) 


def dualMovingAverage(data,shortWindow:int,longWindow:int)->int:
    signals=pd.DataFrame(index=data.Date)
    signals['close']=data['Closing Price VWAP (GHS)'].values
    signals['signal']=0.0
    signals['shortMAVG']=signals['close'].rolling(window=shortWindow,\
                                                        min_periods=1,center=False).mean()
    signals['longMAVG']=signals['close'].rolling(window=longWindow,\
                                                        min_periods=1,center=False).mean()
    signals['signal'][shortWindow:]=np.where(signals['shortMAVG'][shortWindow:]>\
        signals['longMAVG'][shortWindow:],1,0)
    signals['orders']=signals.signal.diff()
    return signals

doubleMovingAverage=dualMovingAverage(sicData,20,100)

fig=plt.figure()
ax1=fig.add_subplot(111,ylabel='SIC PRICES')
sicData['Closing Price VWAP (GHS)'].plot(ax=ax1,color='g',lw=.5)
doubleMovingAverage['shortMAVG'].plot(ax=ax1,color='r',lw=2)
doubleMovingAverage['longMAVG'].plot(ax=ax1,color='b',lw=2)

ax1.plot(doubleMovingAverage.loc[doubleMovingAverage.orders==1.0].\
         index,sicData['Closing Price VWAP (GHS)']\
         [doubleMovingAverage.orders==1.0],'^',markersze=7,color='k')
    
ax1.plot(doubleMovingAverage.loc[doubleMovingAverage.orders==-1.0].\
         index,sicData['Closing Price VWAP (GHS)']\
         [dualMovingAverage.orders==-1.0],'^',markersze=7,color='k')

plt.legend('PRICE','SHORT MAVG','LONG MAVG','BUY','SELL')
plt.title('Double Moving Average Trading Strategy')

plt.show()
