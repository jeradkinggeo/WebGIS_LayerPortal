import owslib
from owslib.wms import WebMapService
import requests
import xml.etree.ElementTree as xmlet
import lxml.etree as xmltree
import os
from pyproj import transform, Proj
import datetime
from datetime import datetime, timedelta
import geopandas as gpd



class layer:
    def __init__(self, crs, wms, layer_name, abr, 
                 size, format, transparent, Time_format):
        self.xmin, self.ymin, self.xmax, self.ymax = None, None, None, None
        self.crs = crs
        self.wms = wms
        self.name = layer_name
        self.abr = abr
        self.size = size
        self.format = format
        self.transparent = transparent
        self.Time_format = Time_format

    def wms_resp(self, wms):
            wmsUrl = wms
            response = requests.get(wmsUrl)
            WmsXml = xmltree.fromstring(response.content)
            result = print(xmltree.tostring(WmsXml, pretty_print = True, encoding = str))
            return result

    def wms_req(self, timeP):
        if self.Time_format == True:
            timeP = timeP + "T00:00:00Z"
        wms = WebMapService(self.wms)
        print(wms)
        result = wms.getmap(layers=self.name,  # Layers
                    srs=self.crs,  # Map projection
                    bbox=(self.xmin,self.ymin, self.xmax,self.ymax),  # Bounds
                    size=self.size,  # Image size
                    time=timeP,  # Time of data
                    format=self.format,  # Image format
                    transparent=self.transparent)
        return result
    
def create_date_list(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    num_days = (end - start).days
    date_list = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(num_days + 1)]
    return date_list
    

def shp_extent(shapefile_path):
    gdf = gpd.read_file(shapefile_path)
    bounds = gdf.total_bounds
    return (bounds[0], bounds[1], bounds[2], bounds[3])


def coord_transformer(bounds):
    proj_4326 = Proj(init = 'epsg:4326')
    proj_3857 = Proj(init = 'epsg:3857')
    xmin, ymin = transform(proj_4326, proj_3857, bounds[0], bounds[1])
    xmax, ymax = transform(proj_4326, proj_3857, bounds[2], bounds[3])
    return (xmin, ymin, xmax, ymax)


def layer_pull(bounds, datelist, layer_name, layer_obj):
    pri_dir = "Image_Directory"
    region = f"{bounds[0]}_{bounds[1]}_{bounds[2]}_{bounds[3]}"  

    if not isinstance(datelist, list):
        datelist = [datelist]

    if not os.path.exists(pri_dir):
        os.mkdir(pri_dir)
    
    os.chdir(pri_dir)
    
    
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    runtime_dir = "runtime_" + current_time
    os.mkdir(runtime_dir)
    os.chdir(runtime_dir)
    
    for d in datelist:
        pathname = d
        os.makedirs(pathname, exist_ok=True)  
        os.chdir(pathname)
        
        if isinstance(layer_obj, list):
            
            for sat in layer_obj:
                img = sat.wms_req("date")
                with open(sat.abr + "_" + d + '.png', 'wb') as out:
                    out.write(img.read())
        else:
            
            img = layer_obj.wms_req(d)
            with open(layer_obj.abr + "_" + d + '.png', 'wb') as out:
                out.write(img.read())
                
        os.chdir('..')  

    os.chdir(os.path.join('..', '..'))



MODIS_Terra_CorrectedReflectance_TrueColor = layer(
                                                   'EPSG:3857', 
                                                   'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', 
                                                   ['MODIS_Terra_CorrectedReflectance_TrueColor'],
                                                   'MODIS_TCR', 
                                                   (1200, 600), 
                                                   'image/png', 
                                                   True, 
                                                   False)

VIIRS_NOAA20_Thermal_Anomalies_375m_All = layer(
                                                'EPSG:4326', 
                                                'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', 
                                                ['VIIRS_NOAA20_Thermal_Anomalies_375m_All'],
                                                'VIIRS_TA', 
                                                (1200, 600), 
                                                'image/png', 
                                                True, 
                                                False)

# ^ Only has data past 2020-01-01

VIIRS_NOAA20_LST = layer(
                        'EPSG:4326', 
                        'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', 
                        ['VIIRS_NOAA20_Land_Surface_Temp_Day'],
                        'VIIRS_LST', 
                        (1200, 600), 
                        'image/png', 
                        True, 
                        False)

MODIS_Aqua_Terra_AOD = layer(
                           'EPSG:4326', 
                           'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', 
                            ['MODIS_Combined_MAIAC_L2G_AerosolOpticalDepth'],
                            'MODIS_Terra_AOD', 
                             (1200, 600), 
                             'image/png', 
                              True, 
                              False)

MODIS_Combined_Thermal_Anomalies_All = layer(
                           'EPSG:4326', 
                           'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', 
                            ['MODIS_Combined_Thermal_Anomalies_All'],
                            'MODIS_Terra_TA', 
                             (1200, 600), 
                             'image/png', 
                              True, 
                              True)




def set_bbox(self, bounds):
    self.xmin = bounds[0]
    self.ymin = bounds[1]
    self.xmax = bounds[2]
    self.ymax = bounds[3]
    return self.xmin, self.ymin, self.xmax, self.ymax

def resolution_calc(self, scale):
    scalefactor = scale  
    
    initial_width = (int(self.xmax) - int(self.xmin)) * scalefactor
    initial_height = (int(self.ymax) - int(self.ymin)) * scalefactor
    
    max_dimension = max(initial_width, initial_height)
    
    if max_dimension > 20000:
        reduction_factor = 20000 / max_dimension
        width = initial_width * reduction_factor
        height = initial_height * reduction_factor
    else:
        width = initial_width
        height = initial_height
    
    self.size = (int(width), int(height))


#Index for layers are hardcoded, but works for now
def layer_check(layerlist, datelist):
    if datelist[0] < '2020-01-01':
        print("VIIRS_NOAA20_Thermal_Anomalies_375m_All does not have data before 2020-01-01")
        return layerlist[1::]
    else:
        layerlist.remove(layerlist[1])
        return layerlist



        

            