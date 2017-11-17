import numpy as np
import datetime
from scipy import interpolate
from math import sin, cos, sqrt, atan2, radians
import matplotlib.pyplot as plt
def distance(lat1,lon1,lat2,lon2):
# approximate radius of earth in km
	R = 6373.0

	lat1 = radians(np.abs(lat1))
	lon1 = radians(np.abs(lon1))
	lat2 = radians(np.abs(lat2))
	lon2 = radians(np.abs(lon2))

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c

#	print("Result:", distance)
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
	print(H.shape)
	if tipo == 'height':
		jump=10
	elif tipo == 'pressure':
		jump=2
	minh=0
	maxh=10000
	for i in range(0,H.shape[1]):
		h=H[:,i]
		if np.nanmin(h)>minh:
			minh=np.nanmin(h)
		if np.nanmax(h)<maxh:
			maxh=np.nanmax(h)
	hnew=np.arange(minh,maxh,jump)
	print(hnew)
#	print(hnew)
	tnew=np.empty([H.shape[1],len(hnew)])
	for i in range(0,H.shape[1]):
		t=T[i,:]
		h=H[:,i]
	#	print(len(h),len(t))
		f = interpolate.interp1d(h, t)
		ts=f(hnew)
		tnew[i,:]=ts
	#	plt.plot(T[i,:],H[:,i])
		#plt.show()
		#plt.plot(ts,hnew,label=str(i))
	#plt.legend()
	#plt.show()
	return hnew,tnew
def refill(h,maxr):
	if len(h)<maxr:
		counti=len(h)
		while counti<maxr:
			h=np.insert(h,counti,np.nan)
			counti+=1
	return h
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
		if r0>300:
			print(r0)
			del distances[i]
			del newdicc[lon[i]]
			newlat=np.delete(newlat,i)
			newlon=np.delete(newlon,i)
	plt.plot(distances)
	plt.show()
	print(distances)
	return newlat,newlon,newdicc,distances
