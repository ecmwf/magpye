
from .. import macro
from ..action import action
from ._data import Data


class Grib(Data):
    
    @action(
        macro.mgrib,
        {
            "grib_file_address_mode": "byte_offset",
        },
        file_name="grib_input_file_name",
        index="grib_field_position",
        grib_id="grib_id",
    )
    def _get(self, *args, **kwargs):
        pass