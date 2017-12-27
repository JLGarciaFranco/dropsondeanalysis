from netCDF4 import Dataset
import numpy as np
import datetime
import pandas as pd
from toolbox import distance
import glob,os
from math import sin, cos, sqrt, atan2, radians
import matplotlib.pyplot as plt
def getrack(storm,year):
    #filename=Dataset('../Data/2003/Isabel/FLIGHT_2003_AL132003_ISABEL_L3_v1.2.nc')
    filen=glob.glob('../Data/'+year+'/'+storm+'/*.nc')
    #print(filen)
    filename=Dataset(filen[0])
    df=pd.read_csv('track.csv')
    df=df[(df['Storm Name']==storm.upper()) & (df['Year']==int(year))]
    df.index=df['Datetime']
    df.index=pd.to_datetime(df.index)
    del df['Datetime']
    speeddic={'Datetime':[],'U':[],'V':[]}
    for i,dt in enumerate(df.index):
        values=df.loc[dt]
        t1=df.loc[df.index[i+1]]
    #    print(values['Latitude'],len(values['Latitude']))
        lon0=radians(float(values['Longitude'][2:6]))
        lat0=radians(float(values['Latitude'][1:5]))
        lon1=radians(float(t1['Longitude'][2:6]))
        lat1=radians(float(t1['Latitude'][1:5]))
        dlon = lon1 - lon0
        dlat = lat1 - lat0
        #theta=atan2(sin(dlon)*cos(lat1),cos(lat0)*sin(lat1)-sin(lat0)*cos(lat1)*cos(dlon))
        #print(theta)
        r=distance(lat0,lon0,lat1,lon1)
        rx=distance(lat0,lon0,lat0,lon1)
        ry=distance(lat0,lon0,lat1,lon0)

        x=rx
        y=ry
        u=x/6.
        v=y/6.
        #print(lon0,lon1,t1['Longitude'][2:6])
        u=u*1000/3600.
        v=v*1000/3600.
        #print(rx,ry,u,v)
        if dlon > 0:
            u=-u
        if dlat <0:
            v=-v
        speeddic['Datetime'].append(dt)
        speeddic['U'].append(u)
        speeddic['V'].append(v)
        if i==len(df.index)-2:
            break
    #df=pd.read_csv('../Data/2003/Isabel/isabeltrack.csv',names=['day','slash','hour','latitude','longitude','minpressure','winds','state'])
    #print(df.columns)
    #x=uyy
    btlat=[]
    btlon=[]
    btdate=[]
    keys=filename.variables.keys()
#    for key in keys:
    #    print(key)
    #print(filename['FL_PLATFORM_uwind_storm_relative'])
    #print(filename['FL_PLATFORM_true_air_speed'])


    #print(filename['FL_RLB_sfmr_rain_rate_quality_controlled'])
    #print(filename['FL_RLU_distance_from_center'])
    dataindex=np.array(filename['FL_RLU_distance_from_center'])
    #print(list(filename['FL_flight_platform_name']))
    #print(filename['FL_RLU_distance_from_center'])
    #dt=filename['FL_PLATFORM_Sdatetime']
    rmax=np.array(filename['FL_good_radial_leg_flight_level_rmax'])
#    print(filename['FL_RLU_flight_level_wind_speed_earth_relative'])
    dt=filename['FL_RLU_time_offset']
    lat=filename['FL_RLU_latitude']
    lon=filename['FL_RLU_longitude']
#    x=yy
    t0=datetime.datetime.strptime('1970-01-01 00:00:00','%Y-%m-%d %H:%M:%S')
    flat=[]
    flon=[]
    dtime=[]
    #print(len(dt))
    for i,j in enumerate(dataindex):
        #print(dt[i][0])
        date=datetime.datetime.fromtimestamp(dt[i][0]).strftime('%Y-%m-%d %H:%M:%S.%f')
        #print(type(date))
        date=datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
        #print(type(date))
        dtime.append(date)
        flat.append(lat[i][0])
        flon.append(lon[i][0])
        for k,val in enumerate(j):
            if val == -9999.0:
                dataindex[i][k]=np.nan
    return dtime,flat,flon,speeddic
    #plt.plot(dataindex[i])
    #plt.show()
#plt.figure(figsize=(12,8))
#plt.plot(btlon*-1,btlat,label='Best Track')
#plt.scatter(flon,flat,c='k',marker='s',label='Flight level data')
#plt.xlim([-60,-55.])
#plt.title('Isabel track for 12/09/2003',fontsize=17)
#plt.xlabel('Longitude',fontsize=15)
#plt.ylabel('Latitude',fontsize=15)
#plt.legend()
#plt.grid()
#plt.savefig('/home/jlgf/Documents/MRes/Project/figs/Isabel/trackcomparison2.png')
#plt.show()
