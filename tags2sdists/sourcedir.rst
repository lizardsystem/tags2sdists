Sourcedir deals with the directory with sources of which we need to make
distributions.

SourceBaseDir just gives us a list of directories to investigate for tags.
(Note that the test package dir isn't a sources dir, but it is enough for
testing the SourceBaseDir):

    >>> import pkg_resources
    >>> testdir = pkg_resources.resource_filename(
    ...     'tags2sdists', 'testpackagedir')
    >>> from tags2sdists import sourcedir
    >>> source_base_dir = sourcedir.SourceBaseDir(testdir)
    >>> dirs = source_base_dir.source_dirs()
    >>> len(dirs)
    2

The directories are absolute paths:

    >>> import os
    >>> os.path.join(testdir, 'package1') == dirs[0]
    True
