import json
from rich import print
import random

def randColor():
  r = lambda: random.randint(0,255)
  return ('#%02X%02X%02X' % (r(),r(),r()))


def makePoint(city):
  feature = {
    "type": "Feature",
    "properties": {
      "marker-color":randColor(),
      "marker-symbol": random.randint(0,33)
    },
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
  
# def makeLineString(city):
#   feature = {
#     "type": "Feature",
#     "properties": {
#       "stroke":randColor(),
#       "stroke-width": 2,
#     },
#     "geometry": {
#       "type": "LineString",
#       "coordinates": [0,0][0,0]
#     }
#   }
#   for key,val in city.items():
#     if key == 'latitude':
#       feature['geometry']['coordinates'][1] = val
#       feature['geometry']['coordinates'][1][1] = key+1[val]
#     elif key == 'longitude':
#       feature['geometry']['coordinates'][0] = val
#       feature['geometry']['coordinates'][1][0] = key+1[val]
#     else:
#       feature['properties'][key] = val
    
#   return feature



#MAIN 


with open("cities.json") as f:
  data = json.load(f)

states = {}
#list for sorting longitudes from least to greatest
long = []
#Used to make points 
points = []

#Used to make line
lineString = {
  "type": "FeatureCollection",
  "features": []
}
coor = []


#Updates the items to the cities in the state with the largest population 
for item in data:
  if not item ["state"] in states or states[item['state']]['population'] < item['population']:
    states.update({
      item['state']:{
          'city' : item['city'],
          'growth' : item['growth'],
          'latitude' : item['latitude'],
          'longitude': item['longitude'],
          'population' : item['population'],
          'state' : item['state']
          
      } }  )
  
  

#only appends the longitudes in the mainland
for keys in states:
  if(states[keys]['longitude'] > -140):
    long.append(states[keys]['longitude'])

#Sorts the longitudes
long.sort(key = float)

#Sort states and create geometry points  
for stateinfo in long:
    for keys in states:
        if (states[keys]['longitude'] == stateinfo) and (stateinfo > -140):
            points.append(makePoint(states[keys]))
            coor.append(states[keys])

#Create line points 
for i in range(len(coor)):
  if i != len(coor) - 1:
    lineString['features'].append(
            {
                "type": "Feature",
                "properties": {
                    "stroke": randColor(),
                    "stroke-width": 2,
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [coor[i]['longitude'], coor[i]['latitude']],
                        [coor[i + 1]['longitude'], coor[i + 1]['latitude']]
                    ]
                }
            }
        )


with open("new.geojson","w") as f:
  json.dump(points,f,indent=4)
  json.dump(lineString,f,indent = 5)
     

