import py_src
from py_src import bbox_calculator as bbox
from py_src import DataNormTool as dn
from py_src import layersclass as lc
import time 


overwrite = True

def request_func(geojson):
    properties = geojson.properties

    start_date = properties.get("StartDate")
    end_date = properties.get("EndDate")
    scale_factor = properties.get("ScaleFactor")
    layer_name = properties.get("LayerName")
    bounds = properties.get("coordinates")


    datelist = dn.create_date_list(start_date, end_date)
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

    print(bounds)

    

    print(f"Start Date: {start_date}, End Date: {end_date}, Scale Factor: {scale_factor}, Layer Name: {layer_name}")

    return "GeoJSON received successfully!"

# def main():

#     while True:
#         command = input(">: ")
#         if command.lower() == "exit":
#             exit()                    
#         elif command.lower() == "help":
#             print("""Commands:
#             Display list of fires in the CalFire GDB, "list":
#             Run the tool, "run":""")
#         elif command.lower() == "list": 
#             print('List of fires, show_recs:' )
#             shpname, shppath = dn.shapefile_finder("FireGDB")
#             dn.show_recs(shppath)
#         elif command.lower() == "run":
#             userinput = input("Enter FIRE NAME: ")
#             userinput = str(userinput)

#             sfinput = input("Enter the desired scale factor (Recommended 1000): ")
#             sfinput = int(sfinput)
            
#             shpname, shppath = dn.shapefile_finder("FireGDB")

#             attr_req = input("Would you like a txt log of the fire attributes (y/n): ")

#             if attr_req.lower() == 'y':
#                 dn.attributes_to_log(shppath, "fire_attributes.txt", userinput)
#             elif attr_req.lower() == 'n':
#                 pass

#             fire_attr_dict, bounds = dn.QueryAndParamPull(shppath, 'FIRE_NAME', userinput)

#             datelist = dn.create_date_list(fire_attr_dict['ALARM_DATE'], fire_attr_dict['CONT_DATE'])

#             satlist = [lc.VIIRS_NOAA20_Thermal_Anomalies_375m_All, lc.MODIS_Combined_Thermal_Anomalies_All, lc.MODIS_Aqua_Terra_AOD,
#                     lc.MODIS_Terra_CorrectedReflectance_TrueColor, lc.VIIRS_NOAA20_LST]
#             satlist = lc.layer_check(satlist,datelist)

#             for layer in satlist:
#                 if layer.crs == 'EPSG:4326':
#                     layer.xmin, layer.ymin, layer.xmax, layer.ymax = bounds
#                     print(layer.xmin, layer.ymin, layer.xmax, layer.ymax)
#                 elif layer.crs == 'EPSG:3857':
#                     coordtransform = lc.coord_transformer(bounds)
#                     layer.xmin, layer.ymin, layer.xmax, layer.ymax = coordtransform
#                     print(layer.xmin, layer.ymin, layer.xmax, layer.ymax)

#             for layer in satlist:
#                 if layer.crs == 'EPSG:4326':
#                     lc.resolution_calc(layer, sfinput)
#                 elif layer.crs == 'EPSG:3857':
#                     lc.resolution_calc(layer, (sfinput/sfinput) * .1)
        
#             lc.layer_pull(satlist, datelist, fire_attr_dict['FIRE_NAME'])
        


# if __name__ == "__main__":
#     main()