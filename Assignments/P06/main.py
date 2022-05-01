from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


from helperClass import helperclass
#loads the API
if __name__ == '__main__':
    uvicorn.run("main:api",host="127.0.0.1", port=8080, log_level="debug", reload=True)

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
@api.get('/country_names/') 
async def country_list(): 
    countries = helpclass.CountryNames()
    output = {'detail': 'Success','countries': countries}
    return output 

#returns the shape of a country
@api.get('/poly/{country}')
async def poly(country: str):
    country = country.title()

    country = helpclass.getPoly(country)

    out = {'detail': 'Success','polygon': country}

    return out


#returns center of relative country
@api.get('/get_center/{country}')
async def get_center(country: str):
    countryCenter = helpclass.getCenter(country)

    output = {'Country\'s Center': countryCenter} 

    return output
     

@api.get('/distance/{poly1}/{poly2}')
async def distance(poly1: str, poly2: str):
    poly1 = helpclass.reducePoints(poly1, 0.5)
    poly2 = helpclass.reducePoints(poly2, 0.5)

    distance = helpclass.getDistance(poly1, poly2, False)

    out = {'detail': 'Success','distance': distance}

    return out




