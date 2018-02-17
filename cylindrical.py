import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import os
import datetime
import glob
from mpl_toolkits.axes_grid1 import make_axes_locatable
from toolbox import *
#def gettingdays(filelist)
#Function to plot plan views
def plotuv(filelist,end,storm,track):
    #Read-in data and select sampling periods
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
        if d not in daylist:
            daylist.append(d)
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
                if hours > 8 or td.days >=1:
                    counti+=1
            if counti==len(sampleperiods):
                sampleperiods.append(dicc['Launch Time'])
    varlist={'P':'hPa','U':'m/s','T':' C','W':'m/s'}
    #Definition of heights for plan views
    l=[300,600,2000]
    print(daylist)
    #
    #sampleperiods=[datetime.datetime(2010,8,28,18,0,0),datetime.datetime(2010,8,29,6,0,0),datetime.datetime(2010,8,29,14,0,0),datetime.datetime(2010,8,30,6,0,0),datetime.datetime(2010,8,31,6,0,0),datetime.datetime(2010,9,1,6,0,0),datetime.datetime(2010,9,2,6,0,0),datetime.datetime(2010,9,3,6,0,0),datetime.datetime(2010,9,4,6,0,0)]
    #sampleperiods=[datetime.datetime(2003,9,12,0,0,0),datetime.datetime(2003,9,12,23,0,0)]#,datetime.datetime(2010,8,29,14,0,0),datetime.datetime(2010,8,30,6,0,0),datetime.datetime(2010,8,31,6,0,0),datetime.datetime(2010,9,1,6,0,0),datetime.datetime(2010,9,2,6,0,0),datetime.datetime(2010,9,3,6,0,0),datetime.datetime(2010,9,4,6,0,0)]
    sampleperiods=[datetime.datetime(2010,8,28,18,0,0),datetime.datetime(2010,8,31,6,0,0),datetime.datetime(2010,9,4,14,0,0),datetime.datetime(2010,8,30,6,0,0),datetime.datetime(2010,8,31,6,0,0),datetime.datetime(2010,9,1,6,0,0),datetime.datetime(2010,9,2,6,0,0),datetime.datetime(2010,9,3,6,0,0),datetime.datetime(2010,9,4,6,0,0)]
    sdt=sampleperiods[0]
    #sampleperiods=[sampleperiods[0]]
    for ll in l:
        for ixi in range(len(sampleperiods)-1):
            sdt=sampleperiods[ixi]#-datetime.timedelta(hours=5)
            nsdt=sampleperiods[ixi+1]
            #nsdt=sampleperiods[ixi]+datetime.timedelta(hours=5)
            x=[]
            y=[]
            z=[]
            dates=[]
            bigdick={'Lat':[],'Lon':[],'P':[],'H':[],'T':[],'U':[],'W':[],'V':[]}
            for filename in filelist:
                print(filename)
                diccionario={'Lat':15,'Lon':14,'P':4,'H':13,'T':5,'U':8,'W':10,'V':9}
                dicc=findproperties(filename,'radazm')
                d=dicc['Launch Time'].day
                if dicc['Launch Time']>sdt:
                    td=dicc['Launch Time']-sdt
                else:
                    td=sdt-dicc['Launch Time']
                    hours, remainder = divmod(td.seconds, 3600)
                date=dicc['Launch Time'].date()
                #if dicc['Launch Time']<sdt or dicc['Launch Time'] > nsdt:
                #    continue
        	    #	print(nump.size,nump.shape)
        	#df=pd.read_csv(filename,sep=' ',skiprows=5,skip_footer=19)
                nump=np.genfromtxt(filename,skip_header=16,skip_footer=19)
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
                mlon=np.nanmean(lon[0:10])
                mlat=np.nanmean(lat[0:10])
                T=clean1(T)
                P=cleanp(clean2(clean1(P)))
                H=clean1(H)
                T=clean2(T)
                r,theta=xytorth(mlon,mlat,track,dicc['Launch Time'])
                plt.scatter(r*np.cos(theta),r*np.sin(theta))
                H=clean2(H)
                u=clean2(cleanu(clean1(u)))
                u=cleanu(u)
                w=clean2(clean1(w))
                rh=clean2(clean1(RH))
                i=findvalues(H,ll)
                #print(i)
                if i==None or np.isnan(np.nanmean(u[i[0]:i[-1]])) or np.isnan(np.nanmean(lon[i[0]:i[-1]])) or np.isnan(np.nanmean(lat[i[0]:i[-1]])):
                        continue
                #print(dicc['lon,lat,alt'])
                T2=np.nanmean(u[i[0]:i[-1]])
                pos=int(np.mean(i))
                for key in bigdick.keys():
                    bigdick[key].append(np.nanmean(diccionario[key][i[0]:i[-1]]))
                dates.append(dicc['Launch Time'])
            #plt.xlim([-250,250])
            #plt.ylim([-250,250])
            #plt.xticks(np.arange(-250,251,50))
            #plt.yticks(np.arange(-250,251,50))
            #plt.grid()
            #plt.show()
            x=bigdick['Lon']
            y=bigdick['Lat']

            #plt.figure()
            print(len(x))
            #ax.contour(tetas,rvec,bigdick['T'])
            #levels=np.arange(10,30,0.5)

            #x=yy
        ##    plt.show()
        #    continue
            print(dates,len(dates))
            #plt.figure(figsize=(13,9))
            mapis=['jet','coolwarm','rainbow']
            counti=0

            for jj,var in enumerate(varlist.keys()):
                print(var)
                if var=='P':
                    step=2
                    offset=0.5
                    place=222
                    #counti=1
                    continue
                elif var=='U':
                    u=bigdick[var]
                    v=bigdick['V']
                    step=8
                    offset=4
                    #continue
                elif var =='T' or var =='W':
                    step=0.5
                    offset=1
                    place=place+1
                    #counti+=1
                    continue
                counter=0
                rvec=[]
                #print(len(x),len(z))
                tetas=[]
                field=[]
                z=bigdick[var]


                dr=[]
                du=[]
                x0=[]
                y0=[]
                dv=[]
                dtheta=[]
                for i,lon in enumerate(x):
                    lat=y[i]
                    r,theta=xytorth(lon,lat,track,dates[i])
                    if r>220:
                        print(r,i)
                        #del z[i-counter]
                    #$    del x[i-counter]
                    #    del y[i-counter]
                    #    del dates[i-counter]
                        counter+=1
                        continue
                    else:
                        if var =='U':
                            unew,vnew=stormu(u[i],v[i],dates[i],track[3])

                            rprima=unew*np.cos(theta)+vnew*np.sin(theta)
                            tetaprima=-unew*np.sin(theta)+vnew*np.cos(theta)
                            #unew,vnew=u[i],v[i]
                            du.append(unew)
                            #print(theta/np.pi,u[i],v[i],np.cos(theta),np.sin(theta),u[i]*np.cos(theta),v[i]*np.sin(theta))
                            dv.append(vnew)
                            dr.append(rprima)
                            dtheta.append(tetaprima)
                            #continue
                            #print(unew,u[i],vnew,v[i])
                        else:
                            field.append(z[i])
                        x0.append(r*np.cos(theta))
                        y0.append(r*np.sin(theta))
                        rvec.append(r)
                        tetas.append(theta)

        #        print(counter)
                #plt.scatter(x0,y0)
                #plt.xlim([-250,250])
                #plt.ylim([-250,250])
                #plt.xticks(np.arange(-250,251,50))
                #plt.yticks(np.arange(-250,251,50))
                #plt.title(storm+' Period:'+str(sdt)+'-'+str(nsdt))
                #plt.grid()
            #    plt.savefig(figdir+'/planviews/tracki.png')
                #plt.show()

                #z=field
                #dr=field
                leni=len(rvec)
                print(leni,rvec)
                #print(len(rvec))
        #        print(x)
        #        print(x0,y0)
                if len(x0)<7:
                    continue
                li=np.linspace(np.nanmin(x0),np.nanmax(x0)+0.1,75)
                yi=np.linspace(np.nanmin(y0),np.nanmax(y0)+0.1,75)
                azi = griddata((x0,y0), dv, (li[None,:], yi[:,None]), method='linear')
        #        CS=plt.contourf(li,yi,azi,colormap='seismic')
        #        plt.colorbar(CS)
        #        plt.show()
                azi = griddata((x0,y0), du, (li[None,:], yi[:,None]), method='linear')
        #        CS=plt.contourf(li,yi,azi,colormap='Spectral')
        #        plt.colorbar(CS)
        #        plt.show()
                xi=np.linspace(np.nanmin(x0)-5,np.nanmax(x0)+5,50)
                yi=np.linspace(np.nanmin(y0)-5,np.nanmax(y0)+5,50)
                xi=np.linspace(np.nanmin(x0)-5,np.nanmax(x0)+5,50)
                yi=np.linspace(np.nanmin(y0)-5,np.nanmax(y0)+5,50)
                print(xi)
                radi = griddata((np.array(x0),np.array(y0)), dr, (xi[None,:], yi[:,None]), method='linear')
                azi= griddata((np.array(x0),np.array(y0)), np.sqrt(np.array(du)**2+np.array(dv)**2), (xi[None,:], yi[:,None]), method='linear')

                labels=['Radial velocity','Azimuthal velocity']
                maps=['jet','RdBu']
            #    for i,zi in enumerate([radi,azi]):
            #        try:
            #            levels=np.arange(int(np.nanmin(zs[i]))+offset,int(np.nanmax(zs[i]))-offset,step)
            #        except:
            #            print('exception killed it')
            #            continue
            #        for ii in range(len(zi[0,:])):
            #            for j in range(len(zi[0,:])):
            #                if zi[j,ii]>max(levels):
            #                    zi[j,ii]=max(levels)
            #                elif zi[j,ii] < min(levels):
            #                    zi[j,ii]=min(levels)
                #    ax = plt.subplot(121+i,projection='polar')
                    #divider = make_axes_locatable(ax)
            #        CS = ax.contour(yi,xi,zi,linewidths=0.5,colors='k',levels=levels)
            #        CS = ax.contourf(yi,xi,zi,cmap=maps[i],levels=levels)
                    #cax = divider.append_axes("right", size="5%", pad=0.05)
            #        plt.colorbar(CS,fraction=0.046, pad=0.04)
            #        ax.scatter(tetas, rvec)
            #        ax.set_rlim(0,220)
            #        ax.set_title(labels[i],fontsize=15)
            #    plt.suptitle(storm+' '+str(sdt),fontsize=16)
            #    plt.show()
                l0=len(rvec)
                #xaxis,yaxis,us,vs=backtoxy(rvec,tetas,du,dv,track[3])
                #break
                #for
                print(len(rvec),len(tetas),len(z))
                #plt.figure(figsize=(12,9))
                #ax = plt.subplot(121,projection='polar')
                #plt.scatter(np.array(x0),np.array(y0))
                #levels=np.arange(-30,30,4)
                #azi = griddata((np.array(tetas),np.array(rvec)), dr, (yi[None,:], xi[:,None]), method='linear')
        #        CS=ax.contourf(xi,yi,azi,cmap='jet')
                #plt.xlim([-250,250])
                #plt.ylim([-250,250])
    #            plt.xticks(np.arange(-250,250,50))
                #plt.colorbar(CS)#
    #            plt.grid()
    #            plt.title(str(sdt))
    #            plt.show()
            #    plt.close()
                #continue
                print(track[3])
                speeddic=track[3]
                rms=speeddic['Rmax']
                ris=0
                counti=0
                for i,key in enumerate(rms):
                    if key.day ==sdt.day:
                        ris+=rms[key]
                        counti+=1
                #rmax=ris/counti
                #print(rmax)
                #equises=np.arange(-rmax,rmax,0.1)
                #yses=np.sqrt(rmax**2-equises**2)
                plt.figure(figsize=(12,6))
                ax = plt.subplot(121)
                CS=ax.contourf(xi,yi,azi,cmap='jet',levels=np.linspace(np.nanmin(azi),np.nanmax(azi),17))
                ax.scatter(x0,y0,c='white')
            #    ax.plot(equises,yses,color='black')
            #    ax.plot(equises,-yses,color='black')
                plt.xlim([-100,100])
                plt.ylim([-100,100])
                ax.set_title('Horizontal wind',fontsize=14)
                plt.colorbar(CS,fraction=0.046, pad=0.04)
                counti+=1
                ax = plt.subplot(122)
                if np.abs(np.nanmin(radi))>np.abs(np.nanmax(radi)):
                    mini=np.nanmin(radi)
                    maxi=-mini
                else:
                    maxi=np.nanmax(radi)
                    mini=np.nanmin(radi)
                CS=ax.contourf(xi,yi,radi,cmap='seismic',levels=np.linspace(mini,maxi,22))
                ax.scatter(x0,y0,c='white')
                plt.xlim([-100,100])
                plt.ylim([-100,100])
                plt.colorbar(CS,fraction=0.046, pad=0.04)
                ax.set_title('Radial')
                plt.suptitle(storm+' '+str(sdt)+' '+str(ll)+' m',fontsize=16)
                plt.tight_layout()
                #plt.savefig(figdir+'planviews/uvplanview'+str(sdt)+str(ll)+'normal.png')
                plt.show()
                #continue
                #x=yy
                continue
                xaxis=xi
                yaxis=yi
                us = griddata((np.array(x0),np.array(y0)), du, (xi[None,:], yi[:,None]), method='linear')
                vs = griddata((np.array(x0),np.array(y0)), dv, (xi[None,:], yi[:,None]), method='linear')
                thnew=[]
                rnew=np.zeros((len(xaxis),len(yaxis)))
                rprima=np.zeros((len(xaxis),len(yaxis)))
                tetaprima=np.zeros((len(xaxis),len(yaxis)))
                for i in range(50):
                    for j in range(50):
                        rnew[i,j]=np.sqrt(xaxis[i]**2+yaxis[j]**2)
                        if rnew[i,j]<0:
                            print(rnew[i,j],i,j)
                        tetita=np.arctan2(yaxis[j],xaxis[i])
                        if tetita<0:
                            print(xaxis[i],yaxis[j],tetita)
                            tetita=tetita+2*np.pi
                        thnew.append(tetita)
                        rprima[j,i]=us[i,j]*np.cos(tetita)+vs[i,j]*np.sin(tetita)
                        tetaprima[i,j]=-us[i,j]*np.sin(tetita)+vs[i,j]*np.cos(tetita)
                #print(thnew)
                #print(rnew)
                #plt.figure(figsize=(13,9))
                #print(place)
                #levels=np.arange(-30,30,4)
                plt.figure(figsize=(12,6))
                ax=plt.subplot(121)
                CS=ax.contourf(xi,yi,rprima,cmap='Spectral')#,levels=np.linspace(np.nanmin(rprima),np.nanmax(rprima),17))

                plt.title('Radial')
                plt.colorbar(CS,fraction=0.046, pad=0.04)
                ax = plt.subplot(122)
                #levels=np.arange(-40,40,4)

                plt.xlim([-50,50])
                plt.ylim([-50,50])
                CS=ax.contourf(xi,yi,tetaprima,cmap='rainbow')
                #plt.colorbar(CS,fraction=0.046, pad=0.04)
                #plt.show()
                #continue
                plt.title('Azimuthal')
                plt.colorbar(CS,fraction=0.046, pad=0.04)
                plt.suptitle(storm+' '+str(sdt)+' at '+ str(ll)+' m')
                #plt.savefig(figdir+str(sdt)+'rtheta.png')
            #    plt.savefig(figdir+'/planviews/'+str(sdt)+str(ll)+'rdthetacylindr_2.png')
                plt.show()
                plt.close()
                continue
                ii=0
                aa=len(tetas)
                while ii < aa:

                    rvec.append(rvec[ii])
                    tetas.append(tetas[ii]+(2*np.pi))
                    z.append(z[ii])
                    dr.append(dr[ii])
                    ii+=1
                #ii=np.where(np.min(tetas))[0][0]
                #rvec.append(rvec[ii])
                #tetas.append(tetas[ii]+(2*np.pi))
                #imax=np.where(np.min(rvec))[0][0]
                #z.append(z[ii])
                #dr.append(dr[ii])
                #rvec.append(rvec[imax])
                #tetas.append(tetas[imax]+(2*np.pi))
                #z.append(z[imax])
                #dr.append(dr[imax])
        #        for i in range(3):
        #            tetas.append(tetas[i]+(2*np.pi))
        #            rvec.append(rvec[i])
            #        print(rvec)
                #    z.append(z[i])
            #    print(np.nanmin(z),np.nanmax(z))
                xi=np.linspace(np.min(rvec)-5,np.max(rvec),100)
                yi=np.linspace(np.min(tetas),np.max(tetas)+0.2,100)
                print(len(z),len(rvec))
            #    plt.figure()
            #    ax = plt.subplot(111,projection='polar')
            #3    ax.contourf(tetas,rvec,z)
            #    plt.show()
            #    plt.close()
                print('out of level filter')
                azi = griddata((np.array(tetas),np.array(rvec)), z, (yi[None,:], xi[:,None]), method='linear')
                radi=griddata((np.array(tetas),np.array(rvec)), dr, (yi[None,:], xi[:,None]), method='cubic')
                #for i in range(100):
    #            rvec=np.append(rvec,rvec[ii])
    #            tetas=np.append(tetas,tetas[ii]+(2*np.pi))
            #    print(rvec.shape)
                zs=[dr,z]

                labels=['Radial velocity','Azimuthal velocity']
                maps=['Spectral','RdBu']
                for i,zi in enumerate([radi,azi]):
                    try:
                        levels=np.arange(int(np.nanmin(zs[i]))+offset,int(np.nanmax(zs[i]))-offset,5)
                    except:
                        print('exception killed it')
                        continue
                    for ii in range(len(zi[0,:])):
                        for j in range(len(zi[0,:])):
                            if zi[j,ii]>max(levels):
                                zi[j,ii]=max(levels)
                            elif zi[j,ii] < min(levels):
                                zi[j,ii]=min(levels)
                    ax = plt.subplot(221+i,projection='polar')
                    #divider = make_axes_locatable(ax)
                    #CS = ax.contour(yi,xi,zi,linewidths=0.5,colors='k',levels=levels)
                    #CS = ax.contourf(yi,xi,zi,cmap=maps[i],levels=levels)
                    #cax = divider.append_axes("right", size="5%", pad=0.05)
                    #plt.colorbar(CS,fraction=0.046, pad=0.04)
                    ax.scatter(tetas, rvec)
                    ax.set_rlim(0,220)
                    ax.set_title(labels[i],fontsize=15)

                continue
                #x=yy
                print(rvec,tetas)
                print(np.min(rvec),np.min(tetas))
                xi=np.linspace(0,np.max(rvec)+0.1,100)
                yi=np.linspace(0,2*np.pi,100)
                print(xi,yi)
                continue
            #plt.suptitle(storm+' Period:'+str(sdt)+' Height '+str(ll)+' m',fontsize=16)
