import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os 
import glob
def clean1(vec):
	falseval=[9999.0,999.0,99.0,99999.0]
	for i,v in enumerate(vec):
		if v in falseval:
			vec[i]=np.nan
	return vec
filename='../Data/g042715047.avp'
nump=np.genfromtxt(filename,skip_header=5,skip_footer=19)
print(nump.size,nump.shape)
#df=pd.read_csv(filename,sep=' ',skiprows=5,skip_footer=19)
#Allocate variables
T=nump[:,6]
P=nump[:,5]
H=nump[:,13]
RH=nump[:,7]
print(P)
print(nump[-1])
T=clean1(T)
P=clean1(P)
H=clean1(H)
rh=clean1(RH)
textstr=' Pre-launch Obs (alt,lon,lat): \n  7735.6 m, ( 94 19.0314W, 23 50.3082N)'
f, (ax1,ax2,ax3)=plt.subplots(1,3,sharey=True,figsize=(16,9))
f.suptitle('Dropsonde Katrina 2005/08/22, 19:56:16',fontsize=18)
ax1.plot(T,H,'r--')
ax1.set_xlabel('T (ºC)',fontsize=14)
ax1.text(0.02, 0.045, textstr, fontsize=10,transform=plt.gcf().transFigure,color='purple')
ax1.set_ylabel('Geopotential Altitude (m)',fontsize=14)
ax1.grid()
ax2.plot(P,H,'k-.')
ax2.set_xlabel('P (Pa)',fontsize=14)
ax2.grid()
ax3.plot(rh,H,'b-')
ax3.set_xlabel('Relative Humidity (%)',fontsize=14)
ax3.grid()
plt.savefig('katrina1.png')
plt.show()
