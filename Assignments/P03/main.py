import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import json
from pyproj import Transformer


from shapely.ops import unary_union
from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys_with_points_in_area
from geovoronoi import voronoi_regions_from_coords, points_to_coords

from shapely.ops import transform

debug = True
spatIndex = None


def loadGeoDataFrame(file, printHead=False):
    """Load a geojson file into a geoDataFrame
    Params:
        file (string)       : path / filename to be loaded
        printHead (bool)    : if True it prints the "head" of the dataframe
    Returns:
        GeoDataFrame re-projected to epsg:3395
    """
    gdf = gpd.read_file(file)
    gdf = gdf.to_crs("EPSG:3395")

    if printHead or debug:
        print(gdf.head())

    return gdf


def makeGeoDataFrame(data):
    """makes a geoDataFrame from some coordinate data and re-projects to 3395
    Params:
        data (dict) : dictionary with a "Coordinates" field that has a list of point data
    Returns:
        geoDataFrame projected with "EPSG:3395"
    """
    df = pd.DataFrame(data)
    gdf = gpd.GeoDataFrame(df, geometry="Coordinates", crs="EPSG:3395")

    return gdf


def getBoundingBox(points):
    """Get extremes from a geoDataFrame
    Params:
        points (geoDataFrame) : some geoDataFrame
    Returns:
        tuple : (minx, miny, maxx, maxy)
    """
    # gets extreme bounds (but we dont use it its just to log to console)
    minx, miny, maxx, maxy = points.total_bounds
    return (minx, miny, maxx, maxy)


def plotBorderAndPoints(border, points, saveName=None):
    """Given some outline shape (thats a geoDataFrame) and some points, make a plot to show.
       It doesn't really matter if ones a border and the other is points, basically given
       two geoDataFrames, it will plot them.
    Params:
        border (GeoDataFrame) : GeoDataFrame of the border
        points (GeoDataFrame) : GeoDataFrame of the points
        saveName (string)     : name/path if you want to save plot to a file
    Returns:
        None
    """

    fig, ax = plt.subplots(figsize=(8, 6))
    border.plot(ax=ax, color="gray")
    points.plot(ax=ax, markersize=2.5, color="blue")

    plt.axis("off")

    if saveName:
        plt.savefig(saveName, bbox_inches="tight")
    plt.show()


def createVoronoi(boundary, cities):
    """process the boundary (polygon border) and points to create the voronoi diagram.
    Params:
        boundary (geoDataFrame)   : the polygon representing the container of the diagram
        cities   (geoDataFrame)   : the points that represent the "seeds" for the diagram
    Returns:
        All the datastructures needed to plot the voronoi diagram. Most important for us however,
        is the "regionPolys" needed for us to determine which ufos are each of the polygons.

        cityCoords    -  the seeds converted to proper coordinate system for the diagram
        boundaryShape -  the boundary simplified or converted to a single outer ring polygon
        regionPolys   -  a dict of the internal polygons created around each seed
        regionPoints  -  a dict of the points used in the creation of the polygon
    """
    # pre-process data so it works with voronoi
    boundaryProj = boundary.to_crs(epsg=3395)
    citiesProj = cities.to_crs(boundaryProj.crs)
    boundaryShape = unary_union(boundaryProj.geometry)
    cityCoords = points_to_coords(citiesProj.geometry)

    # create the polygons and such
    regionPolys, regionPoints = voronoi_regions_from_coords(cityCoords, boundaryShape)

    # return all the things created so we can use / plot
    return cityCoords, boundaryShape, regionPolys, regionPoints


