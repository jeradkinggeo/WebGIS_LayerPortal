import zipfile
import os
import owslib
from owslib.wms import WebMapService
import layersclass as lc
import geopandas as gpd


overwrite = True

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

# def get_bounds2(coordinates):

#     xmin = xmax = coordinates[0][0]
#     ymin = ymax = coordinates[0][1]

#     for coord in coordinates:
#         xmin = min(xmin, coord[0])
#         ymin = min(ymin, coord[1])
#         xmax = max(xmax, coord[0])
#         ymax = max(ymax, coord[1])

#     bounds = (xmin, ymin, xmax, ymax)
#     return bounds

def get_n_zip(bbox, date, layer_name, layer_obj):
    layercrs = layer_obj.crs
    if layercrs == 'EPSG:4326':
        wms = WebMapService('https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', version='1.1.1')
    elif layercrs == 'EPSG:3857':
        wms = WebMapService('https://gibs.earthdata.nasa.gov/wms/epsg3857/best/wms.cgi?', version='1.1.1')
    else:
        raise ValueError("Invalid CRS")
    
    for d in range(len(date)-1):
        img = layer_obj.wms_req(date[d])
    
        # Save the image
        image_path = f'tmp/{date}_MODIS_Terra_CorrectedReflectance_TrueColor.png'
        with open(image_path, 'wb') as out:
            out.write(img.read())
        
        # Create a ZIP file
        zip_path = f'tmp/{date}_imagery.zip'
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(image_path, arcname=os.path.basename(image_path))
        
        # Cleanup the individual file after zipping
        os.remove(image_path)


def json_parse(geojson):
    start_date = geojson.properties.StartDate
    end_date = geojson.properties.EndDate
    scale_factor = geojson.properties.ScaleFactor
    layer_name = geojson.properties.LayerName
    geometry = geojson.geometry

    coordinates = geometry.coordinates
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
        lc.resolution_calc(layer_obj, (scale_factor/scale_factor) * .1)
    


    

    print(f"Start Date: {start_date}, End Date: {end_date}, Scale Factor: {scale_factor}, Layer Name: {layer_name}")

    get_n_zip(bounds, datelist, layer_name, layer_obj)

