
class Data:

    def __init__(self, source, geomap, *args, **kwargs):
        self.source = source
        self.geomap = geomap
        self.args = args
        self.kwargs = kwargs

    def register(self, *args, **kwargs):
        self.geomap.register(*args, **kwargs)

    def get(self):
        return self._get(self.source, *self.args, **self.kwargs)

    def _get(self, *args, **kwargs):
        raise NotImplementedError

    def get_extent(self):
        return dict()
