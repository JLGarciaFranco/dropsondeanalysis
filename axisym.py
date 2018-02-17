import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime
import glob
import sys
import metpy
from scipy.interpolate import griddata
from toolbox import *
def axics(filelist,end,track,storm):
	filelist=np.sort(filelist)
	figdir='/home/jlgf/Documents/MRes/Project/figs/'
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
	sampleperiods=[]
	daylist=[]
	for filename in filelist:
		print(filename)
		storm=filename.split('/')[3]
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
				hours, remainder = divmod(td.seconds, 3600)
				if hours > 5 or td.days>=1:
					counti+=1
			if counti==len(sampleperiods):
				sampleperiods.append(dicc['Launch Time'])
		if d not in daylist:
			daylist.append(d)
	sampleperiods=[datetime.datetime(2010,8,28,2,0,0),datetime.datetime(2010,8,31,16,0,0),datetime.datetime(2010,8,29,14,0,0),datetime.datetime(2010,8,30,6,0,0),datetime.datetime(2010,8,31,6,0,0),datetime.datetime(2010,9,1,6,0,0),datetime.datetime(2010,9,2,6,0,0),datetime.datetime(2010,9,3,6,0,0),datetime.datetime(2010,9,4,6,0,0)]
	for ixi in range(len(sampleperiods)-1):
		sdt=sampleperiods[ixi]
		#nsdt=sampleperiods[ixi+1]

		lats=[]
		lons=[]
		rmaxis=[]
		latlon={}
		hs={}
		x=np.array([])
		y=[]
		dates=[]
		maxr=10
		for filename in filelist:
				dicc=findproperties(filename,end)
				d=dicc['Launch Time'].day
				#if dicc['Launch Time']<sdt-datetime.timedelta(hours=5) or dicc['Launch Time'] > sdt+datetime.timedelta(hours=5):
					#print(dicc['Launch Time'],sdt)
					#continue
				nump=np.genfromtxt(filename,skip_header=head,skip_footer=foot)
				if end =='avp':
					lon=nump[:,11]
					lat=nump[:,12]
					T=nump[:,6]
					P=nump[:,5]
					H=nump[:,13]
					RH=nump[:,7]
					ur=nump[:,9]
					udir=nump[:,8]
					u=-ur*np.sin(np.pi*udir/180)
					v=-ur*np.cos(np.pi*udir/180)
					w=nump[:,10]
				elif end == 'radazm':
					T=nump[:,5]
					P=nump[:,4]
					H=nump[:,13]
					RH=nump[:,7]
					u=nump[:,8]
					v=nump[:,9]
					udir=nump[:,11]
					w=nump[:,10]
					lon=nump[:,14]
					lat=nump[:,15]
					v=clean2(cleanu(clean1(v)))
				lon=clean2(clean1(lon))
				lat=clean2(clean1(lat))
				mlon=np.nanmean(lon)
				mlat=np.nanmean(lat)
				lati=np.around(mlat,4)
				longi=np.around(mlon,4)
				if np.isnan(lati) or np.isnan(longi) or lati in y or longi in x:
					print('NaN')
					continue
				#print(mlon,mlat)
				r,theta=xytorth(mlon,mlat,track,dicc['Launch Time'])
				if r>220:
					continue
				print(filename)
				rms=track[3]['Rmax']
				ris=0
				counti=0
				for i,key in enumerate(rms):
					if key>dicc['Launch Time']-datetime.timedelta(hours=5) and key<dicc['Launch Time']+datetime.timedelta(hours=5):
						ris+=rms[key]
						counti+=1
						rmax=ris/counti
				y.append(lati)
				x=np.append(x,longi)
				rmaxis.append(rmax)
				dates.append(dicc['Launch Time'])
				T=clean1(T)
				P=clean2(cleanu(cleanp(clean1(P))))
				H0=clean1(H)
				T=cleanu(clean2(T))
				H=clean2(H0)
				u=clean2(cleanu(clean1(u)))
				w=cleanu(clean2(clean1(w)))
				rh=clean2(clean1(RH))
				if len(T)>maxr:
					maxr=len(T)
				latlon[str(longi)+','+str(lati)]=np.array([T,w,rh,H,u,P,v,lon,lat])
		print('end of filelist loop')
		if len(x)<+4:
			continue
		xs=[]
		print('going to get radial')
		for i,lon in enumerate(x):
			r,theta=xytorth(lon,y[i],track,dates[i])
			xs.append(r/rmaxis[i])
		H=np.empty([maxr,len(latlon.keys())])
		T=np.empty([len(latlon.keys()),maxr])
		rh=np.empty([len(latlon.keys()),maxr])
		w=np.empty([len(latlon.keys()),maxr])
		u=np.empty([len(latlon.keys()),maxr])
		v=np.empty([len(latlon.keys()),maxr])
		latitudes=np.empty([len(latlon.keys()),maxr])
		longitudes=np.empty([len(latlon.keys()),maxr])
		P=np.empty([len(latlon.keys()),maxr])
		Rad=np.empty([len(latlon.keys()),maxr])
		TH=np.empty([len(latlon.keys()),maxr])
		for i,key in enumerate(latlon.keys()):
			h=latlon[key][3]
			h=refill(h,maxr)
			H[:,i]=h
			T[i,:]=refill(latlon[key][0],maxr)
			rh[i,:]=refill(latlon[key][2],maxr)
			w[i,:]=refill(latlon[key][1],maxr)
			u[i,:]=refill(latlon[key][4],maxr)
			P[i,:]=refill(latlon[key][5],maxr)
			v[i,:]=refill(latlon[key][6],maxr)
			latitudes[i,:]=refill(latlon[key][8],maxr)
			longitudes[i,:]=refill(latlon[key][7],maxr)
		xs=np.array(xs)

		del(latlon)
		for i,lon in enumerate(x):
			#print(i)
			for j in range(u.shape[1]):
				r,theta=xytorth(longitudes[i,j],latitudes[i,j],track,dates[i])
				unew,vnew=stormu(u[i,j],v[i,j],dates[i],track[3])
				#unew,vnew=u[i,j],v[i,j]
				rprima=unew*np.cos(theta)+vnew*np.sin(theta)
				tetaprima=-unew*np.sin(theta)+vnew*np.cos(theta)
				Rad[i,j]=rprima
				TH[i,j]=tetaprima
		print('going to interpolate')
		h,P0=interp(H,Rad,'height')
		#print("Longitud de h: "+str(len(h)))
		#print(np.nanmin(xs))
		xs=np.array(xs)
		xr,P0=reassemble(xs,P0,h)
		X,Y=np.meshgrid(xs,h)
		xi=np.linspace(0,200,110)
		yi=np.linspace(0,np.max(h),100)
		XI,YI=np.meshgrid(xi,yi)
		#f = interpolate.interp2d(xr, h, P0.T)
		#zi=f(xi,yi)
		#plt.contourf(xi,yi,zi,cmap='jet')
		#plt.colorbar()
		#plt.show()
		fig,axarr=plt.subplots(3,1,figsize=(12,12))
		#print(np.nanmax(xs)-np.nanmin(xs))
		if np.nanmax(P0.T)>70:
			maxlev=40
		else:
			maxlev=np.nanmax(P0.T)
		if np.nanmin(P0.T)<-70:
			mini=-30
		else:
			mini=np.nanmin(P0.T)
		c1=axarr[0].contourf(xr,h,P0.T,cmap='seismic',levels=np.linspace(-30,30,25))
		p,T=interp(H,TH,'height')
		xr,T=reassemble(xs,T,h)
		axarr[0].set_title('Radial velocity')
		#axarr[0,0].set_xlabel('Distance')
		axarr[0].set_ylabel('Height (m)')
	#	axarr[0].set_xlabel('Radius (km)')
		axarr[0].set_xlim([0,3])
		X,Y=np.meshgrid(xr,p)
		if np.nanmax(T.T)>60:
			maxlev=50
		else:
			maxlev=np.nanmax(T.T)
		c2=axarr[1].contourf(xr,p,T.T,cmap='rainbow',levels=np.linspace(-2,np.nanmax(T.T),25))
		axarr[1].set_title('Azimuthal')
		#axarr[1].set_xlabel('Radius (km)')
		axarr[1].set_xlim([0,3])
		axarr[1].set_ylabel('Height [m]')
		axarr[0].set_xlim([0,3])
		fig.colorbar(c1, ax=axarr[0],label='m/s')
		fig.colorbar(c2, ax=axarr[1],label=r'm/s')
		p,w=interp(H,w,'height')
		xr,P0=reassemble(xs,w,h)
		#f = interpolate.interp2d(xs, p, w.T, kind='cubic')
		#yi=np.linspace(np.nanmin(p),np.nanmax(p))
		#zi=f(xi,yi)
		X,Y=np.meshgrid(xr,p)
		if np.nanmax(P0.T)>100:
				maxlev=40
		else:
				maxlev=np.nanmax(P0.T)
		c3=axarr[2].contourf(xr,p,P0.T,cmap='gist_ncar',levels=np.linspace(0,np.nanmax(P0.T),25))
		fig.colorbar(c3, ax=axarr[2],label='m/s')
		axarr[2].set_title('Vertical wind speed')
		axarr[2].set_xlabel('Radius (km)')
		axarr[2].set_xlim([0,3])
		axarr[2].set_ylabel('Height [m]')
	#	plt.suptitle(storm+' '+str(sdt)+'-'+str(nsdt),fontsize=16)
		#plt.savefig(figdir+storm+'/axisym/'+str(sdt)+'vsection.png')
		plt.show()
		#x=yy
		continue
		p,rh=interp(H,rh,'height')
		X,Y=np.meshgrid(xs,p)
		c3=axarr[1, 0].contourf(X,Y,rh.T,cmap="Spectral",levels=np.arange(72,100,1))
		axarr[1,0].set_title('Relative Humidity')

		axarr[1,0].set_xlabel('Distance')
		axarr[1,0].set_ylabel('Pressure (hPa)')
		p,w=interp(H,w,'height')
		#f = interpolate.interp2d(xs, p, w.T, kind='cubic')
		#yi=np.linspace(np.nanmin(p),np.nanmax(p))
		#zi=f(xi,yi)
		X,Y=np.meshgrid(xs,p)
		c4=axarr[1, 1].contourf(X,Y,w.T,cmap=plt.cm.jet,levels=np.arange(np.nanmin(w),np.nanmax(w),0.25))
		fig.colorbar(c1, ax=axarr[0,0],label='hPa')
		fig.colorbar(c2, ax=axarr[0,1],label=r'$\degree$ C')
		fig.colorbar(c3, ax=axarr[1,0],label='\%')
		fig.colorbar(c4, ax=axarr[1,1],label='m/s')
		axarr[1,1].set_title('Vertical speed')
		axarr[1,1].set_xlabel('Distance')
		axarr[1,1].set_ylabel('Pressure (hPa)')
		#axarr[1].set_title('Original')
		#axarr[0].set_title('Interpolated')
		plt.tight_layout()
		plt.suptitle(storm+' '+str(sdt),fontsize=18)

		plt.tight_layout()
		fig.subplots_adjust(top=0.925)
		plt.savefig(figdir+storm+'/'+str(sdt)+'vsection.png')
	#	plt.show()
