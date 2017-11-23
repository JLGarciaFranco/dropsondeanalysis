import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import os
import datetime
import glob
import sys
from vcsections import *
from hcrossections import *
from flightdata import getrack
#def gettingdays(filelist)
figdir='/home/jlgf/Documents/MRes/Project/figs/'
year=input("What year is your storm? ")
os.system('ls ../Data/'+year+'/')
storm=input("What storm are you looking for? ")
if int(year)>2012:
    downloadtype='avp'
else:
    downloadtype='radazm'
if downloadtype == 'radazm':
    filelist=glob.glob('../Data/'+year+'/'+storm+'/gps.qc.eol/4GIV/*')
    filelist6=glob.glob('../Data/'+year+'/'+storm+'/ublox.qc.eol/4GIV/*')
    filelist2=glob.glob('../Data/'+year+'/'+storm+'/gps.qc.eol/P-3.43/*')
    filelist3=glob.glob('../Data/'+year+'/'+storm+'/ublox.qc.eol/P-3.43/*')
    filelist4=glob.glob('../Data/'+year+'/'+storm+'/ublox.qc.eol/noaa.P-3/*')
    filelist5=glob.glob('../Data/'+year+'/'+storm+'/ublox.qc.eol/P-23.42/*')
    filelist=filelist+filelist2+filelist5+filelist3+filelist4+filelist6
elif downloadtype =='avp':
    filelist=glob.glob('../Data/'+year+'/'+storm+'/*')
track=getrack(storm,year)
print(track[0])
filelist=np.sort(filelist)
os.system('mkdir ../figs/'+storm)
#vsection(filelist,downloadtype)
hsection(filelist,downloadtype,storm)
