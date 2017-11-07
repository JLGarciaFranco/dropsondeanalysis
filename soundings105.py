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
year=input("What year is your storm?")
os.system('ls ../Data/'+year+'/*')
storm=input("What storm are you looking for?")
filelist=glob.glob('../Data/'+year+'/'+storm+'/gps.qc.eol/GIV/*')
filelist2=glob.glob('../Data/'+year+'/'+storm+'/gps.qc.eol/P-3.43/*')
import subprocess
print(subprocess.run(['ls', '-l'], stdout=subprocess.PIPE).stdout.decode('utf-8'))
filelist3=glob.glob('../Data/'+year+'/'+storm+'/ublox.qc.eol/P-3.43/*')
filelist4=glob.glob('../Data/'+year+'/'+storm+'/ublox.qc.eol/GIV/*')
filelist5=glob.glob('../Data/'+year+'/'+storm+'/ublox.qc.eol/P-3.42/*')
filelist=filelist+filelist2+filelist5
filelist=np.sort(filelist)
os.system('mkdir ../figs/'+storm)
figdir='/home/jlgf/Documents/MRes/Project/figs/'+storm+'/'
daylist=[]
for filename in filelist:

	print(filename)
	dicc=findproperties(filename,'radazm')
	d=dicc['Launch Time'].day
	if d not in daylist:
		daylist.append(d)
varlist={'P':'hPa','U':'m/s','T':' C','W':'m/s'}
ll=1000
for dd in daylist:

    x=[]
    y=[]
    z=[]
    bigdick={'Lat':[],'Lon':[],'P':[],'H':[],'T':[],'U':[],'W':[]}
    for filename in filelist:
        print(filename)
        diccionario={'Lat':15,'Lon':14,'P':4,'H':13,'T':5,'U':8,'W':10}
        dicc=findproperties(filename,'radazm')
        d=dicc['Launch Time'].day
        if d != dd:
            continue
        date=dicc['Launch Time'].date()

	    #	print(nump.size,nump.shape)
	#df=pd.read_csv(filename,sep=' ',skiprows=5,skip_footer=19)
        nump=np.genfromtxt(filename,skip_header=16,skip_footer=19)
#        print(nump.shape)
	    #Allocate variables
        for key in diccionario.keys():
            var=nump[:,diccionario[key]]
            diccionario[key]=clean2(clean1(var))
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
 #       print(cleanu(u))
        w=clean2(clean1(w))
        rh=clean2(clean1(RH))
        i=findvalues(H,ll)
        if i==None or np.isnan(np.nanmean(u[i[0]:i[-1]])) or np.isnan(np.nanmean(lon[i[0]:i[-1]])) or np.isnan(np.nanmean(lat[i[0]:i[-1]])):
                continue
        T2=np.nanmean(u[i[0]:i[-1]])
        print('End of clean and find values')
#        print(T2)
        pos=int(np.mean(i))
        for key in bigdick.keys():
            bigdick[key].append(np.nanmean(diccionario[key][i[0]:i[-1]]))
    #    plt.scatter(lon[pos],lat[pos],s=25,c=T2,marker='v')

        #plt.scatter(lon[0],lat[0],s=10,marker='v')
        #plt.plot(lon,lat,label=dicc['Launch Time'].time())
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
    #print(x,y,z)
    x=bigdick['Lon']
    y=bigdick['Lat']
    for var in varlist.keys():

        plt.figure(figsize=(13,9))
        z=bigdick[var]
        try:
            levels=np.arange(int(np.nanmin(z))-1,int(np.nanmax(z))+2,2)
        except:
            continue
        xi=np.linspace(np.min(x)-0.1,np.max(x)+0.1)
        yi=np.linspace(np.min(y)-0.1,np.max(y)+0.1)
        print(bigdick)
        print(xi,yi)
        try:
            zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')
        except:
            continue
        print(zi.shape)
        for i in range(len(zi[0,:])):
            for j in range(len(zi[0,:])):

        	    if zi[j,i]>max(levels):
	        	    zi[j,i]=max(levels)
	            elif zi[j,i] < min(levels):
	        	    zi[j,i]=min(levels)  
        CS = plt.contour(xi,yi,zi,levels,linewidths=0.5,colors='k')
        CS = plt.contourf(xi,yi,zi,levels,cmap=plt.cm.jet)
        cbar=plt.colorbar()# draw colorbar
        cbar.ax.set_title(varlist[var])
        plt.title(var+' field on '+ str(date)+ storm + ' ('+year+')',fontsize=16)
        plt.xlabel('Longitude ',fontsize=15)
        plt.ylabel('Latitude ',fontsize=15)
        plt.grid()
        plt.legend(title='Time',fontsize=8.5)
        plt.savefig(figdir+str(dd)+var+storm+str(ll)+'_2.png')
    #    plt.show()
        plt.close()

        #plt.title('Dropsonde drift'+str(dd)+'for Hurr Rita (2005)',fontsize=14)
    #plt.xlabel('Longitude ',fontsize=15)
    #plt.ylabel('Latitude ',fontsize=15)
    #plt.grid()
   # plt.legend(title='Time',fontsize=8.5)
    #plt.savefig(figdir+'driftrita'+str(dd)+'.png')
    #plt.show()
    #	break
    #plt.savefig('katrina1.png')
    #plt.show()
