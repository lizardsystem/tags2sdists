tags2sdists
===========

Tags2sdists creates python sdists from tags into a structure that can serve as
a company-internal pypi (python package index).


Basic operation
---------------

Tags2sdists looks at two directories:

- A source directory ("CHECKOUTDIR") with checkouts. Every checkout (svn trunk
  checkout, git/hg clone) is examined for tags according to that version
  control system.

- A target directory ("SDISTDIR") where per-package directories are made with
  sdists named like ``PACKAGENAME-1.2.tar.gz`` in it.

Those two directories are kept in sync by checking for packages/tags that are
available in the version control system but that are missing in the target
directory. If missing, an "sdist" (.tar.gz source distribution) is generated
and placed in the target directory.


Usage
-----

Tags2sdists provides the ``tags2sdists`` command::

    Usage: tags2sdists CHECKOUTDIR SDISTDIR
        CHECKOUTDIR: directory with checkouts
        SDISTDIR: directory with sdist package directories

    Options:
      -h, --help     show this help message and exit
      -v, --verbose  Show debug output
      -q, --quiet    Show minimal output


Setup
-----

Installing tags2sdists itself is as simple as ``pip install tags2sdists`` or
``easy_install tags2sdists`` or including it in your buildout in the regular
manner.

Next you need the CHECKOUTDIR and SDISTDIR directories.

**CHECKOUTDIR**: you need a directory with checkouts. So doing it by hand is
fine. But when you use svn, a directory with ``svn:externals`` is probably
handiest. For everything else (and also for svn), `checkoutmanager
<http://pypi.python.org/pypi/checkoutmanager>`_ is the thing I'd use. Make a
config file (``checkoutmanager.cfg``) looking like this::

    [internalprojects]
    vcs = git
    basedir = /srv/packages/var/checkouts/
    checkouts =
        git@github.com:lizardsystem/nensskel.git
        git@github.com:lizardsystem/lizard-ui.git
        git@github.com:lizardsystem/tags2sdists.git

And set up a cron job that runs ``checkoutmanager
--configfile=YOURCONFIGFILE``, it'll update the checkouts in the base dir you
configured. (In that same cronjob, fire up ``tags2sdists`` afterwards).

**SDISTDIR**: just a directory somewhere will do. You'll get a pypi-like
directory structure in there.

A structure like generated with tags2sdists is a perfect index for
easy_install and buildout if you let apache host it.  Only problem: you can
only have one index (note: pip apparently supports multiple indexes).  You can
solve this problem by having apache redirect you to pypi when something is not
found.

Here's an example apache config snippet::

  # Allow indexing
  Options +Indexes
  IndexOptions FancyIndexing VersionSort

  # Start of rewriterules to use our own var/private/* packages
  # when available and to redirect to pypi if not.
  RewriteEngine On
  # Use our robots.txt:
  RewriteRule ^/robots.txt - [L]
  # Use our apache's icons:
  RewriteRule ^/icons/.* - [L]
  # We want OUR index.  Specified in a weird way as apache
  # searches in a weird way for index.htm index.html index.php etc.
  RewriteRule ^/index\..* - [L]

  # Use our var/private/PROJECTNAME if available,
  # redirect to pypi otherwise:
  RewriteCond /path/on/server/var/private/$1 !-f
  RewriteCond /path/on/server/var/private/$1 !-d
  RewriteRule ^/([^/]+)/?$ http://pypi.python.org/pypi/$1/ [P,L]

  # Use our var/private/PROJECTNAME/project-0.1.tar.gz if available,
  # redirect to pypi otherwise:
  RewriteCond /path/on/server/var/private/$1 !-d
  RewriteRule ^/([^/]+)/([^/]+)$ http://pypi.python.org/pypi/$1/$2 [P,L]


Using the apache-served index
-----------------------------

You can use such a custom apache-served index in two ways.  Easy_install has a
``-i`` option for passing along an index::

    $> easy_install -i http://packages.my.server/ zest.releaser

In buildout, you can set it like this::

    [buildout]
    index = http://packages.my.server/
    parts =
        ...


Development
-----------

- The source code is on https://github.com/lizardsystem/tags2sdists/ .

- Bugs can be reported on https://github.com/lizardsystem/tags2sdists/issues .

