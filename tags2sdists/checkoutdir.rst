Checkoutdir deals with the directory with checkouts of which we need to make
distributions.

CheckoutBaseDir just gives us a list of directories to investigate for tags.
(Note that the test package dir isn't a checkouts dir, but it is enough for
testing the CheckoutBaseDir):

    >>> import pkg_resources
    >>> testdir = pkg_resources.resource_filename(
    ...     'tags2sdists', 'testpackagedir')
    >>> from tags2sdists import checkoutdir
    >>> checkout_base_dir = checkoutdir.CheckoutBaseDir(testdir)
    >>> dirs = checkout_base_dir.checkout_dirs()
    >>> len(dirs)
    2

The directories are absolute paths:

    >>> import os
    >>> os.path.join(testdir, 'package1') == dirs[0]
    True