def plotVoronoi(cityCoords, boundaryShape, regionPolys, regionPoints, saveName=None):
    """plot the voronoi diagram.
    Params:
        cityCoords  (numpy ndarray)     : the seeds converted to proper coordinate system for the diagram
        boundaryShape (shapely polygon) : the boundary simplified or converted to a single outer ring polygon
        regionPolys   (dict)            : a dict of the internal polygons created around each seed
        regionPoints  (dict)            : a dict of the points used in the creation of the polygon
        saveName (string)               : path / filename to save file for plot if wanted
    """

    fig, ax = subplot_for_map(figsize=(8, 6))
    plot_voronoi_polys_with_points_in_area(
        ax, boundaryShape, regionPolys, cityCoords, regionPoints
    )
    if saveName:
        plt.savefig(saveName, bbox_inches="tight")
    plt.show()


def insertSpatIndex(gdf, epsg=None):
    """Insert some geo shape into the spatial index
    Params:
        gdf (geoDataFrame) : some geo data
        epsg (int)         : some new epsg (like 3395 or 4326) if you want to change the crs
    Returns:
        None
    """
    global spatIndex

    if epsg:
        gdf.to_crs(epsg=epsg)

    if not spatIndex:
        spatIndex = gpd.GeoSeries(gdf["geometry"])
    else:
        spatIndex.append(gdf["geometry"])


def getPolygonUfos(ufos, poly):
    """Query the spatial index given the polygon passed in.
    Params:
        ufos (geoDataFrame)    : data frame of ufos so we use the indexes returned
                                 by query to access the ufo data
        poly (shapely polygon) : the polygon to query with
    Returns:
        results (list) : list if indexes of the points found within the polygon
    """
    global spatIndex  # explicitly says use this global

    indexes = []  # list for resulting indexes found
    coordinates = []  # ufo data using the index from the geoDataFrame

    # This runs the query looking for ufo's that are "within" the polygon
    results = spatIndex.within(poly)

    # if a result in the results list is true, append that index to the results list
    for i in range(len(results)):
        if results[i]:
            indexes.append(i)
            coordinates.append(ufos["geometry"][i])

    # return results in a dataframe ready dictionary
    return {"indexes": indexes, "Coordinates": coordinates}


def getPolyCoords(poly):
    """Takes a shapely polygon and returns its xy coords making up the polygon.
    I used this to "check" my sanity when comparing different projections
    Params:
        poly (shapely polygon) : not a multipolygon, just a polygon
    Returns:
        returns to lists: one with x coords and one with y coords
    """
    # Extract the point values that define the perimeter of the polygon
    x, y = poly.exterior.coords.xy

    return x, y



#loads cities
city_geodatafrm = gpd.read_file("Assignments/P03/cities.geojson")



ufodata = pd.read_csv("Assignments/P03/ufo_data.csv")

pd.set_option('display.max_columns', None)

#makes geopandas dataframe from ufo
#crs projects points
ufo_dataframe = gpd.GeoDataFrame(ufodata, geometry = 
    gpd.points_from_xy(ufodata.lon, ufodata.lat), crs = "EPSG:4326")
    
ufo_dataframe = ufo_dataframe.to_crs(epsg =3395)


#opens shape file
border = gpd.read_file("Assignments/P03/us_border_shp")


fig, ax = plt.subplots(figsize =(12, 10))

#plots border
border.plot(ax=ax, color = "gray")


city_geodatafrm.plot(ax=ax, markersize=2.5, color = "blue")
ax.axis("off")
plt.axis('equal')




#Start voronoi creation
border = border.to_crs(epsg=3395)
city_proj = city_geodatafrm.to_crs(border.crs)

#convert points to coords
border_shape = unary_union(border.geometry)
coords = points_to_coords(city_proj.geometry)
# print(coords)

#initialize the polygon
polys, region_pts = voronoi_regions_from_coords(coords,border_shape)

fig, ax = subplot_for_map(figsize= (12, 10))

# plot polygon
plot_voronoi_polys_with_points_in_area(ax, border_shape, polys, coords, region_pts)

#create boundaries
fig  = plt.gcf()

#saves voronoi 
fig.savefig('voronoi1.png')
plt.show()