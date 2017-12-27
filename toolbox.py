import numpy as np
import datetime
import pandas as pd
from scipy.interpolate import griddata
from scipy import interpolate
from math import sin, cos, sqrt, atan2, radians
import matplotlib.pyplot as plt
def distance(lat1,lon1,lat2,lon2):
# approximate radius of earth in km
	R = 6373.0

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c
	return distance
def clean1(vec):
	falseval=[9999.0,999.0,99.0,99999.0,-999.,-9999.,-99.]
	for i,v in enumerate(vec):
		if v in falseval:
			vec[i]=np.nan
	return vec
def cleanp(vec):
	for i,v in enumerate(vec):
		if v < 500 or v>1100:
			vec[i]=np.nan
	return vec
def clean2(vec):
	for i,v in enumerate(vec):
		if np.isnan(v) and i < len(vec)-1:
			if not(np.isnan(vec[i-1])) and not(np.isnan(vec[i+1])):
				vec[i]=(vec[i-1]+vec[i+1])/2.0
			elif not(np.isnan(vec[i-1])) and i>4:
				vec[i]=np.nanmean(vec[i-4:i])
	return vec
def cleanu(vec):
	for i,v in enumerate(vec):
		if np.abs(v) > np.abs(np.mean(vec)+3*np.std(vec)):
			vec[i]=np.nan
		if np.abs(v-vec[i-1]) > np.abs(1.1*np.std(vec)):
			vec[i]=np.nan
	dif=np.diff(vec)
	ii=np.where(np.abs(dif)>1)
	for i in ii:
		vec[i+1]=np.nan
	return vec
def findproperties(filename,database):
	if database=='avp':
		indexes=[-15,-7,-16,-7]
		formato='%Y-%m-%d, %H:%M:%S '
		h=6
		b=19
	elif database=='radazm':
		indexes=[2,4,5]
		formato='%Y, %m, %d, %H:%M:%S '
		h=16
		b=19
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
def getleg(lats,lons,r0):
	newlats=lats[:]
	newlongs=lons[:]
	counter=0
	for i in range(len(lats)):
		#print(newlats[i-counter],newlongs[i-counter])
		del newlats[i-counter]
		del newlongs[i-counter]
	#	print(i,counter)
		r=np.corrcoef(newlongs,newlats)
		r=r[0,1]
		print(r0,r)
		#print(newlats,lats)
		if np.abs(r0)>0.935 or len(newlats)<4:
			break
		if np.abs(r) > np.abs(r0)+0.01:
			r0=r
			counter+=1
			continue
		else:
			newlats.insert(i-counter,lats[i])
			#print(i,len(lons),len(lats))
			newlongs.insert(i-counter,lons[i])
	#print(r,len(newlats))
	return newlats,newlongs,r
def interp(H,T,tipo):
#	print(H.shape[1])
#	print(H.shape)
	if tipo == 'height':
		jump=10
	elif tipo == 'pressure':
		jump=2
	minh=50
	maxh=1500
	#print(H)
	for i in range(0,H.shape[1]):
		h=H[:,i]
		slvec=T[i,:]

		if np.nanmin(h)>minh:
			#minh=np.nanmin(h)
			slvec=np.insert(slvec,0,np.nan)
			h=np.insert(h,0,minh)
		if np.nanmax(h)<maxh:
			#maxh=np.nanmax(h)
			slvec=np.insert(slvec,-1,np.nan)
			h=np.insert(h,-1,1500)
	#	if len(h)>H.shape[0]:
			#H=np.reshape(H,(len(h),H.shape[1]))
		#H[:,i]=h
		#T[i,:]=slvec
	#print(minh,maxh)
	hnew=np.arange(50,2500,jump)
	#print(hnew1)
	#print(hnew)
	tnew=np.empty([H.shape[1],len(hnew)])
	for i in range(0,H.shape[1]):
		t=T[i,:]
		h=H[:,i]
	#	print(len(h),len(t))
		#griddata((xs, ys), u, (xaxis[None,:], yaxis[:,None]), method='cubic')
		f = interpolate.interp1d(h, t,fill_value=np.nan,bounds_error=False)
		ts=f(hnew)
		tnew[i,:]=ts
		#plt.plot(T[i,:],H[:,i])
		#plt.show()
	#	plt.plot(ts,hnew,label=str(i))
	#plt.legend()
#	plt.show()
	return hnew,tnew
#def filling2(h,vec):

def refill(h,maxr):
	if len(h)<maxr:
		counti=len(h)
		while counti<maxr:
			h=np.insert(h,counti,np.nan)
			counti+=1
	return h
def stormu(u,v,date,dicc):
	#print(type(date))
	dates=dicc['Datetime']
	for i,dt in enumerate(dates):
		dates[i]=pd.to_datetime(dt)
	us=dicc['U']
	vs=dicc['V']
