from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class GeoJSON(BaseModel):
    type: str
    properties: Dict
    geometry: Dict

@app.post("/geojson/")
async def receive_geojson(geojson: GeoJSON):
    # Process your GeoJSON here
    print(geojson.dict())
    return {"message": "GeoJSON received successfully!"}

# run in bash in same dir as this app uvicorn app:app --reload
