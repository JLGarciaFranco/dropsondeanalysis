import numpy as np
import pandas as pd
import datetime
import os
atlantic='../Data/AtlanticTrack.txt'
pacific='../Data/PacificTrack.txt'
#df=pd.DataFrame([],columns=['Storm Name','Datetime','Longitude','Latitude','pressure'])
def readtrack(filename,basin):
    f=open(filename,'r')
    a=f.readlines()
    dicc={'Storm Name':[],'Datetime':[],'Longitude':[],'Latitude':[],'pressure':[],'Intensity':[],'Basin':[]}
    f.close()
    ii=0
    line=a[ii]
    while '1996' not in line:
        ii+=1
        line=a[ii]
    while ii<len(a)-1:
        stormname=line.split(',')[1]
        while stormname[0]==' ':
            stormname=stormname[1:]
        #collect datetime, pressure and track.
        ii+=1
        line=a[ii]
        while len(line.split(','))>5 and ii<len(a)-1:
            strings=line.split(',')
            dt=datetime.datetime(int(strings[0][0:4]),int(strings[0][4:6]),int(strings[0][6:8]),int(strings[1][1:3]),int(strings[1][3:5]))
            newlist=[stormname,dt,strings[5],strings[4],int(strings[7]),strings[3],basin]
            ii+=1
            line=a[ii]
            for j,key in enumerate(dicc.keys()):
                dicc[key].append(newlist[j])
    df=pd.DataFrame(dicc)
    return df
df=readtrack(pacific,'pacific')
df2=readtrack(atlantic,'atlantic')
df=df.append(df2)
df.to_csv('track.csv')
