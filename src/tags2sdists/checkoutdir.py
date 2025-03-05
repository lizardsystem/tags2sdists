import logging
import os
import shutil
import sys
from pathlib import Path

import packaging
from packaging.version import parse as parse_version
from zest.releaser import release

from tags2sdists.utils import command

logger = logging.getLogger(__name__)


def find_tarballs(directory: Path, name: str, version: str) -> list[Path]:
    """Return matching tarball/wheel paths from dist/ dir (if found).

    Setuptools generates a source distribution in a ``dist/`` directory and we
    need to find the exact filename, whether .tgz or .zip.

    We expect "name + '-' + version + '.tar.gz'", but we *can* get a
    -dev.r1234.tar.gz as that can be configured in a setup.cfg.  Not pretty,
    but we don't want to force anyone to modify old tags.

    """
    dir_contents = os.listdir(os.path.join(directory, "dist"))
    candidates = [
        tarball
        for tarball in dir_contents
        if (tarball.endswith(".gz") or tarball.endswith(".whl"))
        and (
            tarball.startswith(name + "-" + version)
            or tarball.startswith(name.replace("-", "_") + "-" + version)
        )
    ]
    if not candidates:
        logger.error(
            "No recognizable distribution found for %s, version %s", name, version
        )
        logger.error("Contents of %s: %r", directory, dir_contents)
        return []
    tarballs = [(directory / "dist" / candidate) for candidate in candidates]
    return tarballs


class CheckoutBaseDir:
    """Wrapper around the directory containing the checkout directories."""

    def __init__(self, base_directory):
        self.base_directory = base_directory

    def checkout_dirs(self):
        """Return directories inside the base directory."""
        directories = [
            os.path.join(self.base_directory, d)
            for d in os.listdir(self.base_directory)
        ]
        return sorted([d for d in directories if os.path.isdir(d)])


def sorted_versions(versions):
    result = []
    for version in versions:
        try:
            result.append(parse_version(version))
        except packaging.version.InvalidVersion:
            logger.warning(f"Tag found that isn't a valid version: {version}")

    return result


class CheckoutDir:
    """Wrapper around a directory with a checkout in it."""

    def __init__(self, directory):
        self._missing_tags = None
        self.start_directory = directory
        os.chdir(directory)
        self.wrapper = release.Releaser()
        self.wrapper.prepare()  # zest.releaser requirement.
        self.package = self.wrapper.vcs.name

    def missing_tags(self, existing_sdists=None, build_all=False):
        """Return difference between existing sdists and available tags."""
        if existing_sdists is None:
            existing_sdists = []
        logger.debug("Existing sdists: %s", existing_sdists)
        if self._missing_tags is None:
            missing = []
            existing_sdists = sorted_versions(set(existing_sdists))
            available = set(self.wrapper.vcs.available_tags())
            available_tags = sorted_versions(available)
            available_tags.reverse()
            for tag in available_tags:
                if tag.is_prerelease:
                    logger.warning("Pre-release marker in tag: %s, ignoring", tag)
                    continue
                if tag in existing_sdists:
                    if not build_all:
                        # Tag found. We're looking from the newest to the oldest.
                        # We're not building all tags, so we omit (possibly faulty)
                        # older tags. (This is the default).
                        logger.debug(
                            "Tag %s is already available, not looking further", tag
                        )
                        break
                    else:
                        # Tag found. We keep looking. (--build-all has been used)
                        continue
                else:
                    missing.append(tag)
                    logger.debug("Tag %s is missing", tag)
            missing.reverse()
            # Convert back to proper strings:
            mapping = {}
            for tag in available:
                mapping[parse_version(tag)] = tag
            self._missing_tags = [mapping[tag] for tag in missing]
        if self._missing_tags:
            logger.info("Missing sdists for %s: %s", self.package, self._missing_tags)
        else:
            logger.info("Ok: %s", self.package)
        return self._missing_tags

    def create_sdists(self, tag: str) -> list[Path]:
        """Create an sdist/wheel and return the full file paths of the .tar.gz. and .whl"""
        logger.info("Making tempdir for %s with tag %s...", self.package, tag)
        self.wrapper.vcs.checkout_from_tag(tag)
        # checkout_from_tag() chdirs to a temp directory that we need to clean up
        # later.
        self.temp_tagdir = Path(os.path.realpath(os.getcwd()))
        logger.debug("Tag checkout placed in %s", self.temp_tagdir)
        python = sys.executable
        logger.debug(command(f"{python} -m build --sdist"))
        # ^^^ No wheels as they can be binary.
        tarballs = find_tarballs(self.temp_tagdir, self.package, tag)
        return tarballs

    def cleanup(self):
        """Clean up temporary tag checkout dir."""
        shutil.rmtree(self.temp_tagdir)
        # checkout_from_tag might operate on a subdirectory (mostly
        # 'gitclone'), so cleanup the parent dir as well
        parentdir = os.path.dirname(self.temp_tagdir)
        # ensure we don't remove anything important
        if os.path.basename(parentdir).startswith(self.package):
            os.rmdir(parentdir)
        os.chdir(self.start_directory)
