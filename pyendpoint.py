from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import py_src.layersclass as lc
import pyreqrun as pr


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"])

class GeoJSON(BaseModel):
    type: str
    properties: Dict
    geometry: Dict

class Message(BaseModel):
    content: str

#StartDate

#EndDate

#layerName

@app.post("/geojson/")
async def receive_geojson(geojson: GeoJSON):
    # Accessing properties
    properties = geojson.properties

    pr.request_func(geojson)

    # Print individual variables
    #print(f"Start Date: {start_date}, End Date: {end_date}, Scale Factor: {scale_factor}, Layer Name: {layer_name}")

    return {"message": "GeoJSON received successfully!"}

# uvicorn pyendpoint:app --reload
