"""
north_west_europe
==================

| area_name = "north_west_europe"

.. image:: /_static/geoareas/north_west_europe.png
    :width: 400

| **magpye** has a list of predefined geographical areas.
| Options are available to customise your Coastlines.

"""

from magpye import GeoMap

map = GeoMap(area_name="north_west_europe")


map.coastlines(land_colour="grey")
map.gridlines(line_style="dash")
map.show()


# sphinx_gallery_thumbnail_path = '_static/geoareas/north_west_europe.png'
