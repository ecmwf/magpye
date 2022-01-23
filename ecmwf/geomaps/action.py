# (C) Copyright 2021- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

from . import presets


def action(magics_macro, conditions=None, default_preset=None, **valid_args):
    

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
