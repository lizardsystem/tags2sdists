Changelog of tags2sdists
===================================================


1.4.1 (2019-12-18)
------------------

- Fixed bug in condition from 1.4...


1.4 (2019-12-18)
----------------

- Added --build-all option: don't stop if the latest tag is found, but just
  build all the tags.


1.3 (2019-09-13)
----------------

- Updated setup (pytest, tox, travis-ci integration, etc).

- Made tags2sdists python3 compatible (tox tests 2.7 and 3.7).


1.2 (2015-05-26)
----------------

- Compensating for newer setuptools versions.


1.1 (2013-07-12)
----------------

- New way of searching for missing tags: we leave old
  unneeded/wrong/renamed ones alone.

- Removing tags with 'dev' in their name from the list of missing
  tags.


1.0 (2013-01-15)
----------------

- Fixed the temp dir cleanup: under certain circumstances it left an
  empty directory.


0.7.1 (2011-12-08)
------------------

- Switching back to the correct directory after 0.7's temp dir cleanup.


0.7 (2011-12-08)
----------------

- Added more logging related to 0.6's corner case.

- Cleaning up the temp dir after a run.


0.6 (2011-12-07)
----------------

- Compensating for a corner case where a package was renamed.


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
