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

def plotuv(filelist,end,storm,track):
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
                if hours > 5 or td.days >=1:
                    counti+=1
            if counti==len(sampleperiods):
                sampleperiods.append(dicc['Launch Time'])
    varlist={'P':'hPa','U':'m/s','T':' C','W':'m/s'}
    ll=600
    print(sampleperiods)
    for sdt in sampleperiods:
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
            if hours>4  or td.days>=1:
                continue
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
            T=clean1(T)
            P=cleanp(clean2(clean1(P)))
            H=clean1(H)
            T=clean2(T)
            H=clean2(H)
            u=clean2(cleanu(clean1(u)))
            u=cleanu(u)
            w=clean2(clean1(w))
            rh=clean2(clean1(RH))
            i=findvalues(H,ll)
            #print(i)
            if i==None or np.isnan(np.nanmean(u[i[0]:i[-1]])) or np.isnan(np.nanmean(lon[i[0]:i[-1]])) or np.isnan(np.nanmean(lat[i[0]:i[-1]])):
                    continue
            T2=np.nanmean(u[i[0]:i[-1]])
            pos=int(np.mean(i))
            for key in bigdick.keys():
                bigdick[key].append(np.nanmean(diccionario[key][i[0]:i[-1]]))
            dates.append(dicc['Launch Time'])

        x=bigdick['Lon']
        y=bigdick['Lat']

        #plt.figure()
        #plt.contourf(zi)
        #plt.show()
        #ax.contour(tetas,rvec,bigdick['T'])
        #levels=np.arange(10,30,0.5)

        #x=yy
    ##    plt.show()
    #    continue
        print(dates,len(dates))
        #plt.figure(figsize=(13,9))
        #counti=1
        for jj,var in enumerate(varlist.keys()):
            print(var)
            if var=='P':
                step=2
                offset=0.5
                place=222
                counti=1
                continue
            elif var=='U':
                u=bigdick[var]
                v=bigdick['V']
                step=8
                offset=4
            #    continue
            elif var =='T' or var =='W':
                step=0.5
                offset=1
                place=place+1
                counti+=1
                continue
            counter=0
            rvec=[]
            #print(len(x),len(z))
            tetas=[]
            field=[]
            z=bigdick[var]
            dr=[]
            du=[]
            dv=[]
            dtheta=[]
            for i,lon in enumerate(x):
                lat=y[i]
                r,theta=xytorth(lon,lat,track,dates[i])
                if r>350:
                    print(r,i)
                    #del z[i-counter]
                    del x[i-counter]
                    del y[i-counter]
                    del dates[i-counter]
                    counter+=1
                    continue
                else:
                    if var =='U':
                        unew,vnew=stormu(u[i],v[i],dates[i],track[3])
                        rprima=unew*np.cos(theta)+vnew*np.sin(theta)
                        tetaprima=-unew*np.sin(theta)+vnew*np.cos(theta)
                        #unew,vnew=u[i],v[i]
                        du.append(unew)
                        dv.append(vnew)
                        dr.append(rprima)
                        dtheta.append(tetaprima)
                        #continue
                        #print(unew,u[i],vnew,v[i])
                    else:
                        field.append(z[i])
                    rvec.append(r)
                    tetas.append(theta)
            #ax=plt.subplot(221,projection='polar')
            #ax.scatter(tetas,rvec)
            #plt.show()
            z=field
            dr=field
            leni=len(rvec)
            #for i in range(leni):
            #    tetas.append(tetas[i]+(2*np.pi))
            #    rvec.append(rvec[i])
            #    print(rvec)
            #    z.append(z[i])
            #rvec.append(0)
            #tetas.append(0)
        #    xi=np.linspace(np.min(rvec)-5,np.max(rvec),100)
        #    yi=np.linspace(np.min(tetas),np.max(tetas)+0.2,100)
        #    azi = griddata((np.array(tetas),np.array(rvec)), z, (yi[None,:], xi[:,None]), method='linear')
        #    radi=griddata((np.array(tetas),np.array(rvec)), dr, (yi[None,:], xi[:,None]), method='linear')4

            #for i in range(100):
