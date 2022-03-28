from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn

#loads the API
if __name__ == '__main__':
    uvicorn.run("Main_API:api",host="127.0.0.1", port=8080, log_level="debug", reload=True)

#Starts api
api = FastAPI()

#gets the required documents
@api.get('/')
async def root_folder():
    return RedirectResponse(url="/docs")


#returns the list of countries
@api.get('/country_list/') 
async def country_list(): 


#returns the shape of a country
@api.get('/get_shape/{country}')
async def get_shape(country: str):


#autofills countries based off prefix
@api.get('/autofill/{string}')
async def autofill(string: str):


#returns center of relative country
@api.get('/get_center/{country}')
async def get_center(country: str): # type in a country name


#returns the total distance between 2 countries
@api.get('/find_distance/{country1},{country2}')
async def find_distance(country1: str, country2: str):

#returns what continent a country is on
@api.get('/get_continent/{country}')
async def get_continent(country: str):

#returns the direction from 2 countries
@api.get('/find_direction/{country1}/{country2}')
async def find_direction(country1: str, country2: str):
