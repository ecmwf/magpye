
from .. import macro
from ..action import action
from ._data import Data


class Grib(Data):
    
    @action(
        macro.mgrib,
        file_name="grib_input_file_name",
        grib_id="grib_id",
    )
    def _get(self, *args, **kwargs):
        pass