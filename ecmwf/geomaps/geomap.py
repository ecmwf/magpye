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

from . import macro, presets
from .action import action


class GeoMap:
    """Class for designing and plotting geospatial maps."""

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

    def _map(self, *args, **kwargs):
        extent = kwargs.pop("extent", None)
        if extent is not None:
            (
                kwargs["lower_left_lat"],
                kwargs["lower_left_lon"],
                kwargs["upper_right_lat"],
                kwargs["upper_right_lon"],
            ) = extent
        self.__map(*args, **kwargs)

    @action(
        macro.mmap,
        {"subpage_map_area_name": {"subpage_map_library_area": True}},
        area_name="subpage_map_area_name",
        projection="subpage_map_projection",
        lower_left_lat="subpage_lower_left_latitude",
        lower_left_lon="subpage_lower_left_longitude",
        upper_right_lat="subpage_upper_right_latitude",
        upper_right_lon="subpage_upper_right_longitude",
    )
    def __map(self, *args, **kwargs):
        pass

    @action(
        macro.mcoast,
        {
            "map_rivers": True,
            "map_coastline": True,
            "map_coastline_thickness": 0,
            "map_grid": False,
            "map_label": False,
        },
        resolution="map_coastline_resolution",
        line_colour="map_rivers_colour",
        line_style="map_rivers_style",
        line_thickness="map_rivers_thickness",
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
        line_colour="map_coastline_colour",
        land_colour="map_coastline_land_shade_colour",
        sea_colour="map_coastline_sea_shade_colour",
        line_style="map_coastline_style",
        line_thickness="map_coastline_thickness",
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
        line_style="map_grid_line_style",
        line_thickness="map_grid_thickness",
        line_colour="map_grid_colour",
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
    def gridlines(self, *args, **kwargs):
        pass

    @action(
        macro.mtext,
        text="text_lines",
    )
    def title(self, text, **kwargs):
        pass

    def _input(self, data):
        if isinstance(data, str):
            file_name = data
            method = {
                "grib": self._grib,
                "netcdf": self._netcdf,
            }[detect_input(file_name)]
        else:
            file_name = data.grib_index()[0][0]
            method = self._grib
        method(file_name)

    def contour_lines(self, data, *args, preset=None, **kwargs):
        """
        Plot line contours on a map.
        """
        self._input(data)
        self._contour_lines(*args, preset=preset, **kwargs)

    def shaded_contours(self, data, *args, style=None, preset=None, **kwargs):
        """
        Plot filled contours on a map.
        """
        self._input(data)

        if isinstance(style, str):
            kwargs["contour_shade_palette_name"] = style

        self._shaded_contours(*args, preset=preset, **kwargs)

    @action(
        macro.mcont,
        {
            "legend": False,
            "contour": False,
            "contour_shade": True,
            "contour_shade_method": "area_fill",
            "contour_interval": {
                "contour_level_selection_type": "interval",
            },
            "contour_level_list": {
                "contour_level_selection_type": "level_list",
            },
            "contour_label_text": {
                "contour_label_type": "text",
            },
            "contour_shade_palette_name": {
                "contour_shade_colour_method": "palette",
            },
        },
        levels="contour_level_list",
        interval="contour_interval",
        interval_reference="contour_reference_level",
        dynamic_levels="contour_level_count",
        fill_pattern="contour_shade_method",
        dot_size="contour_shade_dot_size",
        dot_max_density="contour_shade_max_level_density",
        dot_min_density="contour_shade_min_level_density",
        hatch_index="contour_shade_hatch_index",
        hatch_thickness="contour_shade_hatch_thickness",
        hatch_density="contour_shade_hatch_density",
        shade_type="contour_shade_technique",
        contour_method="contour_method",
    )
    def _shaded_contours(self, *args, **kwargs):
        pass

    @action(
        macro.mcont,
        {
            "legend": False,
            "contour": True,
            "contour_shade": False,
            "contour_interval": {
                "contour_level_selection_type": "interval",
            },
            "contour_level_list": {
                "contour_level_selection_type": "level_list",
            },
            "contour_label_text": {
                "contour_label_type": "text",
            },
        },
        line_style=["contour_line_style", "contour_highlight_style"],
        line_colour=["contour_line_colour", "contour_highlight_colour"],
        line_thickness=["contour_line_thickness", "contour_highlight_thickness"],
        highlight="contour_highlight",
        highlight_colour="contour_highlight_colour",
        highlight_style="contour_highlight_style",
        highlight_thickness="contour_highlight_thickness",
        highlight_frequency="contour_highlight_frequency",
        levels="contour_level_list",
        interval="contour_interval",
        interval_reference="contour_reference_level",
        dynamic_levels="contour_level_count",
        labels="contour_label",
        label_text="contour_label_text",
        label_size="contour_label_height",
        label_blanks="contour_label_blanking",
        label_quality="contour_label_quality",
        label_font="contour_label_font",
        label_font_style="contour_label_font_style",
        label_colour="contour_label_colour",
        label_frequency="contour_label_frequency",
    )
    def _contour_lines(self, *args, **kwargs):
        pass

    @action(
        macro.mgrib,
        file_name="grib_input_file_name",
    )
    def _grib(self, *args, **kwargs):
        pass

    @action(
        macro.mnetcdf,
        {
            "netcdf_value_variable": "psl",
        },
        file_name="netcdf_filename",
    )
    def _netcdf(self, *args, **kwargs):
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
