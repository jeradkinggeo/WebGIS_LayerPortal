from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import shutil
import layersclass as lc
import reqrun as pr
from fastapi.responses import FileResponse
import os


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"])

class Properties(BaseModel):
    StartDate: str
    EndDate: str
    ScaleFactor: str
    LayerName: str

class Geometry(BaseModel):
    type: str
    coordinates: List[List[List[float]]]  # Nested list for polygon coordinates

class GeoJSON(BaseModel):
    type: str
    properties: Properties
    geometry: Geometry

class Message(BaseModel):
    content: str

#StartDate

#EndDate

#layerName

@app.post("/geojson/")
async def receive_geojson(geojson: GeoJSON):
    # Accessing properties
    #print(geojson.dict())
    start_date = geojson.properties.StartDate
    end_date = geojson.properties.EndDate
    scale_factor = geojson.properties.ScaleFactor
    layer_name = geojson.properties.LayerName
    geometry = geojson.geometry

    coordinates = geometry.coordinates


    datelist = lc.create_date_list(start_date, end_date)
    print(datelist)
    message = pr.json_parse(geojson)
    print(message)
    #print(f"Start Date: {start_date}, End Date: {end_date}, Scale Factor: {scale_factor}, Layer Name: {layer_name}")

@app.get("/download-imagery/{file_name}")
async def download_imagery(file_name: str):
    file_path = f"tmp/{file_name}"
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=file_name, media_type='application/zip')
    return {"error": "File not found."}
# uvicorn pyendpoint:app --reload

