import logging
import os
import shutil
import sys

from zest.releaser import release

from tags2sdists.utils import command

logger = logging.getLogger(__name__)


def find_tarball(directory, name, version):
    """Return matching tarball filename from dist/ dir (if found).

    Setuptools generates a source distribution in a ``dist/`` directory and we
    need to find the exact filename, whether .tgz or .zip.

    We expect "name + '-' + version + '.tar.gz'", but we *can* get a
    -dev.r1234.tar.gz as that can be configured in a setup.cfg.  Not pretty,
    but we don't want to force anyone to modify old tags.

    """
    dir_contents = os.listdir(os.path.join(directory, 'dist'))
    candidates = [tarball for tarball in dir_contents
                  if tarball.endswith('.gz')
                  and tarball.startswith(name + '-' + version)]
    if not candidates:
        logger.error("No recognizable distribution found for %s, version %s",
                     name, version)
        logger.error("Contents of %s: %r", directory, dir_contents)
        return
    if len(candidates) > 1:
        # Should not happen.
        logger.warn("More than one candidate distribution found: %r",
                    candidates)
    tarball = candidates[0]
    return os.path.join(directory, 'dist', tarball)


class CheckoutBaseDir(object):
    """Wrapper around the directory containing the checkout directories."""

    def __init__(self, base_directory):
        self.base_directory = base_directory

    def checkout_dirs(self):
        """Return directories inside the base directory."""
        directories = [os.path.join(self.base_directory, d)
                       for d in os.listdir(self.base_directory)]
        return [d for d in directories if os.path.isdir(d)]


class CheckoutDir(object):
    """Wrapper around a directory with a checkout in it."""

    def __init__(self, directory):
        self._missing_tags = None
        self.start_directory = directory
        os.chdir(directory)
        self.wrapper = release.Releaser()
        self.wrapper.prepare()  # zest.releaser requirement.
        self.package = self.wrapper.vcs.name

    def missing_tags(self, existing_sdists=None):
        """Return difference between existing sdists and available tags."""
        if existing_sdists is None:
            existing_sdists = set()
        else:
            existing_sdists = set(existing_sdists)
        logger.debug("Existing sdists: %s", existing_sdists)
        if self._missing_tags is None:
            # So, this can only be called once, effectively :-)
            self._missing_tags = list(
                set(self.wrapper.vcs.available_tags()) - existing_sdists)
        logger.debug("Missing sdists: %s", self._missing_tags)
        return self._missing_tags

    def create_sdist(self, tag):
        """Create an sdist and return the full file path of the .tar.gz."""
        logger.info("Making tempdir for %s with tag %s...",
                    self.package, tag)
        self.wrapper.vcs.checkout_from_tag(tag)
        # checkout_from_tag() chdirs to a temp directory that we need to clean up
        # later.
        self.temp_tagdir = os.path.realpath(os.getcwd())
        logger.debug("Tag checkout placed in %s", self.temp_tagdir)
        python = sys.executable
        logger.debug(command("%s setup.py sdist" % python))
        tarball = find_tarball(self.temp_tagdir, self.package, tag)
        return tarball

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
