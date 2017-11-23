from netCDF4 import Dataset
import numpy as np
import datetime
import pandas as pd
import glob,os
import matplotlib.pyplot as plt
def getrack(storm,year):
    #filename=Dataset('../Data/2003/Isabel/FLIGHT_2003_AL132003_ISABEL_L3_v1.2.nc')
    filen=glob.glob('../Data/'+year+'/'+storm+'/*.nc')
    print(filen)
    filename=Dataset(filen[0])
    #df=pd.read_csv('../Data/2003/Isabel/isabeltrack.csv',names=['day','slash','hour','latitude','longitude','minpressure','winds','state'])
    #print(df.columns)
    btlat=[]
    btlon=[]
    btdate=[]
    #for index,row in df.iterrows():
    #    print(row['latitude'])
    #    try:
    #        btlat.append(float(row['latitude']))
    #        btlon.append(float(row['longitude']))
    #        btdate.append(datetime.datetime(2003,9,int(row['day']),int(row['hour']/100)))
    #    except:
    #        continue
    #btlon=np.array(btlon)
    #btlat=np.array(btlat)
    keys=filename.variables.keys()
    #print(filename['FL_RLU_distance_from_center'])
    dataindex=np.array(filename['FL_RLU_distance_from_center'])
    print(list(filename['FL_flight_platform_name']))
    print(filename['FL_RLU_distance_from_center'])
    #dt=filename['FL_PLATFORM_Sdatetime']
    dt=filename['FL_RLU_time_offset']
    lat=filename['FL_RLU_latitude']
    lon=filename['FL_RLU_longitude']
    t0=datetime.datetime.strptime('1970-01-01 00:00:00','%Y-%m-%d %H:%M:%S')
    flat=[]
    flon=[]
    dtime=[]
    print(len(dt))
    for i,j in enumerate(dataindex):
        #print(dt[i][0])
        date=datetime.datetime.fromtimestamp(dt[i][0]).strftime('%Y-%m-%d %H:%M:%S.%f')
        dtime.append(date)
        flat.append(lat[i][0])
        flon.append(lon[i][0])
        for k,val in enumerate(j):
            if val == -9999.0:
                dataindex[i][k]=np.nan
    return dtime,flat,flon
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
