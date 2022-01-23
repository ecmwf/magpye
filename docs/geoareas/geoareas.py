from Magics import macro as magics
from ecmwf.geomaps import GeoMap

areas = magics.predefined_areas()

for area in areas:

    map = GeoMap(area_name=area)
    map.coastlines(land_colour="grey")
    map.gridlines(line_style="dash")
    map.save("{}.png".format(area))
