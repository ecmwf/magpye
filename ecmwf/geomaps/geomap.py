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

from . import data, macro, presets
from .action import action

ARROW_STYLES = ["angle", "triangle", "triangle2", "triangle3"]


class GeoMap:
    """Class for designing and plotting geospatial maps."""

    def __init__(self, *args, preset=None, **kwargs):

        self.queue = []
        self._map(*args, **kwargs)

        self.apply_preset(preset)

        self._show_legend = False

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
        {
            "subpage_map_area_name": {"subpage_map_library_area": True},
            "subpage_expand_mode": True,
            "subpage_clipping": True,
        },
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
        label_latitude_frequency="map_label_latitude_frequency",
        label_longintude_frequency="map_label_longitude_frequency",
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

    def _input(self, source, **kwargs):
        source = data.detect_source(source, self)
        source.get(**kwargs)

    def contour_lines(self, source, *args, preset=None, **kwargs):
        """
        Plot line contours on a map.
        """
        self._input(source)
        self._contour_lines(*args, preset=preset, **kwargs)

    def contour_shaded(self, source, *args, style=None, preset=None, **kwargs):
        """
        Plot filled contours on a map.
        """
        self._input(source)

        if isinstance(style, str):
            kwargs["contour_shade_palette_name"] = style

        self._shaded_contours(*args, preset=preset, **kwargs)

    def waves(self, source, *args, preset=None, **kwargs):
        return self._vector(
            self._input(source, wind_mode="sd"),
            self._wind,
            *args,
            preset=preset,
            **kwargs,
        )

    def waves_shaded(self, source, *args, preset=None, **kwargs):
        return self._vector(
            self._input(source, wind_mode="sd"),
            self._wind_shaded,
            *args,
            preset=preset,
            **kwargs,
        )

    def wind(self, source, *args, preset=None, **kwargs):
        """
        Plot wind arrows on a map.
        """
        return self._vector(
            self._input(source), self._wind, *args, preset=preset, **kwargs
        )

    def wind_shaded(self, source, *args, preset=None, **kwargs):
        """
        Plot coloured wind arrows on a map.
        """
        return self._vector(
            self._input(source), self._wind_shaded, *args, preset=preset, **kwargs
        )

    def _vector(self, input, plotter, *args, **kwargs):

        arrow_head = kwargs.pop("arrow_head", None)
        if arrow_head is not None:
            if "-" in arrow_head:
                style, angle = arrow_head.split("-")
            else:
                style, angle = arrow_head, 45
            kwargs["_arrow_shape"] = ARROW_STYLES.index(style)
            kwargs["_arrow_ratio"] = int(angle) / 90

        plotter(*args, **kwargs)

    @action(
        macro.mcont,
        {
            "legend": True,
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
        legend="legend",
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
        legend="legend",
    )
    def _contour_lines(self, *args, **kwargs):
        pass

    @action(
        macro.mwind,
        {
            "legend": False,
            "wind_thinning_method": "automatic",
            "wind_arrow_calm_below": {"wind_arrow_calm_indicator": True},
            "wind_flag_calm_below": {"wind_flag_calm_indicator": True},
        },
        wind_style="wind_field_type",
        colour=["wind_flag_colour", "wind_arrow_colour"],
        flag_length="wind_flag_length",
        flag_origin_marker="wind_flag_origin_marker",
        flag_origin_size="wind_flag_origin_marker_size",
        density="wind_thinning_factor",
        calm_threshold=["wind_arrow_calm_below", "wind_flag_calm_below"],
        calm_indicator_size=[
            "wind_arrow_calm_indicator_size",
            "wind_flag_calm_indicator_size",
        ],
        _arrow_shape="wind_arrow_head_shape",
        _arrow_ratio="wind_arrow_head_ratio",
        max_speed=["wind_arrow_max_speed", "wind_flag_max_speed"],
        min_speed=["wind_arrow_min_speed", "wind_flag_min_speed"],
        arrow_origin="wind_arrow_origin_position",
        line_thickness=["wind_arrow_thickness", "wind_flag_thickness"],
        line_style=["wind_arrow_style", "wind_flag_style"],
        legend="legend",
    )
    def _wind(self, *args, **kwargs):
        pass

    @action(
        macro.mwind,
        {
            "legend": False,
            "wind_advanced_method": True,
            "wind_thinning_method": "automatic",
            "wind_arrow_calm_below": {"wind_arrow_calm_indicator": True},
            "wind_flag_calm_below": {"wind_flag_calm_indicator": True},
            "contour_level_count": {
                "wind_advanced_colour_selection_type": "count",
            },
            "contour_interval": {
                "wind_advanced_colour_selection_type": "interval",
            },
            "contour_level_list": {
                "wind_advanced_colour_selection_type": "list",
            },
            "wind_advanced_colour_list": {
                "wind_advanced_colour_table_colour_method": "list",
            },
            "contour_shade_min_level_colour": {
                "wind_advanced_colour_table_colour_method": "calculate",
            },
        },
        wind_style="wind_field_type",
        flag_length="wind_flag_length",
        flag_origin_marker="wind_flag_origin_marker",
        flag_origin_size="wind_flag_origin_marker_size",
        density="wind_thinning_factor",
        calm_threshold=["wind_arrow_calm_below", "wind_flag_calm_below"],
        calm_indicator_size=[
            "wind_arrow_calm_indicator_size",
            "wind_flag_calm_indicator_size",
        ],
        _arrow_shape="wind_arrow_head_shape",
        _arrow_ratio="wind_arrow_head_ratio",
        max_speed=[
            "wind_arrow_max_speed",
            "wind_flag_max_speed",
            "contour_max_level",
            "contour_shade_max_level",
            "wind_advanced_colour_max_value",
        ],
        min_speed=[
            "wind_arrow_min_speed",
            "wind_flag_min_speed",
            "contour_min_level",
            "contour_shade_min_level",
            "wind_advanced_colour_min_value",
        ],
        arrow_origin="wind_arrow_origin_position",
        line_thickness=["wind_arrow_thickness", "wind_flag_thickness"],
        line_style=["wind_arrow_style", "wind_flag_style"],
        bin_count=["contour_level_count", "wind_advanced_colour_level_count"],
        bin_tolerance=[
            "contour_level_tolerance",
            "wind_advanced_colour_level_tolerance",
        ],
        bin_reference=[
            "contour_reference_level",
            "wind_advanced_colour_reference_level",
        ],
        bin_interval=["contour_interval", "wind_advanced_colour_level_interval"],
        bins=["contour_level_list", "wind_advanced_colour_level_list"],
        colours="wind_advanced_colour_list",
        min_colour=[
            "contour_shade_min_level_colour",
            "wind_advanced_colour_min_level_colour",
        ],
        max_colour=[
            "contour_shade_max_level_colour",
            "wind_advanced_colour_max_level_colour",
        ],
        colour_wheel_direction=[
            "contour_shade_colour_direction",
            "wind_advanced_colour_direction",
        ],
        legend="legend",
    )
    def _wind_shaded(self, *args, **kwargs):
        pass

    def legend(self, *args, **kwargs):
        self._show_legend = True
        position = kwargs.pop("position", None)
        if position is not None:
            if isinstance(position, (list, tuple)):
                try:
                    (
                        kwargs["_user_x_position"],
                        kwargs["_user_y_position"],
                        kwargs["_user_x_length"],
                        kwargs["_user_y_length"],
                    ) = position
                except ValueError:
                    raise ValueError("position expects [x, x_len, y, y_len]")
            else:
                kwargs["_auto_position"] = position
        return self._legend(*args, **kwargs)

    @action(
        macro.mlegend,
        {
            "legend_display_type": "continuous",
            "legend_title_text": {"legend_title": True},
            "legend_user_minimum_text": {"legend_user_minimum": True},
            "legend_user_maximum_text": {"legend_user_maximum": True},
            "legend_box_x_position": {"legend_box_mode": "positional"},
        },
        text_colour=["legend_text_colour", "legend_title_font_colour"],
        title="legend_title_text",
        title_text_colour="legend_title_font_colour",
        title_orientation="legend_title_orientation",
        title_font_size="legend_title_font_size",
        title_position="legend_title_position",
        minimum_text="legend_user_minimum_text",
        maximum_text="legend_user_maximum_text",
        display_type="legend_display_type",
        label_frequency="legend_label_frequency",
        _auto_position="legend_automatic_position",
        _user_x_position="legend_box_x_position",
        _user_y_position="legend_box_y_position",
        _user_x_length="legend_box_x_length",
        _user_y_length="legend_box_y_length",
    )
    def _legend(self, *args, **kwargs):
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
        if not self._show_legend:
            for item in self.queue:
                if item.PLOTTER:
                    item._kwargs["legend"] = False
        output = [output] if output is not None else []
        queue = output + sorted(self.queue, key=lambda x: x.z_index)
        return magics.plot(*(macro.execute() for macro in queue))
