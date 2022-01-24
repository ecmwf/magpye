from .geomap import GeoMap


def get_active_geomap():
    return GeoMapHelper.get_active()


class GeoMapHelper:

    active = None

    EXTENT_KWARGS = {
        "subpage_lower_left_latitude": lambda x, y: x < y,
        "subpage_lower_left_longitude": lambda x, y: x < y,
        "subpage_upper_right_latitude": lambda x, y: x > y,
        "subpage_upper_right_longitude": lambda x, y: x > y,
    }

    @classmethod
    def get_active(cls):
        if cls.active is None:
            cls.active = cls.default_geomap()
        return cls.active

    @classmethod
    def default_geomap(cls):
        return GeoMap(preset="background-foreground")

    @classmethod
    def _modify_bounds(cls, source):
        new_extent = source.extent
        active_extent = [
            cls.active.queue[0].kwargs.get(kwarg) for kwarg in cls.EXTENT_KWARGS
        ]
        for key, new_value in new_extent:
            active_value = active_extent.get(key, new_value)
            if cls.EXTENT_KWARGS[key](new_value, active_value):
                cls.active.queue[0].kwargs[key] = new_value
