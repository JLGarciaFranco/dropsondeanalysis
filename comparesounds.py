import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import os 
import datetime
import glob
#def gettingdays(filelist)
figdir='/home/jlgf/Documents/MRes/Project/figs/'
def findvalues(z,level):
        i=0
        zi=z[i]
        index=[]
        while np.abs(zi-level)>10 or np.isnan(zi):
                i+=1
                zi=z[i]
                if i==len(z)-3:
                        return
        index.append(i)
        i+=1
        zi=z[i]

        while np.abs(zi-level)<10 or np.isnan(zi):
                index.append(i)
                i+=1
                zi=z[i]
        return index
def cleanp(P):
    for i,p in enumerate(P):
        if p < 870 or p > 1100:
            P[i]=np.nan
    return P
def cleanll(lon):
#	print(np.abs(np.nanmean(lon)+np.nanstd(lon)))
	for i,l in enumerate(lon):
#		print(i,l)
		if np.abs(l-np.nanmean(lon)) > np.abs(np.nanmean(lon)+np.nanstd(lon)):
			lon[i]=np.nan
	for i,l in enumerate(lon):
#		print(i,l)
		if np.abs(l-np.nanmean(lon)) > 0.5:
			lon[i]=np.nan
	return lon
			
def clean1(vec):
    falseval=[9999.0,999.0,99.0,99999.0,-999,-9999,-99]
#    print(falseval)
    for i,v in enumerate(vec):
        if v in falseval:
            vec[i]=np.nan
    return vec
def clean2(vec):
	for i,v in enumerate(vec):
		if np.isnan(v) and i < len(vec)-1:
			if not(np.isnan(vec[i-1]) or np.isnan(vec[i+1])):
				vec[i]=(vec[i-1]+vec[i+1])/2.0
	return vec
def cleanu(vec):
	for i,v in enumerate(vec):
		if np.abs(v)> 100 or v<-100:
			print(i,v)
		if np.abs(v) > np.abs(np.mean(vec)+2*np.std(vec)) or np.abs(v)>100:
			print(v)
			vec[i]=np.nan
	return vec
def findproperties(filename,database):
	if database=='avp':
		indexes=[-15,-16,-7]
		formato='%Y-%m-%d, %H:%M:%S '
	elif database=='radazm':
		indexes=[2,4,5]
		formato='%Y, %m, %d, %H:%M:%S '
	f=open(filename,'r')
	lineas=f.readlines()
	f.close()
	i=-1
	diccionario={'Sounding name':' ','lon,lat,alt':' ','Launch Time':' '}
	l1=lineas[indexes[0]].split(':')
	ls=lineas[indexes[1]].split(':')
	l2=lineas[indexes[2]].split('):')
	#print(l1,l2,ls)
	diccionario['Sounding name']=l1[-1]
	ls=ls[1].split(',')
	diccionario['lon,lat,alt']=ls[2:]
	#print(l2)
	diccionario['Launch Time']=l2[1]
	#print(l2[1])
	lanza=diccionario['Launch Time']
	while lanza[0]==' ':
		lanza=lanza[1:]
#	print(len(lanza))
	diccionario['Launch Time']=datetime.datetime.strptime(lanza,formato)		
	lanza=diccionario['Sounding name']
	while lanza[0]==' ':
		lanza=lanza[1:]
	diccionario['Sounding name']=lanza
	return diccionario
year=2005
os.system('ls ../Data/'+str(year)+'/*')
storm='Rita'
time='2005/09/21, 16:34:00.31'
filelist=['../Data/2005/Rita/indv/g012225003.avp','../Data/2005/Rita/gps.qc.eol/P-3.43/D20050921_161654.012225003_PQC.eol.radazm.Wwind']
figdir='/home/jlgf/Documents/MRes/Project/figs/'+storm+'/'
daylist=[]
filename=filelist[0]
nump=np.genfromtxt(filename,skip_header=6,skip_footer=19)
	#	print(nump.size,nump.shape)
	#df=pd.read_csv(filename,sep=' ',skiprows=5,skip_footer=19)
	#Allocate variables
