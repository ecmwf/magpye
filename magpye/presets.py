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

from . import config


def get(preset, method_name="GLOBAL"):
    yaml_file = os.path.join(config.PRESETS, method_name, f"{preset}.yaml")
    if not os.path.exists(yaml_file):
        print(yaml_file)
        raise ValueError(f"no preset '{preset}' defined for {method_name}()")

    with open(yaml_file, "r") as f:
        kwargs = yaml.load(f, Loader=yaml.SafeLoader)
    return kwargs
