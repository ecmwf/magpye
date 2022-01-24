from ._helpers import get_active_geomap


def quick_plot(func):
    def plotter(*args, **kwargs):
        geomap = get_active_geomap()
        getattr(geomap, func.__name__)(*args, **kwargs)
        return geomap

    return plotter


def show():
    return get_active_geomap().show()


@quick_plot
def contour_lines(*args, **kwargs):
    pass


@quick_plot
def wind(*args, **kwargs):
    pass


@quick_plot
def rivers(*args, **kwargs):
    pass
