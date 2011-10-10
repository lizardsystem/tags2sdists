Packagedir wraps a directory with source distributions.

    >>> from tags2sdists import packagedir
    >>> package_dir = packagedir.PackageDir(None)
    >>> package_dir.packages
    defaultdict(<type 'list'>, {})

    >>> import pkg_resources
    >>> testdir = pkg_resources.resource_filename(
    ...     'tags2sdists', 'testpackagedir')
    >>> package_dir = packagedir.PackageDir(testdir)
    >>> package_dir.parse()
    >>> sorted(package_dir.packages.keys())
    ['package1', 'package2']
    >>> sorted(package_dir.packages['package1'])
    ['0.1', '0.2']
