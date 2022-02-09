

"""
south_atlantic_and_indian_ocean
==================

| area_name = "south_atlantic_and_indian_ocean"  

| **magpye** has a list of predefined geographical areas.    
| Options are available to customise your Coastlines. 

"""

from magpye import GeoMap

map = GeoMap(area_name="south_atlantic_and_indian_ocean")


map.coastlines(land_colour="grey")
map.gridlines(line_style="dash")
map.show()


# sphinx_gallery_thumbnail_path = '_static/geoareas/south_atlantic_and_indian_ocean.png'

    