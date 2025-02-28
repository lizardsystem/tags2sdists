Checkoutdir deals with the directory with checkouts of which we need to make
distributions.

CheckoutBaseDir just gives us a list of directories to investigate for tags.
(Note that the test package dir isn't a checkouts dir, but it is enough for
testing the CheckoutBaseDir):

    >>> import importlib
    >>> package_dir = importlib.resources.files("tags2sdists")
    >>> root_dir = importlib.resources.files("tags2sdists").parent.parent
    >>> test_dir = package_dir / 'testpackagedir'
    >>> from tags2sdists import checkoutdir
    >>> checkout_base_dir = checkoutdir.CheckoutBaseDir(test_dir)
    >>> dirs = checkout_base_dir.checkout_dirs()
    >>> len(dirs)
    2

The directories are absolute paths:

    >>> import os
    >>> os.path.join(test_dir, 'package1') == dirs[0]
    True

A checkout directory is wrapped by a CheckoutDir. This in turn uses
zest.releaser. We test everything on ourselves:

    >>> checkout_dir = checkoutdir.CheckoutDir(root_dir)
    >>> print(sorted(checkout_dir.wrapper.vcs.available_tags())[0])
    0.1

``.wrapper.vcs.something``: yes, zest.releaser also does some wrapping, so it
is a bit wrapper inside wrapper, but that's ok. We're only interested in the
missing tags and that's something we can call directly:

    >>> '0.1' in checkout_dir.missing_tags()
    True

If we tell CheckoutDir that 0.1 is already an existing sdist, it won't be
reported as a missing tag:

    >>> checkout_dir = checkoutdir.CheckoutDir(root_dir)
    >>> '0.1' in checkout_dir.missing_tags(existing_sdists=['0.1'])
    False

Create an sdist of 0.1:

    >>> print('start'), checkout_dir.create_sdists('0.1')  #doctest: +ELLIPSIS
    start...
    >>> sorted(os.listdir(os.path.join(checkout_dir.temp_tagdir, 'dist')))
    ['tags2sdists-0.1-py3-none-any.whl', 'tags2sdists-0.1.tar.gz']
    >>> checkout_dir.cleanup()  # Remove the temp tag dir.
