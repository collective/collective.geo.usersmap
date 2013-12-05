from setuptools import setup, find_packages
import os

version = '1.0'

setup(
    name='collective.geo.usersmap',
    version=version,
    description="Collective Geo Users' map",
    long_description=(
        open("README.rst").read() + "\n" +
        open(os.path.join("docs", "HISTORY.txt")).read()
    ),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='collective plone package geo-reference users map',
    author='Giorgio Borelli',
    author_email='giorgio@giorgioborelli.it',
    url='https://github.com/collective/collective.geo.usersmap.git',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective', 'collective.geo'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'geopy>=0.96.2',
        'collective.geo.bundle',
        'collective.geo.mapwidget > 1.6'
    ],
    extras_require={
        'test': [
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