#	print(us,vs)

	goodate=dates[0]
	if goodate>date:
		td=goodate-date
	else:
		td=date-goodate
	for i,dt in enumerate(dates):
		if date > dt:
			newtd=date-dt
		else:
			newtd=dt-date
		if newtd<td:
			goodate=dt
			td=newtd
			ii=i
	#print(u,v,us[ii],vs[ii])
	#x=yy
	newu=u-us[ii]
	newv=v-vs[ii]
	return newu,newv
def backtoxy(rs,thetas,u,v,trackdata):
	xs=[]
	ys=[]

	for i,r in enumerate(rs):
		xs.append(r*cos(thetas[i]))
		ys.append(r*sin(thetas[i]))
	xaxis=np.linspace(np.min(xs)-1,np.max(xs)+1,100)
	yaxis=np.linspace(np.min(ys)-1,np.max(ys)+1,100)
	uinterp = griddata((xs, ys), u, (xaxis[None,:], yaxis[:,None]), method='linear')
	vinterp = griddata((xs, ys), v, (xaxis[None,:], yaxis[:,None]), method='linear')
#	plt.scatter(xs,ys)
	#plt.colorbar()
	#plt.grid()
	#plt.show()
#	plt.contourf(xaxis,yaxis,vinterp,cmap='RdBu',levels=np.arange(np.min(v),np.max(v),1))
	#plt.colorbar()
	#plt.show()
	return xaxis,yaxis,uinterp,vinterp
def getcenter(dates,track):
	dt,traclat,traclon,dicc=track
	goodate=dt[0]
#	print(goodate,dates)
	#print(type(goodate),type(dates))
	if goodate>dates:
		td=goodate-dates
	else:
		td=dates-goodate
	for i,date in enumerate(dt):
		if date > dates:
			newtd=date-dates
		else:
			newtd=dates-date
		if newtd<td:
			goodate=date
			td=newtd
	ii=dt.index(goodate)
	return traclat[ii],traclon[ii]
def xytorth(lon,lat,track,dates):
	lat2 = radians(np.abs(lat))
	lon2 = radians(np.abs(lon))
	clat,clon=getcenter(dates,track)
	lat1=radians(np.abs(clat))
	lon1=radians(np.abs(clon))
	r=distance(lat1,lon1,lat2,lon2)
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	ry=distance(lat1,lon1,lat2,lon1)
	rx=distance(lat1,lon1,lat1,lon2)
	if dlon <0:
		rx=-rx
	if dlat <0:
		ry=-ry
   # print(rx,ry,r)
	theta=np.arctan2(ry,rx)
	if theta<0:
		theta=2*np.pi+theta
	return r,theta
	#θ = atan2(sin(Δlong)*cos(lat2), cos(lat1)*sin(lat2) − sin(lat1)*cos(lat2)*cos(Δlong))
def reshape(lat,lon,dicc):
	lon=np.array(lon)
	lat=np.array(lat)
	newdicc={}
	p=lon.argsort()
	newlon=lon[p]
	newlat=lat[p]
	for i,longi in enumerate(newlon):
		key=str(longi)+','+str(newlat[i])
		nkey=longi
		newdicc[nkey]=dicc[key]
	distances=[0]
	print(newlon,lon)
	lon0=newlon[0]
	lat0=newlat[0]
	ii=1
	while ii <= len(newlon)-1:
		lat2=newlat[ii]
		lon2=newlon[ii]
		r=distance(lat0,lon0,lat2,lon2)
		ii+=1
		distances.append(r)
	for i,r0 in enumerate(distances):
		if r0>400:
			print(r0)
			del distances[i]
			del newdicc[lon[i]]
			newlat=np.delete(newlat,i)
			newlon=np.delete(newlon,i)
#	plt.plot(distances)
	#plt.show()
	#print(distances)
	return newlat,newlon,newdicc,distances
def findvalues(z,level):
        i=0
        zi=z[i]
        index=[]
        while np.abs(zi-level)>20 or np.isnan(zi):
                i+=1
                zi=z[i]
                if i==len(z)-3:
                        return
        index.append(i)
        i+=1
        zi=z[i]

        while np.abs(zi-level)<20 or np.isnan(zi):
                index.append(i)
                i+=1
                zi=z[i]
                if i==len(z)-3:
                        return
        return index
def reassemble(r,matrix):
	print(np.nanmin(r))
	newr=np.sort(r)
	newmatrix=np.zeros(matrix.shape)
	for i,r0 in enumerate(newr):
		ii=np.where(r==r0)
		ii=ii[0][0]
		newmatrix[i,:]=matrix[ii,:]
	return newr,newmatrix
