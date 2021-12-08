# (C) Copyright 2021- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

import os
import yaml
from Magics import macro as magics
from .config import PATHS


class Macro:
    def __init__(self, *args, **kwargs):
        self._macro_config = None
        self._kwargs = kwargs

        for i, arg in enumerate(args):
            try:
                kwarg = self.args[i]
            except IndexError:
                raise ValueError(
                    f"{self.macro} expected at most {len(self.args)} "
                    f'argument{"s" if len(self.args)>1 else ""}, got '
                    f"{len(args)}"
                )
            kwargs[kwarg] = arg

    @property
    def macro_config(self):
        if self._macro_config is None:
            path = os.path.join(PATHS["macro_config"], f"{self.macro}.yml")
            try:
                with open(path, "r") as f:
                    self._macro_config = yaml.safe_load(f)
            except FileNotFoundError:
                self._macro_config = dict()
        return self._macro_config

    @property
    def thesaurus(self):
        return self.macro_config.get("thesaurus", dict())

    @property
    def requirements(self):
        return self.macro_config.get("requirements", dict())

    @property
    def args(self):
        return self.macro_config["positional_arguments"]

    @property
    def macro(self):
        return self.__class__.__name__

    @property
    def kwargs(self):
        mapped_kwargs = {
            self.thesaurus.get(key, key): value for key, value in self._kwargs.items()
        }
        for key, value in self.requirements.items():
            if key in mapped_kwargs:
                mapped_kwargs = {**mapped_kwargs, **value}
        return mapped_kwargs

    def execute(self):
        macro = getattr(magics, self.macro)
        return macro(**self.kwargs)


def detect_input(data):
    _, format = os.path.splitext(data)
    format = format.lstrip(".")
    macros = {
        "grib": mgrib,
        "grib2": mgrib,
        "nc": mnetcdf,
    }
    try:
        macro = macros[format]
    except KeyError:
        f'unable to plot data of type "{format}"; try grib or netcdf instead'
    return macro


class output(Macro):
    pass


class mtext(Macro):
    pass


class mcont(Macro):
    pass


class mlegend(Macro):
    pass


class mmap(Macro):
    pass


class mcoast(Macro):
    pass


class mgrib(Macro):
    pass


class mnetcdf(Macro):
    pass
