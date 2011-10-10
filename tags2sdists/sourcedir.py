import os

import zest.releaser


class SourceBaseDir(object):
    """Wrapper around the directory containing the source directories."""

    def __init__(self, base_directory):
        self.base_directory = base_directory

    def source_dirs(self):
        """Return directories inside the base directory."""
        directories = [os.path.join(self.base_directory, d)
                       for d in os.listdir(self.base_directory)]
        return [d for d in directories if os.path.isdir(d)]