T=nump[:,6]
P=nump[:,5]
H=nump[:,13]
RH=nump[:,7]
u=nump[:,9]
udir=nump[:,8]
w=nump[:,0]
lon=nump[:,11]
lat=nump[:,12]
lon=clean2(clean1(lon))
lat=clean2(clean1(lat))

#t(nump[-1])
lon=cleanll(lon)
lat=cleanll(lat)
T=clean1(T)
P=cleanp(clean2(clean1(P)))
H=clean1(H)
T=clean2(T)
H=clean2(H)
u=clean2(cleanu(clean1(u)))
u=cleanu(u)
print(np.nanmin(u))
print(cleanu(u))
w=clean2(clean1(w))
rh=clean2(clean1(RH))
#plt.scatter(lon[0],lat[0],s=10,marker='v')
#plt.plot(lon,lat,label=dicc['Launch Time'].time())
f, (ax1,ax2,ax3)=plt.subplots(1,3,sharey=True,figsize=(16,9))
f.suptitle('Dropsonde Rita 2005/09/21, 16:16',fontsize=18)
ax1.plot(T,H,'r--',label='Individual')
ax1.set_xlabel('T (C)',fontsize=14)
#ax1.text(0.02, 0.045, textstr, fontsize=10,transform=plt.gcf().transFigure,color='purple')
ax1.set_ylabel('Geopotential Altitude (m)',fontsize=14)
ax1.grid()
ax2.plot(P,H,'k-.',label='Individual')
ax2.set_xlabel('P (Pa)',fontsize=14)
ax2.grid()
ax3.plot(rh,H,'b-',label='Individual')
ax3.set_xlabel('Relative Humidity (%)',fontsize=14)
ax3.grid()
varlist={'P':'hPa','U':'m/s','T':' C','W':'m/s'}
    #	print(nump.size,nump.shape)
#df=pd.read_csv(filename,sep=' ',skiprows=5,skip_footer=19)
nump=np.genfromtxt(filelist[1],skip_header=16,skip_footer=10)
T=nump[:,5]
P=nump[:,4]
H=nump[:,13]
RH=nump[:,7]
print('Cleaning u')
u=nump[:,8]
udir=nump[:,11]
w=nump[:,10]
lon=nump[:,14]
lat=nump[:,15]
lon=clean2(clean1(lon))
lat=clean2(clean1(lat))

#t(nump[-1])
lon=cleanll(lon)
lat=cleanll(lat)
T=clean1(T)
P=cleanp(clean2(clean1(P)))
H=clean1(H)
T=clean2(T)
H=clean2(H)
u=clean2(cleanu(clean1(u)))
u=cleanu(u)
print(np.nanmin(u))
print(cleanu(u))
w=clean2(clean1(w))
rh=clean2(clean1(RH))
#plt.scatter(lon[0],lat[0],s=10,marker='v')
#plt.plot(lon,lat,label=dicc['Launch Time'].time())
ax1.plot(T,H,'k--',label='Large Data Set')
ax1.set_xlabel('T (C)',fontsize=14)
#ax1.text(0.02, 0.045, textstr, fontsize=10,transform=plt.gcf().transFigure,color='purple')
ax1.set_ylabel('Geopotential Altitude (m)',fontsize=14)
ax1.grid()
ax2.plot(P,H,'r-.',label='Large Data Set')
ax2.set_xlabel('P (Pa)',fontsize=14)
ax2.grid()
ax3.plot(rh,H,'g-',label='Large Data Set')
ax3.set_xlabel('Relative Humidity (%)',fontsize=14)
ax3.grid()
ax1.legend()
ax2.legend()
ax3.legend()
plt.legend()
plt.savefig(figdir+'comparison.png')
plt.show()
plt.close()
    #plt.xlim([-100,-98])
    #plt.ylim([12,14])
    #print(x,y,z)
   
