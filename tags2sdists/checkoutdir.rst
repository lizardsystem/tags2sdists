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

A checkout directory is wrapped by a CheckoutDir. This in turn uses
zest.releaser. We test everything on ourselves:

    >>> testdir = pkg_resources.resource_filename(
    ...     'tags2sdists', '')
    >>> checkout_dir = checkoutdir.CheckoutDir(
    ...     os.path.join(testdir, '..'))
    >>> checkout_dir.wrapper.vcs.available_tags()[0]
    '0.1'

``.wrapper.vcs.something``: yes, zest.releaser also does some wrapping, so it
is a bit wrapper inside wrapper, but that's ok. We're only interested in the
missing tags and that's something we can call directly:

    >>> '0.1' in checkout_dir.missing_tags()
    True

If we tell CheckoutDir that 0.1 is already an existing sdist, it won't be
reported as a missing tag:

    >>> checkout_dir = checkoutdir.CheckoutDir(
    ...     os.path.join(testdir, '..'))
    >>> '0.1' in checkout_dir.missing_tags(existing_sdists=['0.1'])
    False

Create an sdist of 0.1:

    >>> checkout_dir.create_sdist('0.1')  #doctest: +ELLIPSIS
    Note: checking out '0.1'.
    ...tags2sdists-0.1.tar.gz'
    >>> checkout_dir.cleanup()  # Remove the temp tag dir.
