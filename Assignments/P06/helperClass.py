import json
import geopandas
from shapely.geometry import Polygon
import math
import numpy


class helperclass:
    def __init__(self):
        with open ('/Users/josh/4553-Spatial-Williams/Assignments/P06/continents.json') as f:
            self.worldData = json.load(f)
        self.output = open('output.geojson','w')

    #returns the polygon shape of a nation
    def getPoly(self, country):
        nation = self.countries(country)

        multi = nation['geometry']['coordinates']

        poly = self.createPoly(multi)

        return poly


    # returns the dictionary list of all the country names
    def CountryNames(self): 
        worldList=[] 
        for continents in self.worldData:
            for countries in self.worldData[continents]:
                worldList.append(countries['properties']['name'])
        return worldList 

    
    #returns the center of a polygon
    def getCenter(self, poly):
        series = geopandas.GeoSeries(Polygon(poly))

        center = [series.centroid[0].x, series.centroid[0].y]

        return center

    #returns country
    def countries(self, country):
        for continents in self.worldData:
            for countries in self.worldData[continents]:
                if countries['properties']['name'].lower() == country.lower():
                    return countries
    
    #returns continent
    def Continent(self, name):
        for continents in self.worldData:
            for countries in self.worldData[continents]:
                if name == countries['properties']['name']:
                    return continents

    

    #returns polygon after creating it from bigger one
    def createPoly(self, multi):
        ct = 0
        index = 0
        max = 0
            
        for poly in multi:
            if len(poly[0]) > max:
                    max = len(poly[0])
                    index = ct
            ct += 1
                

        return multi[index][0]




    #finds the distance between 2 nations
    def getDistance(self, poly1, poly2, algo):
        if algo == True:
            center2 = self.getCenterPoint(poly1)
            center1 = self.getCenterPoint(poly2)

            tempRec = [center1, [center1[0], center2[1]], center2, [center2[0], center1[1]]]
            rec = Polygon(tempRec)

            con1 = geopandas.GeoSeries(geopandas.points_from_xy([x[0] for x in poly1], [y[1] for y in poly1]))
            con2 = geopandas.GeoSeries(geopandas.points_from_xy([x[0] for x in poly2], [y[1] for y in poly2]))
            
            #queries the borders with the rectangle
            pi1 = con1.sindex.query(rec)
            pi2 = con2.sindex.query(rec)

            distance = []

            #finds distance between 2 points
            for p1 in pi1:
                for p2 in pi2:
                    distance.append(math.sqrt(((con1[p1].x - con2[p2].x)**2)+((con1[p1].y-con2[p2].y)**2))) 
            tempRec.append(tempRec[0])

            ps = []

            for points in pi1:
                ps.append([con1[points].x, con1[points].y])

            for points in pi2:
                ps.append([con2[points].x, con2[points].y])

            self.__geoJsonPoly(polys=[poly1, poly2, tempRec], points=ps)
        else:
            con1 = geopandas.GeoSeries(geopandas.points_from_xy([x[0] for x in poly1], [y[1] for y in poly1]))
            con2 = geopandas.GeoSeries(geopandas.points_from_xy([x[0] for x in poly2], [y[1] for y in poly2]))

            distance = []

            for p1 in con1:
                for p2 in con2:
                    distance.append(math.sqrt(((p1.x - p2.x)**2)+((p1.y-p2.y)**2)))

        #finds shortest path
        distance.sort()

        return distance[0]

            


    #takes in a weight that reduces the polygon
    def reducePoints(self, name, weight):
        poly = self.getPoly(name)

        series = geopandas.GeoSeries(Polygon(poly))

        poly = series.simplify(weight)[0]
        poly = numpy.asarray(poly.exterior.coords).tolist()

        return poly
