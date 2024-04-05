import zipfile
import os
import owslib
from owslib.wms import WebMapService
import layersclass as lc


overwrite = True

def json_parse(geojson):
    properties = geojson.properties

    start_date = properties.get("StartDate")
    end_date = properties.get("EndDate")
    scale_factor = properties.get("ScaleFactor")
    layer_name = properties.get("LayerName")
    bounds = geojson.geometry.coordinates


    datelist = lc.create_date_list(start_date, end_date)
    print(datelist)

    if layer_name is "MODIS_Terra_CorrectedReflectance_TrueColor":
        layer_obj = lc.MODIS_Terra_CorrectedReflectance_TrueColor
    else:
        layer_obj = lc.VIIRS_NOAA20_Thermal_Anomalies_375m_All


    if layer_obj.crs == 'EPSG:4326':
        layer_obj.xmin, layer_obj.ymin, layer_obj.xmax, layer_obj.ymax = bounds
        
    elif layer_obj.crs == 'EPSG:3857':
            coordtransform = lc.coord_transformer(bounds)
            layer_obj.xmin, layer_obj.ymin, layer_obj.xmax, layer_obj.ymax = coordtransform

    if layer_obj.crs == 'EPSG:4326':
        lc.resolution_calc(layer_obj, scale_factor)
    elif layer_obj.crs == 'EPSG:3857':
        lc.resolution_calc(layer_obj, (scale_factor/scale_factor) * .1)

    


    

    print(f"Start Date: {start_date}, End Date: {end_date}, Scale Factor: {scale_factor}, Layer Name: {layer_name}")

    return "GeoJSON received successfully!"


def get_n_zip(bbox, date, layer_name, layer_obj):
    layercrs = layer_obj.crs
    if layercrs == 'EPSG:4326':
        wms = WebMapService('https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', version='1.1.1')
    elif layercrs == 'EPSG:3857':
        wms = WebMapService('https://gibs.earthdata.nasa.gov/wms/epsg3857/best/wms.cgi?', version='1.1.1')
    else:
        raise ValueError("Invalid CRS")
    
    for d in date:
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
