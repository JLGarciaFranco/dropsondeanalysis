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
def vsection(filelist,end):
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
	sampleperiods=[]
	daylist=[]
	for filename in filelist:
		print(filename)
		storm=filename.split('/')[3]
		dicc=findproperties(filename,end)
		d=dicc['Launch Time'].day
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
				hours, remainder = divmod(td.seconds, 3600)
				if hours > 4:
					counti+=1
			if counti==len(sampleperiods):
				sampleperiods.append(dicc['Launch Time'])
		if d not in daylist:
			daylist.append(d)
	print(sampleperiods)
	for sdt in sampleperiods:
		lats=[]
		lons=[]
		for filename in filelist:
			dicc=findproperties(filename,end)
			d=dicc['Launch Time'].day
			if dicc['Launch Time']>sdt:
				td=dicc['Launch Time']-sdt
			else:
				td=sdt-dicc['Launch Time']
			hours, remainder = divmod(td.seconds, 3600)
			if hours < 2:
				nump=np.genfromtxt(filename,skip_header=head,skip_footer=foot)
				print(filename)
				lon=nump[:,longindex]
				lat=nump[:,latindex]
				lon=clean2(clean1(lon))
				lat=clean2(clean1(lat))
				mlon=np.nanmean(lon)
				mlat=np.nanmean(lat)
				lats.append(mlat)
				lons.append(mlon)
			#	print(nump[-1])

		r=np.corrcoef(lons,lats)
		r=r[0,1]
		print(r,len(lats))
		lats,lons,r=getleg(lats,lons,r)

		if np.abs(r)<0.8549:
			print('r failure')
			continue
		print("Trying to plot")
		#plt.scatter(lats,lons)
		#plt.title(sdt)
		#plt.show()
		latlon={}
		hs={}
		x=np.array([])
		y=[]
		maxr=10
		for filename in filelist:
				dicc=findproperties(filename,end)
				d=dicc['Launch Time'].day
				if dicc['Launch Time']>sdt:
					td=dicc['Launch Time']-sdt
				else:
					td=sdt-dicc['Launch Time']
				hours, remainder = divmod(td.seconds, 3600)
				nump=np.genfromtxt(filename,skip_header=head,skip_footer=foot)
				print(nump.shape)
				print(filename)
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
					print('Cleaning u')

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
				if mlat not in lats and mlon not in lons:
					continue
				lati=np.around(mlat,3)
				longi=np.around(mlon,3)
				y.append(lati)
				x=np.append(x,longi)
			#	print(nump[-1])
				T=clean1(T)
				P=clean2(cleanu(cleanp(clean1(P))))
				H0=clean1(H)
				T=cleanu(clean2(T))

				H=clean2(H0)
				u=clean2(cleanu(clean1(u)))
				w=cleanu(clean2(clean1(w)))
				#plt.plot(w)
				#plt.show()
				rh=clean2(clean1(RH))
				#print(len(H))
				#plt.plot(u)
				#H,u,w,rh,T=finalclean(H,u,w,rh,T)
				#print(len(T))
				if len(T)>maxr:
					maxr=len(T)
				#plt.plot(T)
				#plt.show()
				latlon[str(longi)+','+str(lati)]=np.array([T,w,rh,H,u,P,v])
		if len(x)==0:
			continue
		lats,lons,latlon,xs=reshape(y,x,latlon)
		H=np.empty([maxr,len(latlon.keys())])
		#H=np.empty([len(T),len(latlon.keys())])
		T=np.empty([len(latlon.keys()),maxr])
		rh=np.empty([len(latlon.keys()),maxr])
		w=np.empty([len(latlon.keys()),maxr])
		u=np.empty([len(latlon.keys()),maxr])
		v=np.empty([len(latlon.keys()),maxr])
		P=np.empty([len(latlon.keys()),maxr])
		for i,key in enumerate(latlon.keys()):
			h=latlon[key][3]
			h=refill(h,maxr)
			H[:,i]=h
			T[i,:]=refill(latlon[key][0],maxr)
			rh[i,:]=refill(latlon[key][2],maxr)
			w[i,:]=refill(latlon[key][1],maxr)
			u[i,:]=refill(latlon[key][4],maxr)
			P[i,:]=refill(latlon[key][5],maxr)
			v[i:,]=refill(latlon[key][6],maxr)
		#plt.contourf(P)
		#plt.show()
		h,rhh=interp(H,rh,'height')

		h,P0=interp(H,P,'height')
	#	plt.contour(w)
	#S	h,w=interp(H,u)
		if len(h)==0:
			continue
		print(len(lons),len(latlon.keys()))
	#	plt.contour(w)
	#	plt.show()
		fig,axarr=plt.subplots(2,2,figsize=(12,16))
		xs=np.array(xs)
		print(xs.shape,h.shape,P0.T.shape)
		X,Y=np.meshgrid(xs,h)
		xi=np.linspace(np.nanmin(xs),np.max(xs))
		yi=np.linspace(np.nanmin(h),np.nanmax(h))
		XI,YI=np.meshgrid(xi,yi)
		#zi = LinearNDInterpolator
		#f = interpolate.interp2d(xs, h, P0.T, kind='cubic')
		#zi=f(xi,yi)
		print(np.min(P0),np.nanmax(P0))
		#zi = griddata(xs,h,P0.T,xi,yi)
		#f = interpolate.interp2d(x, y, P0.T, kind='cubic')
		#znew=f(xi,yi)
		#c1=axarr[0].contourf(xi,yi,zi,cmap=plt.cm.jet,levels=np.arange(np.nanmin(zi),np.nanmax(zi),1))
		c1=axarr[0,0].contourf(X,Y,P0.T,cmap=plt.cm.jet,levels=np.arange(np.nanmin(P0),np.nanmax(P0),1))
		for i in range(0,len(xs)):
			for j in range(0,len(h),10):
				pval=P0[i,j]
				print(pval)
				ur=u[i,np.where(np.abs(P[i,:]-pval)<0.25)[0]]
				vr=v[i,np.where(np.abs(P[i,:]-pval)<0.25)[0]]
				ur=np.nanmean(ur)
				vr=np.nanmean(vr)
				if ur > 100 or vr >100:
					continue
				if i==0:
					offset=10
				elif i==len(xs)-1:
					offset=-10
				else:
					offset=0
				axarr[0,0].barbs(xs[i]+offset,h[j],ur,vr)
		for i,xc in enumerate(xs):
			axarr[0,0].axvline(x=xc)
		axarr[0,0].set_xlim([0,xs[-1]])
		axarr[0,0].set_ylim([np.min(h),h[-1]])
			#axarr[0,0].barbs(H,u,v)
		p,T=interp(P.T,T,'pressure')
		#plt.contourf(T)
		#plt.show()
		axarr[0,0].set_title('Pressure')
		#axarr[0,0].set_xlabel('Distance')
		axarr[0,0].set_ylabel('Geopotential Height (m)')
	#	f = interpolate.interp2d(xs, p, T.T, kind='cubic')
		#xi=np.linspace(np.nanmin(xs),np.max(xs))
		#yi=np.linspace(np.nanmin(p),np.nanmax(p))
		#zi=f(xi,yi)
		X,Y=np.meshgrid(xs,p)
		c2=axarr[0, 1].contourf(xs, p, T.T,cmap='coolwarm',levels=np.arange(np.nanmin(T),np.nanmax(T),0.1))
		axarr[0,1].set_title('Temperature')
		#axarr[0,1].set_xlabel('Distance')
		axarr[0,1].set_ylabel('Pressure (hPa)')
		p,rh=interp(P.T,rh,'pressure')
		X,Y=np.meshgrid(xs,p)
		#f = interpolate.interp2d(xs, p, rh.T, kind='cubic')
		#yi=np.linspace(np.nanmin(p),np.nanmax(p))
		#zi=f(xi,yi)
		c3=axarr[1, 0].contourf(X,Y,rh.T,cmap="Spectral",levels=np.arange(np.nanmin(rh),np.nanmax(rh),1))
		axarr[1,0].set_title('Relative Humidity')
		axarr[1,0].set_xlabel('Distance')
		axarr[1,0].set_ylabel('Pressure (hPa)')
		p,w=interp(P.T,w,'pressure')
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

		plt.suptitle(storm+' '+str(sdt),fontsize=18)

		plt.tight_layout()
		fig.subplots_adjust(top=0.925)
		plt.show()
	#	print(type(np.array(x)),H[:,0].shape,T.shape)
