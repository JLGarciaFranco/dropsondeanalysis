import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os 
import datetime
import glob
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
	print(l1)
	print(l2)
	print(ls)
	diccionario['Sounding name']=l1[-1]
	ls=ls[1].split(',')
	diccionario['lon,lat,alt']=ls[2:]
	diccionario['Launch Time']=l2[-3]+':'+l2[-2]+':'+l2[-1]
	lanza=diccionario['Launch Time']
	while lanza[0]==' ':
		lanza=lanza[1:]
	print(len(lanza))
	diccionario['Launch Time']=datetime.datetime.strptime(lanza,'%Y-%m-%d, %H:%M:%S ')		
	lanza=diccionario['Sounding name']
	while lanza[0]==' ':
		lanza=lanza[1:]
	diccionario['Sounding name']=lanza
	print(diccionario)
	return diccionario
filelist=glob.glob('../Data/2015/Patricia/*.avp')
filelist=np.sort(filelist)
plt.figure(figsize=(13,9))
for filename in filelist:
	nump=np.genfromtxt(filename,skip_header=6,skip_footer=19)
	print(filename)
	dicc=findproperties(filename)
	print(dicc['Launch Time'].day)
	print(nump.size,nump.shape)
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
	T=clean1(T)
	P=clean2(clean1(P))
	H=clean1(H)
	T=clean2(T)
	H=clean2(H)
	u=clean2(cleanu(clean1(u)))
	w=clean2(clean1(w))
	rh=clean2(clean1(RH))
	textstr=' Pre-launch Obs (alt,lon,lat): \n  7735.6 m, ( 94 19.0314W, 23 50.3082N)'
	plt.plot(w,H,label=dicc['Launch Time'])
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
#	plt.show()
ax=plt.gca()
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.85, box.height])
plt.xlim([-50,50])
plt.ylim([0,3000])
plt.title('Windspeed soundings for Hurr Patricia (2015)',fontsize=14)
plt.xlabel('Windspeed (m/s)',fontsize=15)
plt.ylabel('Geopotential Altitude (m)',fontsize=15)
plt.grid()
plt.legend(title='Date/Time',bbox_to_anchor=(1.1, 1.),fontsize=5.5)
plt.savefig('patriciau.png')
plt.show()
#	break
#plt.savefig('katrina1.png')
#plt.show()
