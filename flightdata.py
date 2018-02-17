from netCDF4 import Dataset
import numpy as np
import datetime
import pandas as pd
from toolbox import distance
import glob,os
from math import sin, cos, sqrt, atan2, radians,pi
import matplotlib.pyplot as plt
def cleanrepeatedvalues(dx):
    # Encontramo' los indices duplicado', básicamente evaluamo' la base de dato' dx donde el indice está duplicado
    # y luego le pedimo' el índice. :
    # a) dx.index (indice de dx)
    # b) dx.index.duplicated() objeto que obtiene las posiciones lepetidas o duplicadas.
    # c) dx[dx.index.duplicated()] dx evaluado en las posicions lepetdias.
    # d) dx[dx.index.duplicated()].index similal a a) pelo pala el nuevo mini-dataframe de datos lepetidos.
    indice=dx[dx.index.duplicated()].index
    # El paso anteliol nos devuelve un arreglo de indices sobre el cual iteramos para ir, poco a poco,
    # promediando y sustityendo los datos repetidos.
    for i in indice:
        # Localizamos todos los datos en cada uno de los índices repetidos.
        dh=dx.loc[i]
        # Generamos un nuevo DataFrame con los datos promediados. Este DF solo tendrá un valor por columna (promedio)
        data=pd.DataFrame(dh.groupby(dh.index).mean())
        # Botamos los datos repetidos de dx a partir del índice i.
        dx=dx.drop(i)
        # Ingresamos la DF promediada en dx.
        dx=pd.concat([dx,data])
        # Reacomodamos dx porque este desmadre hizo que los datos promediados se ingresen a dx hasta el final y
        # no donde estaban.
        dx=dx.sort_index()
    return dx
def newtrack(oldtrack):
    newdates=[]
    newlatis=[]
    newlongis=[]
    for i,dt in enumerate(oldtrack.index):
        if i >=len(oldtrack.index)-1:
            break
        values=oldtrack.loc[dt]
        newdates.append(dt)
        counter=1
        t1=oldtrack.loc[oldtrack.index[i+1]]
    #    print(values['Latitude'],len(values['Latitude']))
        lon0=radians(float(values['Longitude'][2:6]))
        lat0=radians(float(values['Latitude'][1:5]))
        lon1=radians(float(t1['Longitude'][2:6]))
        lat1=radians(float(t1['Latitude'][1:5]))
        dlon = lon1 - lon0
        dlat = lat1 - lat0
        newlatis.append(lat0*360/(2*pi))
        newlongis.append(-lon0*360/(2*pi))
        r=distance(lat0,lon0,lat1,lon1)
        rx=distance(lat0,lon0,lat0,lon1)
        ry=distance(lat0,lon0,lat1,lon0)
        x=rx/6
        y=ry/6
        while counter<=5:
            newdates.append(dt+datetime.timedelta(hours=counter))
            newlat=lat0+(dlat/6)*counter
            newlon=lon0+(dlon/6)*counter
            newlatis.append(newlat*360/(2*pi))
            newlongis.append(-newlon*360/(2*pi))
            counter+=1
    #print(len(newlatis),len(newlongis),len(newdates))
    #plt.scatter(newlongis,newlatis,s=1,c='r',label='New Track')
    df=pd.DataFrame(newlongis,index=newdates,columns=['Longitude'])
    df['Latitude']=newlatis
    #df=cleanrepeatedvalues(df)
    #plt.scatter(float(dt['Longitude']),float(dt['Latitude']),s=7,label='Best track')
    #plt.show()
    #x=uu
    return df
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
    btlat=[]
    btlon=[]
    speeddic={'Datetime':[],'U':[],'V':[]}
    for i,dt in enumerate(df.index):
        values=df.loc[dt]
        t1=df.loc[df.index[i+1]]
    #    print(values['Latitude'],len(values['Latitude']))
        lon0=radians(float(values['Longitude'][2:6]))
        lat0=radians(float(values['Latitude'][1:5]))
        lon1=radians(float(t1['Longitude'][2:6]))
        lat1=radians(float(t1['Latitude'][1:5]))
        btlat.append(float(values['Latitude'][1:5]))
        btlon.append(-float(values['Longitude'][2:6]))
        dlon = lon1 - lon0
        dlat = lat1 - lat0
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
    print(speeddic)
    speeddic['Ntrack']=newtrack(df)
    btdate=[]
    keys=filename.variables.keys()
