
import os

from .. import macro
from . import ecdata, grib, netcdf, temporary


def detect_source(source, geomap):
    if isinstance(source, str):
        data = detect_file(source)(source, geomap)
    else:
        data = ecdata.EcData(source, geomap)
    return data


def wind_source_uv(u, v, geomap):
    assert type(u) == type(v), "u and v must be same type"
    uv = temporary.temp_file('.grib').path
    if not isinstance(u, str):
        u, u_index = u.grib_index()[0]
        v, v_index = v.grib_index()[0]
    with open(uv, 'wb') as uv_file:
        for in_file in (u, v):
            with open(in_file, 'rb') as f:
                for line in f:
                    uv_file.write(line)
    return grib.Grib(uv, geomap, wind_mode='uv', grib_mode="byte_offset", u=u_index, v=v_index)


def wind_source_sd(s, d, geomap):
    assert type(s) == type(d), "speed and direction must be same type"
    sd = temporary.temp_file('.grib').path
    if not isinstance(s, str):
        s, s_index = s.grib_index()[0]
        d, d_index = d.grib_index()[0]
    with open(sd, 'wb') as sd_file:
        for in_file in (s, d):
            with open(in_file, 'rb') as f:
                for line in f:
                    sd_file.write(line)
    return grib.Grib(sd, geomap, wind_mode='sd', grib_mode="byte_offset", u=s_index, v=d_index)



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