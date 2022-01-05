
from .grib import Grib


class EcData(Grib):
    
    def get(self):
        file_name, grib_id = self.source.grib_index()[-1]
        return self._get(file_name, grib_id, *self.args, **self.kwargs)