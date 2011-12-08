# Script to tie it all together

import logging
import optparse
import os

from tags2sdists import checkoutdir
from tags2sdists import packagedir

logger = logging.getLogger(__name__)


def main():
    """bin/tags2sdists: create an sdist for a directory of checkouts."""
    usage = ("Usage: %prog CHECKOUTDIR SDISTDIR\n"
             "    CHECKOUTDIR: directory with checkouts\n"
             "    SDISTDIR: directory with sdist package directories")
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="Show debug output")
    parser.add_option("-q", "--quiet",
                      action="store_true", dest="quiet", default=False,
                      help="Show minimal output")
    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.print_help()
        return 1
    checkouts_dir = args[0]
    sdists_dir = args[1]
    checkouts_dir = os.path.abspath(checkouts_dir)
    sdists_dir = os.path.abspath(sdists_dir)
    if options.verbose:
        log_level = logging.DEBUG
    elif options.quiet:
        log_level = logging.WARN
    else:
        log_level = logging.INFO
    logging.basicConfig(level=log_level,
                        format="%(levelname)s: %(message)s")

    logger.info("Looking in %s for new sdists to generate into %s.",
                checkouts_dir, sdists_dir)
    package_dir = packagedir.PackageDir(sdists_dir)
    package_dir.parse()
    checkout_base_dir = checkoutdir.CheckoutBaseDir(checkouts_dir)
    for directory in checkout_base_dir.checkout_dirs():
        logger.debug("Looking at directory %s...", directory)
        checkout_dir = checkoutdir.CheckoutDir(directory)
        package = checkout_dir.package
        if 'Traceback' in package:
            # Some error in the setup.py and we don't want to have a Traceback
            # directory in our sdists dir :-)
            continue
        for tag in checkout_dir.missing_tags(
            existing_sdists=package_dir.packages[package]):
            tarball = checkout_dir.create_sdist(tag)
            package_dir.add_tarball(tarball, package)
            checkout_dir.cleanup()
