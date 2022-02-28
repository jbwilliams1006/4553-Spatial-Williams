## P03 - Voronoi
### Joshua Williams
### Description:

 Loads up GeoPandas GeoSeries (spatial index / Rtree) with all the cities and UFO sightings. Once we have all of these point locations loaded, we can determine which cities have the most UFO sightings in close proximity. Creates a voronoi diagram over the US creating polygons around each of the 49 cities. Loads said polygons and UFO sighting points into a spatial tree (geopandas rtree). Finally, querys the rtree getting the UFO sighting points that are contained within each polygon

### Files

|   #   | File            | Description                                        |
| :---: | --------------- | -------------------------------------------------- |
|   1   | [Main.py](https://github.com/jbwilliams1006/4553-Spatial-Williams/blob/main/Assignments/P03/main.py)         | Main driver of the program the produces output     |
|   2   | [cities.geojson](https://github.com/jbwilliams1006/4553-Spatial-Williams/blob/main/Assignments/P03/cities.geojson)    | Infile that contains city data                          |
|   3   | [ufo_data.csv](https://github.com/jbwilliams1006/4553-Spatial-Williams/blob/main/Assignments/P03/ufo_data.csv)  | Infile that contains UFO data                                            |
|   4   | [city_distances.json](https://github.com/jbwilliams1006/4553-Spatial-Williams/blob/main/Assignments/P03/city_distances.json)  | Outfile of the distances of other cities to specific city                                           |
|   5   | [average_ufo.json](https://github.com/jbwilliams1006/4553-Spatial-Williams/blob/main/Assignments/P03/average_ufo.json)  | Outfile that contains the average ufo distance from specified city                                            |

### Instructions

- Makes sure that all the neccessary dependicies are installed 
- run the main.py file 

 


