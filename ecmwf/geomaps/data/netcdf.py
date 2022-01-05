
from .. import macro
from ..action import action
from ._data import Data


class NetCDF(Data):
    
    @action(
        macro.mnetcdf,
        file_name="netcdf_file_name",
        variable_name="netcdf_value_variable",
    )
    def _get(self, *args, **kwargs):
        pass