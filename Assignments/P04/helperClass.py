import json
import geopandas
from shapely.geometry import Polygon
import math


class helperClass:
    def __init__(self):
        with open ('continents.json') as f:
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
        for feature in self.worldData['features']:  
            worldList.append(feature['properties']['name'])
        return worldList 

    #returns the distance from two countries in miles
    def CalculateDistance(self, country1, country2):
        DistanceList=[]
        DistanceList.append(country1)
        DistanceList.append(country2)
        for (x1, y1), (x2, y2) in zip(DistanceList, DistanceList[1:]):
            #Multiply by 69 for milage conversion
            Distance = ((math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)) * 69)
            
        return Distance

    #returns the center of a polygon
    def getCenter(self, poly):
        series = geopandas.GeoSeries(Polygon(poly))

        center = [series.centroid[0].x, series.centroid[0].y]

        return center

    #returns country
    def countries(self, country):
        for continents in self.worldData:
            for countries in self.worldData[continents]:
                if countries['properties']['name'] == country:
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

    def getDirection(self, Country1, Country2):
        country1 =  getCenter(Country1)
        country2 =  getCenter(Country2)

        if country1[0] < country2[0] and country1[1] < country2[1]:
            direction = 'South-West'
        elif country1[0] < country2[0] and country1[1] > country2[1]:
            direction = 'North-West'
        elif country1[0] > country2[0] and country1[1] > country2[1]:
            direction = 'North-East'
        elif country1[0] > country2[0] and country1[1] < country2[1]:
            direction = 'South-East'
        else:
            if country1[0] == country2[0] and country1[1] < country2[1]:
                direction = 'South'
            elif country1[0] == country2[0] and country1[1] > country2[1]:
                direction = 'Noth'
            elif country1[0] < country2[0] and country1[1] == country2[1]:
                direction = 'East'
            elif country1[0] > country2[0] and country1[1] == country2[1]:
                direction = 'West'

        return direction

    # Outputs data 
    def GeoPolygon(self,name):
        for feature in self.worldData['features']:
            if(feature['properties']['name']== name):
                print("Country: ",name, "Coordinates :\n\n",feature['geometry']['coordinates'])
                coord=feature['geometry']['coordinates']

                out = {
                        "type": "FeatureCollection",
                        "features": []
                    }
                out['features'].append({
                            "type": "Feature",
                            "properties": {},
                            "geometry": {
                            "type": "Polygon",
                            "coordinates": 
                                coord 
                        
                            }
                        })

                self.output.write(json.dumps(out, indent=4))
                return out
