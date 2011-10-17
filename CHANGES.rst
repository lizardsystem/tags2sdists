Changelog of tags2sdists
===================================================


0.5 (2011-10-17)
----------------

- Fix for faulty setup.py's in checkout directories. An error in there would
  generate a directory named ``Traceback\ (most\ recent\ call\ last):`` in the
  sdist directory...


0.4 (2011-10-12)
----------------

- Internally, the directories passed on the commandline are made
  absolute. Necessary as there's quite some ``os.chdir()`` going around.


0.3 (2011-10-12)
----------------

- Added documentation.

- Renamed script from make_sdists to tags2sdists.


0.2 (2011-10-11)
----------------

- Added script that combines the sdist tarball creation with the target
  directory parsing and that generates all the necessary tarballs.

- Added creation (via zest.releaser) of a single sdist tarball.


0.1 (2011-10-10)
----------------

- Added parsing of a target directory with sdists.

- Initial library skeleton created by nensskel.
