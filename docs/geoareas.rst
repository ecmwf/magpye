Predefined geographical areas
=============================

Here is the list of the predefined geographical areas define in **magpye**,

To create a map
 .. code-block:: python
     from ecmwf.geomaps import GeoMap
     
     geomap = GeoMap(area_name="europe")
     geomap.coastlines(land_colour="grey")
     geomap.show()
 .. image:: _static/examples/firststeps-coastlines.png
   :width: 100%


.. toctree::
    :maxdepth: 2
    :glob:

    geoareas/*
