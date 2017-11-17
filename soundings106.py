import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import os
import datetime
import glob
import sys
from vcsections import *
#def gettingdays(filelist)
figdir='/home/jlgf/Documents/MRes/Project/figs/'
year=input("What year is your storm? ")
os.system('ls ../Data/'+year+'/')
storm=input("What storm are you looking for? ")
downloadtype=input('Is your storm part of historical data or individual download? (radazm or avp files)? ')
if downloadtype == 'radazm':
    filelist=glob.glob('../Data/'+year+'/'+storm+'/gps.qc.eol/GsIV/*')
    filelist2=glob.glob('../Data/'+year+'/'+storm+'/gps.qc.eol/P-3.43/*')
    filelist3=glob.glob('../Data/'+year+'/'+storm+'/ublox.qc.eol/P-3.43/*')
    filelist4=glob.glob('../Data/'+year+'/'+storm+'/ublox.qc.eol/noaa.P-3/*')
    filelist5=glob.glob('../Data/'+year+'/'+storm+'/ublox.qc.eol/P-3.42/*')
    filelist=filelist+filelist2+filelist5+filelist3+filelist4
elif downloadtype =='avp':
    filelist=glob.glob('../Data/'+year+'/'+storm+'/*')
filelist=np.sort(filelist)
os.system('mkdir ../figs/'+storm)
vsection(filelist,downloadtype)
