
import os
import tempfile


class TmpFile:
    """The TmpFile objets are designed to be used for temporary files.
    It ensures that the file is unlinked when the object is
    out-of-scope (with __del__).
    Parameters
    ----------
    path : str
        Actual path of the file.
    """

    def __init__(self, path: str):
        self.path = path

    def __del__(self):
        self.cleanup()

    def __enter__(self):
        return self.path

    def __exit__(self, *args, **kwargs):
        self.cleanup()

    def cleanup(self):
        if self.path is not None:
            os.unlink(self.path)
        self.path = None


def temp_file(extension=".tmp") -> TmpFile:
    """Create a temporary file with the given extension .
    Parameters
    ----------
    extension : str, optional
        By default ".tmp"
    Returns
    -------
    TmpFile
    """

    fd, path = tempfile.mkstemp(suffix=extension)
    os.close(fd)
    return TmpFile(path)


class TmpDirectory(tempfile.TemporaryDirectory):
    @property
    def path(self):
        return self.name


def temp_directory():
    return TmpDirectory()
