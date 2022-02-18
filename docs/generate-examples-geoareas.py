#!/usr/bin/env python3
# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#


import Magics.macro as magics

from magpye import GeoMap

areas = magics.predefined_areas()

for area in areas:
    print(area)
    map = GeoMap(area_name=area)
    map.coastlines(land_colour="grey")
    map.gridlines(line_style="dash")
    map.save("_static/geoareas/{}.png".format(area))
    fname = "gallery/geoareas/{}.py".format(area)

    script = '''

"""
{area}
==================

| area_name = "{area}"

.. image:: /_static/geoareas/{area}.png
    :width: 400

| **magpye** has a list of predefined geographical areas.
| Options are available to customise your Coastlines.

"""

from magpye import GeoMap

map = GeoMap(area_name="{area}")


map.coastlines(land_colour="grey")
map.gridlines(line_style="dash")
map.show()


# sphinx_gallery_thumbnail_path = '_static/geoareas/{area}.png'

    '''.format(
        area=area
    )

    with open(fname, "+w") as f:
        f.write(script)
