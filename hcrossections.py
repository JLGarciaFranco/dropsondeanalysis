import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import os
import datetime
import glob
from toolbox import *
#def gettingdays(filelist)

def hsection(filelist,end,storm):
    figdir='/home/jlgf/Documents/MRes/Project/figs/'
    os.system('mkdir ../figs/'+storm)
    figdir='/home/jlgf/Documents/MRes/Project/figs/'+storm+'/'
    daylist=[]
    sampleperiods=[]
    filelist=np.sort(filelist)
    if end=='avp':
    	indexes=[-15,-7,-16,-7]
    	formato='%Y-%m-%d, %H:%M:%S '
    	head=6
    	foot=19
    	longindex=11
    	latindex=12
    elif end=='radazm':
    	indexes=[2,4,5]
    	formato='%Y, %m, %d, %H:%M:%S '
    	head=16
    	foot=19
    	longindex=14
    	latindex=15
    for filename in filelist:
        storm=filename.split('/')[3]
        year=filename.split('/')[2]
        dicc=findproperties(filename,end)
        d=dicc['Launch Time'].day
        #print(dicc['Launch Time'])
        #print(sampleperiods,dicc['Launch Time'])
        if len(sampleperiods)==0:
            sampleperiods.append(dicc['Launch Time'])
        else:
            counti=0
            for date in sampleperiods:
                if dicc['Launch Time']>date:
                    td=dicc['Launch Time']-date
                else:
                    td=date-dicc['Launch Time']
                #print(td.days)
                hours, remainder = divmod(td.seconds, 3600)
                if hours > 5 or td.days >1:
                    counti+=1
            if counti==len(sampleperiods):
                sampleperiods.append(dicc['Launch Time'])

    varlist={'P':'hPa','U':'m/s','T':' C','W':'m/s'}
    ll=1000
    print(sampleperiods)
    for sdt in sampleperiods:
        x=[]
        y=[]
        z=[]
        bigdick={'Lat':[],'Lon':[],'P':[],'H':[],'T':[],'U':[],'W':[]}
        for filename in filelist:
            print(filename)
            diccionario={'Lat':15,'Lon':14,'P':4,'H':13,'T':5,'U':8,'W':10}
            dicc=findproperties(filename,'radazm')
            d=dicc['Launch Time'].day
            if dicc['Launch Time']>sdt:
                td=dicc['Launch Time']-sdt
            else:
                td=sdt-dicc['Launch Time']
                hours, remainder = divmod(td.seconds, 3600)
            date=dicc['Launch Time'].date()
            if hours>4  or td.days>1:
                continue
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
            u=nump[:,8]
            udir=nump[:,11]
            w=nump[:,10]
            lon=nump[:,14]
            lat=nump[:,15]
            lon=clean2(clean1(lon))
            lat=clean2(clean1(lat))

            #t(nump[-1])
            T=clean1(T)
            P=cleanp(clean2(clean1(P)))
            H=clean1(H)
            T=clean2(T)
            H=clean2(H)
            u=clean2(cleanu(clean1(u)))
            u=cleanu(u)
     #       print(cleanu(u))
            w=clean2(clean1(w))
            rh=clean2(clean1(RH))
            i=findvalues(H,ll)
            print(i)
            if i==None or np.isnan(np.nanmean(u[i[0]:i[-1]])) or np.isnan(np.nanmean(lon[i[0]:i[-1]])) or np.isnan(np.nanmean(lat[i[0]:i[-1]])):
                    #print(np.nanmean(u[i[0]:i[-1]]))
                    print('failure in i values')
                    continue
            T2=np.nanmean(u[i[0]:i[-1]])
    #        print(T2)
            pos=int(np.mean(i))
            for key in bigdick.keys():
                bigdick[key].append(np.nanmean(diccionario[key][i[0]:i[-1]]))
            print(len(bigdick[key]))
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
            print(var)
            if var=='P':
                step=15
                offset=0.5
            else:
                step=20
                offset=1
            plt.figure(figsize=(13,9))
            z=bigdick[var]
            print(np.nanmin(z),np.nanmax(z))
            try:
                levels=np.arange(int(np.nanmin(z))-offset,int(np.nanmax(z))+offset,(np.nanmax(z)-np.nanmin(z))/step)
            except:
                print('exception killed it')
                continue
            print('out of level filter')
            xi=np.linspace(np.min(x)-0.1,np.max(x)+0.1)
            yi=np.linspace(np.min(y)-0.1,np.max(y)+0.1)
            #zi = griddata((np.array(x), y), z, (xi[None,:], yi[:,None]), method='cubic')
            try:
                zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')
            except:
                print('griding killed it')
                continue
            print('good')
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
            plt.title(var+' field on '+ str(sdt)+' '+ storm + ' ('+year+')',fontsize=16)
            plt.xlabel('Longitude ',fontsize=15)
            plt.ylabel('Latitude ',fontsize=15)
            plt.scatter(x,y,s=3,c='k')
            plt.grid()
            plt.legend(title='Time',fontsize=8.5)
            plt.savefig(figdir+str(sdt)+' '+var+storm+str(ll)+'_mixed.png')
            plt.show()
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
