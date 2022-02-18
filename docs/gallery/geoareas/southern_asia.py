"""
southern_asia
==================

| area_name = "southern_asia"

.. image:: /_static/geoareas/southern_asia.png
    :width: 400

| **magpye** has a list of predefined geographical areas.
| Options are available to customise your Coastlines.

"""

from magpye import GeoMap

map = GeoMap(area_name="southern_asia")


map.coastlines(land_colour="grey")
map.gridlines(line_style="dash")
map.show()


# sphinx_gallery_thumbnail_path = '_static/geoareas/southern_asia.png'
