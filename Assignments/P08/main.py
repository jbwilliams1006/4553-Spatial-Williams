from operator import ge
import geopandas as geo
import json
from shapely.geometry import Point 

def makePoint(city):
  feature = {
    "type": "Feature",
    "properties": {"marker-symbol": "https://e7.pngegg.com/pngimages/905/993/png-clipart-dot-dot.png"},
    "geometry": {
      "type": "Point",
      "coordinates": [0,0]
    }
  }

  for key,val in city.items():
    if key == 'latitude':
      feature['geometry']['coordinates'][1] = val
    elif key == 'longitude':
      feature['geometry']['coordinates'][0] = val
    else:
      feature['properties'][key] = val

  return feature



with open('Assignments/P08/cities.json') as f:
    cities = json.load(f)

with open('Assignments/P08/states.geojson') as g:
    states = json.load(g)

states = states["features"]
# print(states[34])

#Creates template for states' visualization
for state in states:
    state['properties']['title'] = state['properties']['name'] 
    state['properties']['stroke'] = "#000000" 
    state['properties']['fill'] = '#F5F5F5' 
    state['properties']['stroke-width'] = 1 
    state['properties']['population'] = 0 

#reads geoseries in 
with open('Assignments/P08/states.geojson') as g:
    geo_states = geo.read_file(g)


#Contains the polygon for each state
geo_series = geo.GeoSeries(geo_states['geometry'])

#print(geo_series)

#appends features of points
pointfeat = []

for i in range(len(cities)):
    #Only checks for cities in the mainland 
    if cities[i]['longitude'] > -140:

        points = Point(cities[i]['longitude'],cities[i]['latitude'])

        pointfeat.append(makePoint(cities[i]))

        # This code finds matches within the  geoseries
        #Must install pygeos
        #Checks what state the city points reside within 
        #Will return the number polygon in the geoseries
        print(points)
        PointQuery = geo_series.sindex.query(points, predicate='within')

        if (PointQuery.size == 1):
            # print(PointQuery.item(0))
            states[PointQuery.item(0)]['properties']['population'] += cities[i]['population']
            
            #Changes a states fill color based off population size
            if(states[PointQuery.item(0)]['properties']['population'] > 20000000):
                states[PointQuery.item(0)]['properties']['fill'] = "#000066"
            elif(states[PointQuery.item(0)]['properties']['population'] > 15000000):
                states[PointQuery.item(0)]['properties']['fill'] = "#000099"
            elif(states[PointQuery.item(0)]['properties']['population'] > 10000000):
                states[PointQuery.item(0)]['properties']['fill'] = "#0000CC"
            elif(states[PointQuery.item(0)]['properties']['population'] > 8000000):
                states[PointQuery.item(0)]['properties']['fill'] = "#0000FF"
            elif(states[PointQuery.item(0)]['properties']['population'] > 6000000):
                states[PointQuery.item(0)]['properties']['fill'] = "#3333FF"
            elif(states[PointQuery.item(0)]['properties']['population'] > 4000000):
                states[PointQuery.item(0)]['properties']['fill'] = "#6666FF"
            elif(states[PointQuery.item(0)]['properties']['population'] > 2000000):
                states[PointQuery.item(0)]['properties']['fill'] = "#9999FF"
            elif(states[PointQuery.item(0)]['properties']['population'] > 500000):
                states[PointQuery.item(0)]['properties']['fill'] = "#CCCCFF"

            print(states[PointQuery.item(0)]['properties']['name'], ' Population: ',states[PointQuery.item(0)]['properties']['population'])
       
        elif (PointQuery.size > 1):
            print("Too many")

        else:
            print("Not Found")    

#print(pointfeat)

GeoJsonOutput = {
            "type": "FeatureCollection",
            "features": []
         }
for s in states:
    GeoJsonOutput['features'].append(s)

for p in pointfeat:
    GeoJsonOutput['features'].append(p)

with open('Assignments/P08/Output.geojson', 'w') as out:
      out.write(json.dumps(GeoJsonOutput, indent=4))


