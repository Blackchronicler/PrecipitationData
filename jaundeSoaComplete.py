# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 19:28:21 2020

@author: Ty
"""  

import os

import numpy as np
import pandas as pd
import h5py
import shutil
import glob
import matplotlib.pyplot as plt 

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from datetime import date, timedelta


### To be on the safe side, create copy of original folder      --- precautionary step ---
theSource = 'C:\\bacon...'                      # Folder to be copied
theDestination = 'C:\\bacon_backup...'              # where it should be copied to
shutil.copytree( theSource , theDestination )     # Copies entire folder and files contained in it


### Changing file extension for batch of files
os.chdir('C:\\')                      # Do Not Touch: Command initiates Directory Path

folder = "C:\\Users\..."
for filename in glob.iglob(os.path.join(folder, '*.SUB.nc4')):    #set old extension
    os.rename(filename, filename[:-8] + '')         #set new extension
   

### creating pathway links to files in a folder with python
path = "C:\\Users\..."
folder = glob.glob(os.path.join(path, '*.HDF5'))
folder_content = []

for filename in folder:
       folder_content.append(filename)
    
#print(folder_content,"\n")              # For verification purposes
#print(len(folder_content, "\n"))        # For verification purposes


files = folder_content   

### Creating a List for each of the Locations (Latidude x Longitude)
gridpoints = [[] for i in range(25)]
latidudes = []
longitudes = []

for doc in files:
    ### Reading from hdf5 file
    f = h5py.File(doc, 'r')
    #for key in f.keys():                   # checking which datasets in file
    #    print(key)
    latdata = f['lat'][()]
    londata = f['lon'][()]
    precidata = f['precipitation'][()]
    timedata = f['time'][()]

    templist = []
    rainfall = precidata[0]

    ### Iterate through 2D list to creat temporal list
    for i in range(len(rainfall)):              # iterating through rows
            for j in range(len(rainfall[i])):     # iterating through elements
                templist.append(rainfall[i][j])
                
                
    ### Creating total precipitation array/list
    x = 0
    for area in gridpoints:
        area.append(templist[x])
        x += 1
    f.close()                   # closing each file after it has been read
             
#print("This is total precipitation for each of the 25 locations:" "\n")
#print(locations, "\n")
#print(len(locations), "\n")         # printing the length of the list

#for x in range(len(locations)):           # printing the length 
#    print(len(locations[x]), "\n")       # of each location array

### Setting up timeseries
sdate = date(2000,6,1)   # start date
edate = date(2020,8,31)   # end date

mydates = pd.date_range(sdate, edate, freq = "M" ).tolist()     # freq = monthly
#print(mydates)                               # For verification purposes
#print(len(mydates))                          # For verification purposes

### Visualisation
time = mydates                  # Time series, x-axis
precipitation = gridpoints       # rainfall, y-axis
#print(len(precipitation[0]))         # For verification purposes
#print(len(time))                    # For verification purposes

plt.xlabel("Zeit")
plt.ylabel("Niederschlag")
plt.title("Klimadiagramm Soa (2000-2020)")

### To plot one Gridpoint activate this
plt.plot(time,precipitation[6],linewidth=1,label = 'id %s'%i, color="orange")

### To plot all Gridpoints activate this
#for rainfall in range(len(precipitation)):
#        plt.plot(time,precipitation[rainfall],linewidth=1,label = 'id %s'%i)
        
plt.legend()
plt.show()

