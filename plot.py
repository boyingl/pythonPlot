import pandas as pd
import math
import numpy as np
from matplotlib import pyplot
from shapely.geometry.polygon import LinearRing, Polygon
import shapely.ops as so

def point_inside_polygon(x,y,poly):

    n = len(poly)
    inside =False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

data = pd.read_csv("geographic.csv", header=0)
df = pd.DataFrame(data)


color = ['b','g','r','c','m','y','b']
colorCount = 0
polygons = []
zoneCordList = []
for i in list(data.columns):
  l = list(df[i])
  #print(l)
  cordList = []
  for i in range(len(l) - 1):
    if i%2 == 0:
      if not np.isnan(l[i]):
        cord = l[i], l[i+1];
        cordList.append(cord)
      i = i + 1

  zoneCordList.append(cordList)
  #construct
  polygons.append(Polygon(cordList))


fig = pyplot.figure()
for i in polygons:
  xs, ys = i.exterior.xy

  # plot it
  axs = pyplot.subplot(1,1,1)
  axs.fill(xs, ys, alpha=0.5, fc=color[colorCount%7], ec='none')
  colorCount = colorCount + 1
pyplot.show()  # if not interactive

#count uber 2014 in different region
dataUber2014 = pd.read_csv("uber_trips_2014.csv", header=0)
dfUber2014 = pd.DataFrame(dataUber2014)

longitude = list(dfUber2014['pickup_longitude'])
latitude = list(dfUber2014['pickup_latitude'])

uberPickup = dict()

for a in range(len(longitude)):
    count = -1
    for i in zoneCordList:
      count += 1
      if point_inside_polygon(longitude[a], latitude[a], i):
        if count in uberPickup.keys():
            uberPickup[data.columns[count]] += 1
        else:
            uberPickup[data.columns[count]] = 1
        break

print(uberPickup)

pyplot.bar(range(len(uberPickup)), uberPickup.values(), align='center')
pyplot.xticks(range(len(uberPickup)), uberPickup.keys())

pyplot.show()
