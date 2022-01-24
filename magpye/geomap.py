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

from . import data, macro
from .action import action

ARROW_STYLES = ["angle", "triangle", "triangle2", "triangle3"]


class GeoMap:
    """
    Class for designing and plotting geospatial maps.

    Parameters
    ----------
    area_name : str, optional
        The name of a an area (e.g. 'europe') with a pre-configured projection
        and extent - see examples for a sample of valid area names.
    projection : str, optional
        The name of the map projection to use for this map. See examples for
        a sample of valid projections.
    extent : tuple, optional
        A four-element list/tuple containing the latitude and longitude
        extents to use in the map. These must be provided in the order: lower-
        left latitude, lower-left longitude, upper-right latitude, upper-right
        longitude.
    """

    def __init__(self, *args, **kwargs):
        self._sources = []

        self.queue = []
        self._map(*args, **kwargs)

        self._show_legend = False

    def register(self, item):
        if item.__class__.__name__ == "page":
            self.queue = [self.queue[0]] + [item] + self.queue[1:]
        else:
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
            "page_id_line": False,
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
        macro.page,
        {
            "page_id_line": True,
            "page_id_line_logo_name": {"page_id_line_logo_plot": True},
            "page_id_line_logo_plot": False,
            "page_id_line_system_plot": False,
            "page_id_line_date_plot": False,
            "page_id_line_magics": False,
            "page_id_line_errors_plot": False,
            "page_id_line_colour": "charcoal",
        },
        text="page_id_line_user_text",
        font="page_id_line_font",
        font_style="page_id_line_font_style",
        font_size="page_id_line_height",
        font_colour="page_id_line_colour",
        logo="page_id_line_logo_name",
        datestamp="page_id_line_date_plot",
    )
    def footer(self, *args, **kwargs):
        """
        Add a footer to the bottom of the plot, containing text and/or a logo.

        Parameters
        ----------
        text : str, optional
            A string of text to include in the footer.
        font : str, default='sansserif'
            The name of the font to use for footer text.
        font_style : str, default='normal'
            Style options for the footer font, e.g. `'bold'`.
        font_size : float, optional
            The font size to use, in cm.
        font_colour : str, default='charcoal'
            Either a hexadecimal colour or a named colour to use for the
            footer font.
        logo : bool or str, optional
            The name of an organisation or project whose logo should be added
            to the footer. Must be one of `'ecmwf'`, `'c3s'` or `'cams'` - or
            `False` if no logo should be included (default).
        datestamp : bool, optional
            If `True`, the date and time at which the map was generated will
            be included in the footer text.
        """
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
        """
        Add rivers to the map.

        Parameters
        ----------
        resolution : str, default='low'
            The resolution of the rivers to be included in the map. Must be
            one of `'low'`, `'medium'` or `'high'`.
        line_colour : str, default='blue'
            Either a hexadecimal colour or a named colour to use for the
            river lines.
        line_style : str, default='solid'
            One of `'solid'`, `'dash'`, `'dot'`, `'chain_dash'`, or
            `'chain_dot'`.
        line_thickness : float, default=1.0
            The thickness of the river lines.
        """
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
        line_style="map_coastline_style",
        line_thickness="map_coastline_thickness",
        land_colour="map_coastline_land_shade_colour",
        ocean_colour="map_coastline_sea_shade_colour",
    )
    def coastlines(self, *args, **kwargs):
        """
        Add coastlines to the map.

        Parameters
        ----------
        resolution : str, default='low'
            The resolution of the coastlines to be included in the map. Must
            be one of `'low'`, `'medium'` or `'high'`.
        line_colour : str, default='black'
            Either a hexadecimal colour or a named colour to use for the
            coastlines.
        line_style : str, default='solid'
            One of `'solid'`, `'dash'`, `'dot'`, `'chain_dash'`, or
            `'chain_dot'`.
        line_thickness : float, default=1.0
            The thickness of the coastlines.
        land_colour : str, optional
            Either a hexadecimal colour or a named colour to use for the fill
            colour of areas within coastline polygons (i.e. land).
        ocean_colour : str, optional
            Either a hexadecimal colour or a named colour to use for the fill
            colour of areas outside coastlines (i.e. oceans).
        """
        pass

    @action(
        macro.mcoast,
        {
            "map_coastline": False,
            "map_grid": True,
        },
        lat_frequency="map_grid_latitude_increment",
        lon_frequency="map_grid_longitude_increment",
        lat_reference="map_grid_latitude_reference",
        lon_reference="map_grid_longitude_reference",
        line_colour="map_grid_colour",
        line_style="map_grid_line_style",
        line_thickness="map_grid_thickness",
        labels="map_label",
        label_font="map_label_font_style",
        label_font_size="map_label_height",
        label_font_colour="map_label_colour",
        label_latitude_frequency="map_label_latitude_frequency",
        label_longitude_frequency="map_label_longitude_frequency",
        label_top_edge="map_label_top",
        label_bottom_edge="map_label_bottom",
        label_left_edge="map_label_left",
        label_right_edge="map_label_right",
    )
    def gridlines(self, *args, **kwargs):
        """
        Add gridlines to the map.

        Parameters
        ----------
        lat_frequency : float, default=10
            The interval in degrees of latitude between each latitude grid
            line.
        lon_frequency : float, default=20
            The interval in degrees of longitude between each longitude grid
            line.
        lat_reference : float, default=0
            The reference/starting latitude from which to begin drawing
            latitude lines at a frequency given by `lat_frequency`.
        lon_reference : float, default=0
            The reference/starting longitude from which to begin drawing
            longitude lines at a frequency given by `lon_frequency`.
        line_colour : str, default='blue'
            Either a hexadecimal colour or a named colour to use for the
            river lines.
        line_style : str, default='solid'
            One of `'solid'`, `'dash'`, `'dot'`, `'chain_dash'`, or
            `'chain_dot'`.
        line_thickness : float, default=1.0
            The thickness of the river lines.
        labels : bool, optional
            If `True`, gridlines will be given latitude and longitude labels.
        label_font : str, default='sansserif'
            The name of the font to use for gridline label text.
        label_font_size : float, optional
            The font size to use, in cm.
        label_font_colour : str, default='charcoal'
            Either a hexadecimal colour or a named colour to use for the
            gridline label font.
        label_latitude_frequency : int, optional
            The frequency at which to label latitude gridlines. A frequency of
            1 means every latitude gridline will be labelled.
        label_longitude_frequency : int, optional
            The frequency at which to label longitude gridlines. A frequency
            of 1 means every longitude gridline will be labelled.
        label_top_edge : bool, default=True
            If `True`, labels will be drawn where gridlines intersect the top
            edge/border of the map.
        label_bottom_edge : bool, default=True
            If `True`, labels will be drawn where gridlines intersect the
            bottom edge/border of the map.
        label_left_edge= : bool, default=True
            If `True`, labels will be drawn where gridlines intersect the
            left edge/border of the map.
        label_right_edge : bool, default=True
            If `True`, labels will be drawn where gridlines intersect the
            right edge/border of the map.
        """
        pass

    @action(
        macro.mtext,
        {
            "text_colour": "charcoal",
        },
        text="text_lines",
        text_colour="text_colour",
    )
    def title(self, text, **kwargs):
        """
        Add a title above the map.
        """
        pass

    def _input(self, source, **kwargs):
        source = data.detect_source(source, self)
        self._sources.append(source)
        source.get(**kwargs)

    def _vector_input(self, *args, wind_mode="uv", **kwargs):
        source = data.detect_vector_source(*args, wind_mode=wind_mode, geomap=self)
        self._sources.append(source)
        source.get(**kwargs)

    def contour_lines(self, source, *args, style=None, **kwargs):
        """
        Plot line contours on a map.
        """
        self._input(source)
        self._contour_lines(*args, style=style, **kwargs)

    def contour_shaded(self, source, *args, style=None, **kwargs):
        """
        Plot filled contours on a map.
        """
        self._input(source)
        self._contour_shaded(*args, style=style, **kwargs)

    def arrows(
        self,
        *,
        u=None,
        v=None,
        speed=None,
        direction=None,
        shaded=False,
        style=None,
        **kwargs,
    ):
        """
        Plot arrows on a map.
        """
        if all((u, v)):
            self._vector_input(u, v, wind_mode="uv")
        elif all((speed, direction)):
            self._vector_input(speed, direction, wind_mode="sd")
        else:
            raise TypeError("arrows() requires u and v OR speed and direction")

        method = self._arrows if not shaded else self._arrows_shaded

        return self._vector(method, style=style, **kwargs)

    def _vector(self, plotter, *args, **kwargs):

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
    def _contour_shaded(self, *args, **kwargs):
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
    def _arrows(self, *args, **kwargs):
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
    def _arrows_shaded(self, *args, **kwargs):
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
            "legend_text_colour": "charcoal",
            "legend_title_font_colour": "charcoal",
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
            kwargs["output_name"] = name
            kwargs["output_name_first_page_number"] = False
            kwargs["output_formats"] = [format.lstrip(".")]
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
        result = magics.plot(*(macro.execute() for macro in queue))

        self._sources = []

        return result
