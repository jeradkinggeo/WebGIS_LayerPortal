from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import shutil
import layersclass as lc
import reqrun as pr
from fastapi.responses import FileResponse, JSONResponse
import os
import logging
import json


logger = logging.getLogger("my_logger")
logging.basicConfig(level=logging.INFO)

#File name line 177 error
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False,
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
        process_geojson = (geojson.dict())

        print(geojson.dict())
        print(geojson.properties.LayerName)
        return JSONResponse(content=geojson.dict())

        #pr.json_parse(geojson)

    #     zip_path = pr.get_n_zip(bbox, datelist, layer_name, layer_obj)

        
    #     return FileResponse(path=zip_path, filename=os.path.basename(zip_path), media_type='application/zip')
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))



    #print(f"Start Date: {start_date}, End Date: {end_date}, Scale Factor: {scale_factor}, Layer Name: {layer_name}")


#This should get the 
@app.get("/download-imagery/{file_name}")
async def download_imagery(file_name: str):
    file_path = f"tmp/{file_name}"
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=file_name, media_type='application/zip')
    return {"error": "File not found."}
# uvicorn pyendpoint:app --reload

