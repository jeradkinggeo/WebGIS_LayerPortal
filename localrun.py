import zipfile
import os
import owslib
import json
from owslib.wms import WebMapService
import layersclass as lc
import geopandas as gpd


def sgl_date_check(datelist):
    for i in range(len(datelist) - 1): 
        if datelist[i] == datelist[i+1]:
            return True
    return False

def flatten_coordinates(coords):
    if isinstance(coords[0], float):  
        return [coords]  
    else:  
        return [point for sublist in coords for point in flatten_coordinates(sublist)]

def get_bounds(coordinates):
    flattened_coords = flatten_coordinates(coordinates)
    x_values = [coord[0] for coord in flattened_coords]
    y_values = [coord[1] for coord in flattened_coords]

    xmin, xmax = min(x_values), max(x_values)
    ymin, ymax = min(y_values), max(y_values)

    return (xmin, ymin, xmax, ymax)

def json_parse(geojson):
    start_date = geojson['properties']['StartDate']
    end_date = geojson['properties']['EndDate']
    scale_factor = geojson['properties']['ScaleFactor']
    layer_name = geojson['properties']['LayerName']
    geometry = geojson['geometry']

    coordinates = geometry['coordinates']

    bounds = get_bounds(coordinates)

    datelist = lc.create_date_list(start_date, end_date)


    if sgl_date_check(datelist) == True:
        datelist = datelist[0]
  
    layer_obj = lc.MODIS_Aqua_Terra_AOD

    if layer_name == "MODIS_Terra_CorrectedReflectance_TrueColor":
        layer_obj = lc.MODIS_Terra_CorrectedReflectance_TrueColor
    elif layer_name == "MODIS_Aqua_Terra_AOD":
        layer_obj = lc.MODIS_Aqua_Terra_AOD
    else:
        raise ValueError("Invalid Layer Name")

    print(scale_factor)
    if layer_obj.crs == 'EPSG:4326':
        layer_obj.xmin, layer_obj.ymin, layer_obj.xmax, layer_obj.ymax = bounds
        print(bounds)
        
    elif layer_obj.crs == 'EPSG:3857':
            coordtransform = lc.coord_transformer(bounds)
            print(coordtransform)
            layer_obj.xmin, layer_obj.ymin, layer_obj.xmax, layer_obj.ymax = coordtransform

    if layer_obj.crs == 'EPSG:4326':
        lc.resolution_calc(layer_obj, scale_factor)
    elif layer_obj.crs == 'EPSG:3857':
        adjusted_scale_factor = (int(scale_factor) / int(scale_factor))
        lc.resolution_calc(layer_obj, adjusted_scale_factor)
    


    
   #bounds = (layer_obj.xmin, layer_obj.ymin, layer_obj.xmax, layer_obj.ymax)
    
    print(f"Start Date: {start_date}, End Date: {end_date}, Scale Factor: {scale_factor}, Layer Name: {layer_name}")
    return bounds, datelist, layer_name, layer_obj


def find_and_read_geojson(directory_path):
    files = os.listdir(directory_path)
    geojson_files = [file for file in files if file.endswith('.geojson')]
    return geojson_files

def read_and_parse_geojson(file_path):
    with open(file_path, 'r') as file:
        geojson = json.load(file)
    return geojson


def main():
    print("Start")
    cwd = os.getcwd()
    geojson_files = find_and_read_geojson(cwd)
    for geojson_file in geojson_files:
        file_path = os.path.join(cwd, geojson_file)
        geojson = read_and_parse_geojson(file_path)
        bounds, datelist, layer_name, layer_obj = json_parse(geojson)
        print(layer_obj.size)
        lc.layer_pull(bounds, datelist, layer_name, layer_obj)



if __name__ == "__main__":
    main()