from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


from helperClass import helperclass
#loads the API
if __name__ == '__main__':
    uvicorn.run("Main_API:api",host="127.0.0.1", port=8080, log_level="debug", reload=True)

#Starts api
api = FastAPI()
helpclass = helperclass()

origins = ["*"]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#gets the required documents
@api.get('/')
async def root_folder():
    return RedirectResponse(url="/docs")


#returns the list of countries
@api.get('/country_list/') 
async def country_list(): 
    countries = helpclass.CountryNames()
    output = {'detail': 'Success','countries': countries}
    return output 

#returns the shape of a country
@api.get('/get_shape/{country}')
async def get_shape(country: str):
    country = country.title()

    country = helpclass.getpoly(country)

    output = {'Polygon:': country}
    return output


#returns center of relative country
@api.get('/get_center/{country}')
async def get_center(country: str):
    countryCenter = helpclass.getCenter(country)

    output = {'Country\'s Center': countryCenter} 

    return output
     


#returns the total distance between 2 countries
@api.get('/find_distance/{country1},{country2}')
async def find_distance(country1: str, country2: str):
    Country1 = helpclass.getCenter(country1)
    Country2 = helpclass.getCenter(country2)
    Distance = helpclass.CalculateDistance(Country1,Country2)
    output = {'distance': Distance}
    return output

#returns what continent a country is on
@api.get('/get_continent/{country}')
async def get_continent(country: str):
    continent = helpclass.Continent(country)
    output = {'Country/s Continent': continent}
    return output

#returns the direction from 2 countries
@api.get('/find_direction/{country1}/{country2}')
async def find_direction(country1: str, country2: str):
    Country1 = helpclass.getCenter(country1)
    Country2 = helpclass.getCenter(country2)
    Direction = helpclass.getDirection(Country1,Country2)
    output = {"Direction is ": Direction}
    return output