#    for key in keys:
#        print(key)
    print(len(np.array(filename['FL_WC_wind_center_time_offset'])),len(filename['FL_WC_wind_center_latitude']))
    #plt.scatter(filename['FL_WC_wind_center_longitude'],np.array(filename['FL_WC_wind_center_latitude']),label='WC',s=1)
    #plt.show()
#    x=yy
    #print(filename['FL_PLATFORM_uwind_storm_relative'])
    #print(filename['FL_PLATFORM_true_air_speed'])
    #plt.scatter(btlon,btlat,s=7,label='Best track')
    #print(filename['FL_RLB_sfmr_rain_rate_quality_controlled'])
    #print(filename['FL_RLU_distance_from_center'])
    dataindex=np.array(filename['FL_RLU_distance_from_center'])
    #print(list(filename['FL_flight_platform_name']))
    #print(filename['FL_RLU_distance_from_center'])
    #dt=filename['FL_PLATFORM_Sdatetime']
    rmax=np.array(filename['FL_good_radial_leg_flight_level_rmax'])
    dtt=np.array(filename['FL_good_radial_leg_start_Sdatetime'])
    rmaxdates=np.array(filename['FL_good_radial_leg_start_Sdatetime'])
    #print(rmax)
    #print(rmax.shape)
    rmaxis=np.array(filename['FL_good_radial_leg_flight_level_rmax'])
#    print(dtt)
    #print(filename['FL_WC_wind_center_latitude'])
#    print(filename['FL_RLU_flight_level_wind_speed_earth_relative'])
    dataindex=np.array(filename['FL_WC_wind_center_time_offset'])
    #print(filename['FL_RLU_time_offset'])
    lat=np.array(filename['FL_WC_wind_center_latitude'])
    lon=np.array(filename['FL_WC_wind_center_longitude'])
    t0=datetime.datetime.strptime('1970-01-01 00:00:00','%Y-%m-%d %H:%M:%S')
    flat=[]
    flon=[]
    dtime=[]
    for i,j in enumerate(dataindex):
        date=datetime.datetime.fromtimestamp(j).strftime('%Y-%m-%d %H:%M:%S.%f')
        date=datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
        dtime.append(date)
        flat.append(lat[i])
        flon.append(lon[i])
    for jj,dt in enumerate(dtime):
    #    print(values['Latitude'],len(values['Latitude']))
        lon0=radians(flon[jj])
        lat0=radians(flat[jj])
        lat1=radians(flat[jj+1])
        lon1=radians(flon[jj+1])
        dlon = lon1 - lon0
        dlat = lat1 - lat0
        r=distance(lat0,lon0,lat1,lon1)
        rx=distance(lat0,lon0,lat0,lon1)
        ry=distance(lat0,lon0,lat1,lon0)
        x=rx*1000
        y=ry*1000
        deltatime=dtime[jj+1]-dt
        u=x/deltatime.seconds
        v=y/deltatime.seconds
        #print(lon0,lon1,t1['Longitude'][2:6])
        #print(rx,ry,u,v)
        if dlon > 0:
            u=-u
        if dlat <0:
            v=-v
        speeddic['Datetime'].append(dt)
        speeddic['U'].append(u)
        speeddic['V'].append(v)
        if jj==len(dtime)-2:
            break
    newnewdicc={}
    for i,dt in enumerate(rmaxdates):
        try:
            date=datetime.datetime.strptime(dt[0:-3], '%m/%d/%Y %H:%M:%S ')
            newnewdicc[date]=rmaxis[i]
        except:
            continue
    speeddic['Rmax']=newnewdicc
    return dtime,flat,flon,speeddic
    #plt.plot(dataindex[i])
    #plt.show()
#plt.figure(figsize=(12,8))
#
#plt.scatter(flon,flat,c='k',marker='s',label='Flight level data')
#plt.xlim([-60,-55.])
#plt.title('Isabel track for 12/09/2003',fontsize=17)
#plt.xlabel('Longitude',fontsize=15)
#plt.ylabel('Latitude',fontsize=15)
#plt.legend()
#plt.grid()
#plt.savefig('/home/jlgf/Documents/MRes/Project/figs/Isabel/trackcomparison2.png')
#plt.show()
