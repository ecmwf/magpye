

"""
north_atlantic
==================

| area_name = "north_atlantic"  

| **magpye** has a list of predefined geographical areas.    
| Options are available to customise your Coastlines. 

"""

from magpye import GeoMap

map = GeoMap(area_name="north_atlantic")


map.coastlines(land_colour="grey")
map.gridlines(line_style="dash")
map.show()


# sphinx_gallery_thumbnail_path = '_static/geoareas/north_atlantic.png'

    