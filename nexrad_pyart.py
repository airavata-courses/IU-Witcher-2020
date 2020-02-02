#import libraries for radar visualization
import numpy as np
import datetime
import pyart
import boto
import os
import tempfile
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
#suppress deprecation warnings
import warnings
warnings.simplefilter("ignore", category=DeprecationWarning)

#save the nexrad locations to an array from the PyART library
locs = pyart.io.nexrad_common.NEXRAD_LOCATIONS
#set up the figure for plotting
fig = plt.figure(figsize=(12,8),dpi=100)
ax = fig.add_subplot(111)
#create a basemap for CONUS
m = Basemap(projection='lcc',lon_0=-95,lat_0=35.,
           llcrnrlat=20,urcrnrlat=50,llcrnrlon=-120,
           urcrnrlon=-60, resolution='l')
#draw the geography for the basemap
m.drawcoastlines(linewidth=1)
m.drawcountries(linewidth=1)
m.drawstates(linewidth=0.5)
#plot a point and a label for each of the radar site locations within the CONUS domain
for key in locs:
    lon = locs[key]['lon']
    lat = locs[key]['lat']
    name = key
    if lon >= -120 and lon <= -60 and lat >= 20 and lat <= 50:
        m.scatter(lon,lat,marker='o', color='b',latlon=True)
        x,y = m(lon+0.2,lat+0.2)
        plt.text(x,y,name,color='k',fontsize=7)
#create a figure title
fig.text(0.5,0.92, 'CONUS NEXRAD locations',horizontalalignment='center')
plt.show()

site = 'KIND'

#get the radar location (this is used to set up the basemap and plotting grid)
loc = pyart.io.nexrad_common.get_nexrad_location(site)
lon0 = loc[1] ; lat0 = loc[0]
#use boto to connect to the AWS nexrad holdings directory
s3conn = boto.connect_s3()
bucket = s3conn.get_bucket('noaa-nexrad-level2')
#create a datetime object for the current time in UTC and use the
# year, month, and day to drill down into the NEXRAD directory structure.
now = datetime.datetime.utcnow()
date = ("{:4d}".format(now.year) + '/' + "{:02d}".format(now.month) + '/' +
        "{:2d}".format(now.day) + '/')
#get the bucket list for the selected date
#Note: this returns a list of all of the radar sites with data for
# the selected date
date = "2020/01/30"
ls = bucket.list(prefix=date)
for key in ls:
    #only pull the data and save the arrays for the site we want
    temp = key.name.split('/')
    if site in temp:
        print("Site: ", site)
        #set up the path to the NEXRAD files
        path = date + '/' + site + '/' + site
        #grab the last file in the file list
        print(path)
        fname = bucket.get_all_keys(prefix=path)[-1]
        print(fname)
        #get the file
        s3key = bucket.get_key(fname)
        #save a temporary file to the local host
        localfile = tempfile.NamedTemporaryFile(delete=False)
        print(localfile.name)
        #write the contents of the NEXRAD file to the temporary file
        s3key.get_contents_to_filename(localfile.name)
        print("after s3")
        #use the read_nexrad_archive function from PyART to read in NEXRAD file
        radar = pyart.io.read_nexrad_archive(localfile.name)
        #get the date and time from the radar file for plot enhancement
        time = radar.time['units'].split(' ')[-1].split('T')
        print(site + ': ' + time[0] + ' at ' + time[1] )

        #set up the plotting grid for the data
        display = pyart.graph.RadarMapDisplay(radar)
        x,y = display._get_x_y(0,True,None)

#set up a 1x1 figure for plotting
fig, axes = plt.subplots(nrows=1,ncols=1,figsize=(9,9),dpi=100)
#set up a basemap with a lambert conformal projection centered
# on the radar location, extending 1 degree in the meridional direction
# and 1.5 degrees in the longitudinal in each direction away from the
# center point.
m = Basemap(projection='lcc',lon_0=lon0,lat_0=lat0,
           llcrnrlat=lat0-1.25,llcrnrlon=lon0-1.5,
           urcrnrlat=lat0+1.25,urcrnrlon=lon0+1.5,resolution='h')

#get the plotting grid into lat/lon coordinates
x0,y0 = m(lon0,lat0)
glons,glats = m((x0+x*1000.), (y0+y*1000.),inverse=True)
#read in the lowest scan angle reflectivity field in the NEXRAD file
refl = np.squeeze(radar.get_field(sweep=0,field_name='reflectivity'))
#set up the plotting parameters (NWSReflectivity colormap, contour levels,
# and colorbar tick labels)
cmap = 'pyart_NWSRef'
levs = np.linspace(0,80,41,endpoint=True)
ticks = np.linspace(0,80,9,endpoint=True)
label = 'Radar Reflectivity Factor ($\mathsf{dBZ}$)'
#define the plot axis to the be axis defined above
ax = axes
#normalize the colormap based on the levels provided above
norm = mpl.colors.BoundaryNorm(levs,256)
#create a colormesh of the reflectivity using with the plot settings defined above
cs = m.pcolormesh(glons,glats,refl,norm=norm,cmap=cmap,ax=ax,latlon=True)
#add geographic boundaries and lat/lon labels
m.drawparallels(np.arange(20,70,0.5),labels=[1,0,0,0],fontsize=12,
                color='k',ax=ax,linewidth=0.001)
m.drawmeridians(np.arange(-150,-50,1),labels=[0,0,1,0],fontsize=12,
               color='k',ax=ax,linewidth=0.001)
m.drawcounties(linewidth=0.5,color='gray',ax=ax)
m.drawstates(linewidth=1.5,color='k',ax=ax)
m.drawcoastlines(linewidth=1.5,color='k',ax=ax)
#mark the radar location with a black dot
m.scatter(lon0,lat0,marker='o',s=20,color='k',ax=ax,latlon=True)
#add the colorbar axes and create the colorbar based on the settings above
cax = fig.add_axes([0.075,0.075,0.85,0.025])
cbar = plt.colorbar(cs,ticks=ticks,norm=norm,cax=cax,orientation='horizontal')
cbar.set_label(label,fontsize=12)
cbar.ax.tick_params(labelsize=11)
#add a title to the figure
fig.text(0.5,0.92, site + ' (0.5$^{\circ}$) Reflectivity\n ' +
        time[0] + ' at ' + time[1],horizontalalignment='center',fontsize=16)
#display the figure
plt.show()
