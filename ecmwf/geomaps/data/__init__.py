
import os

from .. import macro
from . import ecdata, grib, netcdf


def detect_source(source, geomap):
    if isinstance(source, str):
        data = detect_file(source)(source, geomap)
    else:
        data = ecdata.EcData(source, geomap)
    return data


def detect_file(file_name):
    _, ext = os.path.splitext(file_name)
    ext = ext.lstrip(".")
    format_types = {
        "grib": "grib",
        "grb": "grib",
        "grib1": "grib",
        "grib2": "grib",
        "nc": "netcdf",
        "nc3": "netcdf",
        "nc4": "netcdf",
        "cdf": "netcdf",
    }
    try:
        format_type = format_types[ext]
    except KeyError:
        f"unrecognised extension '.{ext}'; try grib or netcdf instead"
    
    return {
        "grib": grib.Grib,
        "netcdf": netcdf.NetCDF,
    }[format_type]