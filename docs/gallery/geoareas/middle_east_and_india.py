"""
middle_east_and_india
==================

| area_name = "middle_east_and_india"

.. image:: /_static/geoareas/middle_east_and_india.png
    :width: 400

| **magpye** has a list of predefined geographical areas.
| Options are available to customise your Coastlines.

"""

from magpye import GeoMap

map = GeoMap(area_name="middle_east_and_india")


map.coastlines(land_colour="grey")
map.gridlines(line_style="dash")
map.show()


# sphinx_gallery_thumbnail_path = '_static/geoareas/middle_east_and_india.png'
