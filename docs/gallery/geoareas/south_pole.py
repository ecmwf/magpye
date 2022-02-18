"""
south_pole
==================

| area_name = "south_pole"

.. image:: /_static/geoareas/south_pole.png
    :width: 400

| **magpye** has a list of predefined geographical areas.
| Options are available to customise your Coastlines.

"""

from magpye import GeoMap

map = GeoMap(area_name="south_pole")


map.coastlines(land_colour="grey")
map.gridlines(line_style="dash")
map.show()


# sphinx_gallery_thumbnail_path = '_static/geoareas/south_pole.png'
