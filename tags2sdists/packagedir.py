import collections
import os


class PackageDir(object):
    """Wrapper around the target package directory.

    So: directories named after packages with package-VERSION.tar.gz files in
    them.

    """

    def __init__(self, root_directory):
        """Initialize with the root of the packages dir."""
        self.root_directory = root_directory
        self.packages = collections.defaultdict(list)

    def parse(self):
        """Iterate through the directory and extract package/version info."""
        for package in os.listdir(self.root_directory):
            directory = os.path.join(self.root_directory, package)
            if not os.path.isdir(directory):
                continue
            dir_contents = os.listdir(directory)
            sdists = [tarball for tarball in dir_contents
                      if (tarball.endswith('.tar.gz')
                          and tarball.startswith(package + '-'))]
            for sdist in sdists:
                version = sdist.replace('.tar.gz', '').replace(
                    package + '-', '')
                self.packages[package].append(version)
