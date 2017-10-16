import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import os 
import datetime
import glob
def cleanll(lon):
#	print(np.abs(np.nanmean(lon)+np.nanstd(lon)))
	print(np.nanmean(lon))
	print(np.nanstd(lon))
	for i,l in enumerate(lon):
#		print(i,l)
		if np.abs(l-np.nanmean(lon)) > np.abs(np.nanmean(lon)+np.nanstd(lon)):
			print(np.nanmean(lon))
			print(np.nanstd(lon))
			print(l)
			lon[i]=np.nan
	for i,l in enumerate(lon):
#		print(i,l)
		if np.abs(l-np.nanmean(lon)) > 0.5:
			print(np.nanmean(lon))
			print(np.nanstd(lon))
			print(l)
			lon[i]=np.nan
	return lon
			
def clean1(vec):
	falseval=[9999.0,999.0,99.0,99999.0]
	for i,v in enumerate(vec):
		if v in falseval:
			vec[i]=np.nan
	return vec
def clean2(vec):
	for i,v in enumerate(vec):
		if np.isnan(v):
			if not(np.isnan(vec[i-1]) or np.isnan(vec[i+1])):
				vec[i]=(vec[i-1]+vec[i+1])/2.0
	return vec
def cleanu(vec):
	for i,v in enumerate(vec):
		if v > np.mean(vec)+3*np.std(vec):
			vec[i]=np.nan
	return vec
def findproperties(filename):
	f=open(filename,'r')
	lineas=f.readlines()
	f.close()
	i=-1
	diccionario={'Sounding name':' ','lon,lat,alt':' ','Launch Time':' '}
	l1=lineas[-15].split(':')
	l2=lineas[-16].split(':')
	ls=lineas[-7].split(':')
	diccionario['Sounding name']=l1[-1]
	ls=ls[1].split(',')
	diccionario['lon,lat,alt']=ls[2:]
	diccionario['Launch Time']=l2[-3]+':'+l2[-2]+':'+l2[-1]
	lanza=diccionario['Launch Time']
	while lanza[0]==' ':
		lanza=lanza[1:]
#	print(len(lanza))
	diccionario['Launch Time']=datetime.datetime.strptime(lanza,'%Y-%m-%d, %H:%M:%S ')		
	lanza=diccionario['Sounding name']
	while lanza[0]==' ':
		lanza=lanza[1:]
	diccionario['Sounding name']=lanza
	return diccionario
filelist=glob.glob('../Data/2015/Patricia/*.avp')
filelist=np.sort(filelist)
plt.figure(figsize=(13,9))
map=Basemap(projection='ortho',lat_0=18,lon_0=-100,resolution='l')
map.drawcoastlines(linewidth=0.25)
map.drawcountries(linewidth=0.25)
map.fillcontinents(color='coral',lake_color='aqua')
map.drawparallels(np.arange(-100,-90,4))

dd=22

for filename in filelist:
	nump=np.genfromtxt(filename,skip_header=6,skip_footer=19)
	print(filename)
	dicc=findproperties(filename)
	d=dicc['Launch Time'].day
	if d != dd:
		continue
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
#	print(nump[-1])
	lon=cleanll(lon)
	lat=cleanll(lat)
	T=clean1(T)
	P=clean2(clean1(P))
	H=clean1(H)
	T=clean2(T)
	H=clean2(H)
	u=clean2(cleanu(clean1(u)))
	w=clean2(clean1(w))
	rh=clean2(clean1(RH))
#	plt.scatter(lon[0],lat[0],s=10,marker='v')
	map(lon,lati)#,label=dicc['Launch Time'].time())
#	f, (ax1,ax2,ax3)=plt.subplots(1,3,sharey=True,figsize=(16,9))
#	f.suptitle('Dropsonde Katrina 2005/08/22, 19:56:16',fontsize=18)
#	ax1.plot(T,H,'r--')
#	ax1.set_xlabel('T (C)',fontsize=14)
#	ax1.text(0.02, 0.045, textstr, fontsize=10,transform=plt.gcf().transFigure,color='purple')
#	ax1.set_ylabel('Geopotential Altitude (m)',fontsize=14)
#	ax1.grid()
#	ax2.plot(P,H,'k-.')
#	ax2.set_xlabel('P (Pa)',fontsize=14)
#	ax2.grid()
#	ax3.plot(rh,H,'b-')
#	ax3.set_xlabel('Relative Humidity (%)',fontsize=14)
#	ax3.grid()
#	plt.close()
#plt.xlim([-100,-98])
#plt.ylim([12,14])
plt.title('Dropsonde drift 23 Oct for Hurr Patricia (2015)',fontsize=14)
plt.xlabel('Longitude ',fontsize=15)
plt.ylabel('Latitude ',fontsize=15)
plt.grid()
plt.legend(title='Time',fontsize=8.5)
plt.savefig('drift23.png')
plt.show()
#	break
#plt.savefig('katrina1.png')
#plt.show()
