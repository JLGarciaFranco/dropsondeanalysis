import numpy as np
import pandas as pd
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import os 
import datetime
import glob
figdir='/home/jlgf/Documents/MRes/Project/figs/'
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
def grid(x, y, z, resX=100, resY=100):
    #"Convert 3 column data to matplotlib grid"
    xi = np.linspace(min(x), max(x), resX)
    yi = np.linspace(min(y), max(y), resY)
    Z = linear(x, y, z, xi, yi)
    X, Y = np.meshgrid(xi, yi)
    return X, Y, Z
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
z=[]
x=[]
y=[]
ds=[21,22,23]
levels=[2000,1000,500]
for dd in ds:
    for ll in levels:
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
	        i=findvalues(H,ll)
	        if i==None:
		        continue
	        T2=np.nanmean(T[i[0]:i[-1]])
	        print(i)	
	        pos=int(np.mean(i))
	        x.append(np.nanmean(lon[i[0]:i[-1]]))
	        y.append(np.nanmean(lat[i[0]:i[-1]]))
	        z.append(T2)
	        plt.scatter(lon[pos],lat[pos],s=10,marker='v')	
        #	plt.plot(lon,lat,label=dicc['Launch Time'].time())
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
        #plt.ylim([12,14]0)

        plt.scatter(x, y, marker='o', s=150, linewidths=4, c=z, cmap=plt.cm.coolwarm)
        plt.colorbar()
        plt.xlabel('Longitude ',fontsize=15)
        plt.ylabel('Latitude ',fontsize=15)
        plt.title(r'$\vec{u}$ field at '+str(ll)+' m '+str(dd)+' Oct',fontsize=16)
        plt.grid()
        plt.savefig(figdir+str(dd)+'ufield'+str(ll)+'m.png')
        plt.close()
    print(x,y,z)
    xi=np.linspace(np.min(x)-0.1,np.max(x)+0.1)
    yi=np.linspace(np.min(y)-0.1,np.max(y)+0.1)
    print(xi,yi)
    zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')
    CS = plt.contour(xi,yi,zi,15,linewidths=0.5,colors='k')
    CS = plt.contourf(xi,yi,zi,15,cmap=plt.cm.jet)
    plt.colorbar() # draw colorbar
    plt.title(r'$\vec{u}$'+ str(dd)+ ' Oct, Patricia (2015)',fontsize=14)
    plt.xlabel('Longitude ',fontsize=15)
    plt.ylabel('Latitude ',fontsize=15)
    plt.grid()
    plt.legend(title='Time',fontsize=8.5)
    plt.savefig(figdir+str(dd)+'ucolor'+str(ll)+'.png')
    plt.close()
    #	break
    #plt.savefig('katrina1.png')
    #plt.show()
