# Script to tie it all together

import logging
import optparse


logger = logging.getLogger(__name__)


def main():
    """bin/make_sdists: create an sdist for a directory of checkouts."""
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
    if options.verbose:
        log_level = logging.DEBUG
    elif options.quiet:
        log_level = logging.WARN
    else:
        log_level = logging.INFO
    logging.basicConfig(level=log_level,
                        format="%(levelname)s: %(message)s")
