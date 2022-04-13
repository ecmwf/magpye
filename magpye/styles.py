# (C) Copyright 2021- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

import os

import numpy as np
import yaml
from matplotlib import cm, colors

from . import config


def get(style, method_name):
    method_name = method_name.lstrip("_")
    yaml_file = os.path.join(config.PRESETS, method_name, f"{style}.yaml")
    if not os.path.exists(yaml_file):
        raise ValueError(f"no preset '{style}' defined for {method_name}()")

    with open(yaml_file, "r") as f:
        style_definition = yaml.load(f, Loader=yaml.SafeLoader)

    try:
        kwargs = style_definition["style"]
    except KeyError:
        raise TypeError("style definition requires 'style' key")

    return kwargs


class Style:
    def __init__(self, arg, levels=None, number_of_levels=10, exact_levels=True):
        if isinstance(arg, str):
            cmap = cm.get_cmap(arg)
            if levels is not None:
                levels = list(levels)
                number_of_levels = len(levels) - 1
            self.colours = [
                colors.rgb2hex(cmap(i)) for i in np.linspace(0, 1, number_of_levels)
            ]
            self.number_of_levels = number_of_levels + 1
        else:
            self.colours = arg
            self.number_of_levels = len(self.colours) + 1
        self.levels = levels
        self.exact_levels = exact_levels

    @property
    def _magics_kwargs(self):
        # Many of the mcont settings are controlled by GeoMap
        # e.g. contour_shade_method: area_fill
        kwargs = {
            "contour_shade_colour_list": self.colours,
            "contour_shade_colour_method": "list",
            "contour_level_count": self.number_of_levels,
        }
        if self.levels is not None:
            kwargs["contour_level_list"] = self.levels
        if self.exact_levels:
            kwargs["contour_level_tolerance"] = 0
        return kwargs


DEFAULT = Style("inferno")
