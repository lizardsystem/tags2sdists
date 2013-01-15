from setuptools import setup

version = '1.0'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'pkginfo',
    'setuptools',
    'zest.releaser',
    ],

tests_require = [
    ]

setup(name='tags2sdists',
      version=version,
      description="Create python sdists from tags",
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[],
      keywords=[],
      author='Reinout van Rees',
      author_email='reinout@vanrees.org',
      url='https://github.com/lizardsystem/tags2sdists/',
      license='GPL',
      packages=['tags2sdists'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require = {'test': tests_require},
      entry_points={
          'console_scripts': [
              'tags2sdists = tags2sdists.script:main',
          ]},
      )
