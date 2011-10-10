Packagedir wraps a directory with source distributions:

    >>> from tags2sdists import packagedir
    >>> package_dir = packagedir.PackageDir(None)
    >>> package_dir.packages
    defaultdict(<type 'list'>, {})

We have a testdir with some dummy packages for testing the parsing of the
directory structure:

    >>> import pkg_resources
    >>> testdir = pkg_resources.resource_filename(
    ...     'tags2sdists', 'testpackagedir')
    >>> package_dir = packagedir.PackageDir(testdir)
    >>> package_dir.parse()
    >>> sorted(package_dir.packages.keys())
    ['package1', 'package2']
    >>> sorted(package_dir.packages['package1'])
    ['0.1', '0.2']

For adding tarballs, we use a temporary directory:

    >>> import tempfile
    >>> tempdir = tempfile.mkdtemp()
    >>> import os
    >>> 'package1' in os.listdir(tempdir)
    False
    >>> package_dir = packagedir.PackageDir(tempdir)
    >>> package_dir.parse()
    >>> sorted(package_dir.packages.keys())
    []
    >>> test_tarball = os.path.join(testdir, 'package1',
    ...                             'package1-0.1.tar.gz')
    >>> package_dir.add_tarball(test_tarball, 'package1')
    >>> 'package1' in os.listdir(tempdir)
    True
    >>> 'package1-0.1.tar.gz' in os.listdir(os.path.join(tempdir, 'package1'))
    True
    >>> import shutil
    >>> shutil.rmtree(tempdir)  # Cleanup.
