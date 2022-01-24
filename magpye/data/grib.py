
from .. import macro
from ..action import action
from ._data import Data


class Grib(Data):

    @action(
        macro.mgrib,
        {
            "grib_automatic_scaling": False,
        },
        file_name="grib_input_file_name",
        index="grib_field_position",
        grib_id="grib_id",
        grib_mode="grib_file_address_mode",
        wind_mode="grib_wind_mode",
        wind_1="grib_wind_position_1",
        wind_2="grib_wind_position_2",
    )
    def _get(self, *args, **kwargs):
        pass
