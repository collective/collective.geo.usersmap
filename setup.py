from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='collective.geo.usersmap',
      version=version,
      description="Collective Geo Users' map",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering :: GIS",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.geo'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.geo.bundle',
      ],
      extras_require={
        'tests': [
            'lxml',
            'plone.app.testing',
        ],
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
