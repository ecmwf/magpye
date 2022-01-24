# (C) Copyright 2021- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

from functools import wraps

from . import styles


def action(magics_macro, conditions=None, **valid_args):
    """
    Decorator for generating figure methods.

    Parameters
    ----------
    magics_macro : magpye.macro.Macro
        The Magics macro to execute for this action.
    condition : dict
        A dctionary of conditional variables which are
        required for the given action to execute on the given macro.
        Values can be sub-dictionaries, indicating that the condition is
        only required when a specific argument is passed.
    valid_args : dict
        A mapping of argument names to their Magics counterparts.
    """

    def decorator(method):
        @wraps(method)
        def wrapper(self, *args, style=None, z_index=1, **kwargs):
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

            if style is not None:
                mapped_kwargs = {
                    **styles.get(style, method.__name__),
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
