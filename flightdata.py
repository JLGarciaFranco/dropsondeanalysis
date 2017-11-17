from netCDF4 import Dataset
import numpy as np
import os
import matplotlib.pyplot as plt
filename=Dataset('../Data/2003/Isabel/FLIGHT_2003_AL132003_ISABEL_L3_v1.2.nc')
keys=filename.variables.keys()
for key in keys:
    print(key)
#print(filename['FL_RLU_distance_from_center'])
dataindex=np.array(filename['FL_RLU_distance_from_center'])
print(filename['FL_PLATFORM_distance_from_center'])
print(filename['FL_RLU_latitude'].shape)
print(filename['FL_PLATFORM_Sdatetime'].shape)
print(filename['FL_RLU_distance_from_center'])
for i,j in enumerate(dataindex):
    #print(j)
    for k,val in enumerate(j):
        if val == -9999.0:
            dataindex[i][k]=np.nan
    #plt.plot(dataindex[i])
    #plt.show()
