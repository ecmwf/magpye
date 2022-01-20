# (C) Copyright 2021- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

from Magics import macro as magics


class Macro:

    PLOTTER = False

    def __init__(self, z_index=1, **kwargs):
        self.z_index = z_index
        self._kwargs = kwargs

    @property
    def macro(self):
        return self.__class__.__name__

    @property
    def kwargs(self):
        return {k: self._sanitise_value(v) for k, v in self._kwargs.items()}

    def execute(self):
        macro = getattr(magics, self.macro)
        return macro(**self.kwargs)

    @staticmethod
    def _sanitise_value(value):
        if isinstance(value, bool):
            value = bool_to_string(value)
        return value


def bool_to_string(boolean):
    return "on" if boolean else "off"


class output(Macro):
    pass


class mtext(Macro):
    pass


class mcont(Macro):
    PLOTTER = True


class mwind(Macro):
    pass


class mlegend(Macro):
    pass


class mmap(Macro):
    pass


class page(Macro):
    pass


class mcoast(Macro):
    pass


class mgrib(Macro):
    pass


class mnetcdf(Macro):
    pass
