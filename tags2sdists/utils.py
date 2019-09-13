try:
    from subprocess import getstatusoutput  # Python 3
except ImportError:
    from commands import getstatusoutput  # Python 2

import logging


logger = logging.getLogger(__name__)


class SdistCreationError(Exception):
    pass


def command(cmd):
    """Execute command and raise an exception upon an error.

      >>> 'README' in command('ls')
      True
      >>> command('nonexistingcommand')  #doctest: +ELLIPSIS
      Traceback (most recent call last):
      ...
      SdistCreationError

    """
    status, out = getstatusoutput(cmd)
    if status != 0:
        logger.error("Something went wrong:")
        logger.error(out)
        raise SdistCreationError()
    return out