#            rvec=np.append(rvec,rvec[ii])
#            tetas=np.append(tetas,tetas[ii]+(2*np.pi))
        #    print(rvec.shape)
        #    zs=[dr,z]
            #plt.figure(figsize=(13,9))
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
            xaxis,yaxis,us,vs=backtoxy(rvec,tetas,du,dv,track[3])
            #break
            #for
            #plt.figure(figsize=(12,9))
            #ax = plt.subplot(121,projection='polar')
            #levels=np.arange(-30,30,4)
            #azi = griddata((np.array(tetas),np.array(rvec)), z, (yi[None,:], xi[:,None]), method='linear')
            #CS=ax.contourf(yi,xi,azi,cmap='jet')
            #plt.colorbar(CS)
            #plt.title(var)
            #plt.show()
            #continue
            thnew=np.zeros((len(xaxis),len(yaxis)))
            rnew=np.zeros((len(xaxis),len(yaxis)))
            rprima=np.zeros((len(xaxis),len(yaxis)))
            tetaprima=np.zeros((len(xaxis),len(yaxis)))
            for i in range(100):
                for j in range(100):
                    rnew[i,j]=np.sqrt(xaxis[i]**2+yaxis[j]**2)
                    if rnew[i,j]<0:
                        print(rnew[i,j],i,j)
                    tetita=np.arctan2(yaxis[j],xaxis[i])
                    thnew[i,j]=tetita
                    rprima[i,j]=us[i,j]*np.cos(tetita)+vs[i,j]*np.sin(tetita)
                    tetaprima[i,j]=us[i,j]*np.sin(tetita)+vs[i,j]*np.cos(tetita)
            #print(thnew)
            #print(rnew)
            #plt.figure(figsize=(13,9))
            #print(place)
            #levels=np.arange(-30,30,4)
            plt.figure(figsize=(12,9))
            ax = plt.subplot(121,projection='polar')
            CS=ax.contourf(thnew,rnew,rprima,cmap='jet')
            ax.set_rlim(0,150)
            plt.colorbar(CS,fraction=0.046, pad=0.04)
            #ax = plt.subplot(122,projection='polar')
            #levels=np.arange(-40,40,4)
            ax.set_rlim(0,150)
            #CS=ax.contourf(vs,cmap='RdBu')
            #plt.colorbar(CS,fraction=0.046, pad=0.04)
            #plt.show()
            #continue

            plt.title('Radial velocity',fontsize=16)
            ax = plt.subplot(122,projection='polar')
            CS=ax.contourf(thnew,rnew,tetaprima,cmap='Spectral')
            ax.set_rlim(0,150)
            plt.title('Azimuthal velocity',fontsize=16)
            plt.colorbar(CS,fraction=0.046, pad=0.04)
            plt.suptitle(storm+' '+str(sdt)+' at 600 m')
            plt.savefig(figdir+str(sdt)+'rtheta.png')
            #plt.show()
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
            radi=griddata((np.array(tetas),np.array(rvec)), dr, (yi[None,:], xi[:,None]), method='linear')
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

        #plt.suptitle(storm+' '+str(sdt),fontsize=16)
        #plt.savefig(figdir+str(sdt)+'cylindr_.png')
        #plt.show()

        #zi = griddata((np.array(x), y), z, (xi[None,:], yi[:,None]), method='cubic')
        #try:
        #    zi = griddata((tetas,rvec), bigdick['W'], (yi[None,:], xi[:,None]), method='nearest')
        #except:
        #    print('griding killed it')

            #CS = plt.contour(xi,yi,zi,levels,linewidths=0.5,colors='k')
            #CS = plt.contourf(xi,yi,zi,levels,cmap=plt.cm.jet)
            #cbar=plt.colorbar()# draw colorbar
            #cbar.ax.set_title(varlist[var])
            #plt.title(var+' field on '+ str(sdt)+' '+ storm + ' ('+year+')',fontsize=16)
            #plt.xlabel('Longitude ',fontsize=15)
            #plt.ylabel('Latitude ',fontsize=15)
            #plt.scatter(x,y,s=3,c='k')
            #plt.grid()
            #plt.legend(title='Time',fontsize=8.5)
            #plt.savefig(figdir+str(sdt)+' '+var+storm+str(ll)+'_mixed.png')
            #plt.show()
            #plt.close()
        #
        #plt.show()
        #plt.close()
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
