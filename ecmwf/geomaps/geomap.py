# (C) Copyright 2021- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

import os

import Magics.macro as magics
import yaml

from . import macro, presets


def action(magics_macro, conditions=None, default_preset=None, **valid_args):
    """Decorator for generating figure methods.

    Args:
        magics_macro: The Magics macro to execute for this action.
        condition (dict): A dctionary of conditional variables which are
            required for the given action to execute on the given macro.
            Values can be sub-dictionaries, indicating that the condition is
            only required when a specific argument is passed.
        default_preset (str): The name of the default preset to use for this
            action.
        valid_args (dict): A mapping of argument names to their Magics
            counterparts.

    """

    def decorator(method):
        def wrapper(self, *args, preset=None, z_index=1, **kwargs):
            for i, arg in enumerate(args):
                try:
                    kwarg = list(valid_args)[i]
                except IndexError:
                    raise TypeError(
                        f"{method.__name__}() takes a maximum of "
                        f"{len(valid_args)} positional arguments but "
                        f"{len(args)} were given"
                    )
                if kwarg in kwargs:
                    raise TypeError(
                        f"{method.__name__}() got multiple values for "
                        f"argument '{kwarg}'"
                    )
                else:
                    kwargs[kwarg] = arg

            mapped_kwargs = dict()
            for key, value in kwargs.items():
                try:
                    mapped_key = valid_args[key]
                except KeyError:
                    raise TypeError(
                        f"{method.__name__}() got an unexpected keyword "
                        f"argument '{key}'"
                    )
                if isinstance(mapped_key, list):
                    for mkey in mapped_key:
                        if mkey not in mapped_kwargs:
                            mapped_kwargs[mkey] = value
                else:
                    mapped_kwargs[mapped_key] = value

            if preset is not None:
                mapped_kwargs = {
                    **presets.get(preset, method.__name__),
                    **mapped_kwargs,
                }

            if conditions is not None:
                for key, value in conditions.items():
                    if isinstance(value, dict):
                        if key in mapped_kwargs:
                            mapped_kwargs = {**value, **mapped_kwargs}
                    else:
                        mapped_kwargs = {**{key: value}, **mapped_kwargs}
            self.register(magics_macro(z_index=z_index, **mapped_kwargs))

        return wrapper

    return decorator


class GeoMap:
    def __init__(self, *args, preset=None, **kwargs):

        self.queue = []
        self._map(*args, **kwargs)

        self.apply_preset(preset)

    def apply_preset(self, preset):
        if preset is not None:
            macro_presets = presets.get(preset)
            for macro_preset in macro_presets:
                method = list(macro_preset)[0]
                args = macro_preset[method]
                getattr(self, method)(
                    preset=args.get("preset"),
                    z_index=args.get("z_index"),
                    **args.get("kwargs", dict()),
                )

    def register(self, item):
        self.queue.append(item)

    @action(
        macro.mmap,
        {"subpage_map_area_name": {"subpage_map_library_area": True}},
        area_name="subpage_map_area_name",
        projection="subpage_map_projection",
    )
    def _map(self, *args, **kwargs):
        pass

    @action(
        macro.mcoast,
        {
            "map_rivers": True,
            "map_coastline": False,
            "map_grid": False,
            "map_label": False,
        },
        colour="map_rivers_colour",
        style="map_rivers_style",
        thickness="map_rivers_thickness",
    )
    def rivers(self, *args, **kwargs):
        pass

    @action(
        macro.mcoast,
        {
            "map_coastline": True,
            "map_grid": False,
            "map_label": False,
            "map_coastline_land_shade_colour": {
                "map_coastline_land_shade": True,
            },
            "map_coastline_sea_shade_colour": {
                "map_coastline_sea_shade": True,
            },
        },
        resolution="map_coastline_resolution",
        colour="map_coastline_colour",
        land_colour="map_coastline_land_shade_colour",
        sea_colour="map_coastline_sea_shade_colour",
        style="map_coastline_style",
        thickness="map_coastline_thickness",
    )
    def coastlines(self, *args, **kwargs):
        pass

    @action(
        macro.mcoast,
        {
            "map_coastline": False,
            "map_grid": True,
        },
        lat_increment="map_grid_latitude_increment",
        lon_increment="map_grid_longitude_increment",
        lat_reference="map_grid_latitude_reference",
        lon_reference="map_grid_longitude_reference",
        style="map_grid_line_style",
        thickness="map_grid_thickness",
        colour="map_grid_colour",
        labels="map_label",
        label_font="map_label_font_style",
        label_colour="map_label_colour",
        label_size="map_label_height",
        label_lat_freq="map_label_latitude_frequency",
        label_lon_freq="map_label_longitude_frequency",
        label_top_edge="map_label_top",
        label_bottom_edge="map_label_bottom",
        label_left_edge="map_label_left",
        label_right_edge="map_label_right",
    )
    def grid(self, *args, **kwargs):
        pass

    @action(
        macro.mtext,
        text="text_lines",
    )
    def title(self, text, **kwargs):
        pass

    def data(self, file_name, *args, **kwargs):
        method = {
            "grib": self._grib,
            "netcdf": self._netcdf,
        }[detect_input(file_name)]
        method(file_name)
        self._contour(*args, **kwargs)

    @action(
        macro.mcont,
        style="contour_line_style",
        colour=["contour_line_colour", "contour_highlight_colour"],
        highlight_colour="contour_highlight_colour",
    )
    def _contour(self, *args, **kwargs):
        pass

    @action(
        macro.mgrib,
        file_name="grib_input_file_name",
    )
    def _grib(self, *args, **kwargs):
        pass

    @action(
        macro.mnetcdf,
        file_name="netcdf_file_name",
    )
    def _netcdf(self, *args, **kwargs):
        pass

    @action(
        macro.mtext,
        text="text_lines",
    )
    def title(self, text, **kwargs):
        pass

    def show(self):
        return self._execute()

    def save(self, *args, **kwargs):
        nargs = len(args)
        if nargs == 1:
            name, format = os.path.splitext(args[0])
            kwargs["name"] = name
            kwargs["formats"] = [format.lstrip(".")]
        elif nargs > 1:
            raise TypeError(f"save expected at most 1 argument, got {nargs}")
        output = macro.output(**kwargs)
        return self._execute(output=output)

    def _execute(self, output=None):
        output = [output] if output is not None else []
        queue = output + sorted(self.queue, key=lambda x: x.z_index)
        return magics.plot(*(macro.execute() for macro in queue))


def detect_input(file_name):
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
    return format_type
