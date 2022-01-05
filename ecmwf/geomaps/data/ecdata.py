
from .grib import Grib


class EcData(Grib):
    
    def get(self):
        file_name, index = self.source.grib_index()[-1]
        return self._get(file_name, index, *self.args, **self.kwargs)