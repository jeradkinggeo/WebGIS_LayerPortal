from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

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

@app.post("/geojson/")
async def receive_geojson(geojson: GeoJSON):
    # Process your GeoJSON here
    print(geojson.dict())
    return {"message": "GeoJSON received successfully!"}

# run in bash in same dir as this app uvicorn pyendpoint:app --reload
