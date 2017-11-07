import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import os,sys
import datetime
import glob
#def gettingdays(filelist)
figdir='/home/jlgf/Documents/MRes/Project/figs/'
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
maindir='/home/jlgf/Documents/MRes/Project/Data/'
stormcount=0
valuablecount=0
for i in range(1996,2013):
    year=str(i)
    yrdir=maindir+year+'/'
    stdirs=os.listdir(yrdir)
    for storm in stdirs:
        stormcount+=1
        daylist=[]
        sampleperiods=[]
        counter1=0
        counter2=0
        filelist=glob.glob(yrdir+storm+'/gps.qc.eol/GIV/*')
        filelist2=glob.glob(yrdir+storm+'/gps.qc.eol/P-3.43/*')
        #filelist=filelist+filelist2
        #print(filelist)

#import sbprocess
#print(subprocess.run(['ls', '-l'], stdout=subprocess.PIPE).stdout.decode('utf-8'))
        filelist3=glob.glob(yrdir+storm+'/ublox.qc.eol/P-3.43/*')
        filelist4=glob.glob(yrdir+storm+'/ublox.qc.eol/GIV/*')
        filelist5=glob.glob(yrdir+storm+'/ublox.qc.eol/P-3.42/*')
        if i >= 2011:
            filelist=glob.glob(yrdir+storm+'/ublox.qc.eol/noaa.P-3/*')
            filelist2=glob.glob(yrdir+storm+'/ublox.qc.eol/noaa.GIV/*')
        filelist=filelist+filelist2+filelist3+filelist4+filelist5
        for filename in filelist:
            counter1+=1
            dicc=findproperties(filename,'radazm')
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
                    if hours > 2:
                        counti+=1
                if counti==len(sampleperiods):
                    sampleperiods.append(dicc['Launch Time'])
            if d not in daylist:
                counter2+=1
                daylist.append(d)
        if counter1>90 and len(sampleperiods) >6:
            valuablecount+=1
        print(storm+' '+year)
        print('Archivos totales ='+str(counter1))
        print('Dias medicion ='+str(counter2))
        print('Periodos de muestreo ='+str(len(sampleperiods)))
print(stormcount)
print(valuablecount)
