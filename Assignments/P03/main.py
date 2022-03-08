import csv
import json
import geopandas
import numpy as np
from numpy import sort
from shapely.geometry import Point


import matplotlib.pyplot as plt
from shapely.ops import unary_union
from geovoronoi import voronoi_regions_from_coords, points_to_coords
from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys_with_points_in_area

with open('cities.json') as f:
    cities = json.load(f)

coord = []
cityNames = []

#makes the outline for points as well as keys for city names
for feature in cities["features"]:
    if feature["geometry"]["type"] == "Point":
        coord.append(feature["geometry"]["coordinates"])
        cityNames.append(feature['properties']['city'])

#Makes sure the lists were formatted corrrectly
print(cityNames)
print("-----"*700)
print(coord)

#list that contains the point conversions for the coordinates
cities = []
for points in coord:
    cities.append(Point(points))



#makes geo series from all the cities geo points 
geoseries = geopandas.GeoSeries(cities)


#Contains the city dictionary results 
city_dict = []

#Num of elements to iterate over
series_len = len(geoseries)

for i in range(series_len):

    distances= []
    #Returns a Series containing the distance to aligned other
    array = geoseries.distance(geoseries[i])

    #Puts the distances in array
    array = array.values 
    array_len = len(array)


    #Appends distances from iterated city in list
    for j in range(array_len):
        if array[j] != 0:
            #makes tuple to store all distances
            distances.append((cityNames[j], array[j]))

    #sorts the nearest cities
    distances.sort(key= lambda x: x[1])


    #Creates city dictionary
    city = {
        'city': cityNames[i],
        'longitude': geoseries[i].x,
        'latitude': geoseries[i].y,
        'distance': distances
    }
    
    #appends each city dictionary to list
    city_dict.append(city)

#Creates and writes to output file containing city's distances to each other
with open('city_distances.json', 'w') as f:
    f.write (json.dumps(city_dict))





#Next we need to add a file that contains the average distance to the 100 closests UFO's for each city


#List that loads in data from ufo csv file
ufoData = []

with open('ufo_data.csv') as f:
    file = csv.DictReader(f, delimiter = ',')

    for line in file:
        #loads in the csv into the list 
        ufoData.append(line)

#List that contains all the points of UFO sightings
ufo_points = []
for dics in ufoData:
    ufo_points.append(Point(float(dics['lon']), float(dics['lat'])))


#geoseries of all ufos coordinates
ufo_series = geopandas.GeoSeries(ufo_points)

avg_ufo_dist = []


for i in range(series_len):
    dist = []

    #Returns a Series containing the distance to aligned other
    dist_array = ufo_series.distance(geoseries[i])

    dist_array = dist_array.values

    #sorts the array based on closest ufo sightings
    dist_array = sort(dist_array)

    #gets only the top 100 nearest ufos
    closest_array = dist_array[0:100]

    #finds the average distance away of the 100 closest ufos
    avg_dist = (sum(closest_array)/(len(closest_array)))

    city = {
        'city': cityNames[i],
        'longitude': geoseries[i].x,
        'latitude': geoseries[i].y,
        'avgufo_distance': avg_dist
    }

    avg_ufo_dist.append(city)

#Creates and writes to output file containing average UFO distance from city
with open('average_ufo.json', 'w') as f:
    f.write(json.dumps(avg_ufo_dist))
