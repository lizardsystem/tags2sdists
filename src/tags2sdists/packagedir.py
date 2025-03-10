import collections
import logging
import os
import shutil

logger = logging.getLogger(__name__)


class PackageDir:
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
            names = [package]
            if "-" in package:
                names.append(package.replace("-", "_"))
            if "." in package:
                names.append(package.replace(".", "_"))
            for tarball in dir_contents:
                if not tarball.endswith(".tar.gz"):
                    continue
                for name in names:
                    if tarball.startswith(name + "-"):
                        version = tarball.replace(".tar.gz", "").replace(name + "-", "")
                        self.packages[package].append(version)

    def add_tarball(self, tarball, package):
        """Add a tarball, possibly creating the directory if needed."""
        if tarball is None:
            logger.error(
                "No tarball found for %s: probably a renamed project?", package
            )
            return
        target_dir = os.path.join(self.root_directory, package)
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
            logger.info("Created %s", target_dir)
        logger.info("Copying tarball to %s", target_dir)
        shutil.copy(tarball, target_dir)
