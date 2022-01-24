
from .grib import Grib


class EcData(Grib):

    def get(self, **kwargs):
        file_name, index = self.source.grib_index()[0]
        return self._get(
            file_name, index,
            grib_mode="byte_offset",
            *self.args, **{**self.kwargs, **kwargs},
        )
