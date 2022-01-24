
import os

from . import ecdata, grib, netcdf, temporary


def detect_source(source, geomap):
    if isinstance(source, str):
        data = detect_file(source)(source, geomap)
    else:
        data = ecdata.EcData(source, geomap)
    return data


def detect_vector_source(*args, wind_mode, geomap):
    tmp = temporary.temp_file('.grib').path
    indices = []
    for source in args:
        if not isinstance(source, str):
            fname, grib_index = source.grib_index()[0]
        else:
            raise NotImplementedError("vector plots only work with ecmwf-data")
        with open(tmp, 'ab') as tf:
            with open(fname, 'rb') as f:
                for line in f:
                    tf.write(line)
        indices.append(grib_index)
    return grib.Grib(tmp, geomap, wind_mode=wind_mode, grib_mode="byte_offset", wind_1=indices[0], wind_2=indices[1])


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
