

"""
south_east_asia_and_indonesia
==================

| area_name = "south_east_asia_and_indonesia"  

.. image:: /_static/geoareas/south_east_asia_and_indonesia.png
    :width: 400

| **magpye** has a list of predefined geographical areas.    
| Options are available to customise your Coastlines. 

"""

from magpye import GeoMap

map = GeoMap(area_name="south_east_asia_and_indonesia")


map.coastlines(land_colour="grey")
map.gridlines(line_style="dash")
map.show()


# sphinx_gallery_thumbnail_path = '_static/geoareas/south_east_asia_and_indonesia.png'

    