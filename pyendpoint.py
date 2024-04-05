from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
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
    coordinates = geojson.geometry.coordinates[0]


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

