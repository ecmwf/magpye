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
from . import macro


class Figure:
    def __init__(self, *args, **kwargs):
        self.queue = []
        self._map(*args, **kwargs)

    def register(self, item):
        self.queue.append(item)

    def _map(self, *args, **kwargs):
        self.register(macro.mmap(*args, **kwargs))

    def title(self, text, **kwargs):
        self.register(macro.mtext(text_lines=text, **kwargs))

    def land(self, *args, **kwargs):
        self.register(macro.mcoast(*args, **kwargs))

    def coastlines(self, *args, **kwargs):
        self.register(macro.mcoast(*args, **kwargs))

    def contour(self, data, *args, **kwargs):
        input_macro = macro.detect_input(data)
        self.register(input_macro(data))
        self.register(macro.mcont(*args, **kwargs))

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
        queue = output + self.queue
        return magics.plot(*(macro.execute() for macro in queue))
