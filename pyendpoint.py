from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import py_src.layersclass as lc
import pyreqrun as pr
import DataNormTool as dn

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
    #print(geojson.dict())
    properties = geojson.properties

    start_date = properties.get("StartDate")
    end_date = properties.get("EndDate")
    scale_factor = properties.get("ScaleFactor")
    layer_name = properties.get("LayerName")
    bounds = properties.get("coordinates")

    datelist = dn.create_date_list(start_date, end_date)
    print(datelist)
    message = pr.request_func(geojson)
    print(message)
    #print(f"Start Date: {start_date}, End Date: {end_date}, Scale Factor: {scale_factor}, Layer Name: {layer_name}")


# uvicorn pyendpoint:app --reload
