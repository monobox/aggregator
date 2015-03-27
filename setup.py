#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    # TODO: put package requirements here
    'requests',
    'flask',
    'peewee',
]

setup(
    name='monobox-aggregator',
    version='0.1.0',
    description='Monobox Aggregator',
    long_description=readme,
    author='OXullo Intersecans',
    author_email='x@brainrapers.org',
    url='https://github.com/oxullo/monobox-aggregator',
    packages=[
        'monobox_aggregator',
    ],
    package_dir={'monobox-aggregator': 'monobox_aggregator'},
    install_requires=requirements,
    license='GPL',
    zip_safe=False,
    keywords='monobox-aggregator',
    entry_points={
            'console_scripts': [
                    'monobox-as = monobox_aggregator.server:run',
                    'monobox-fetcher = monobox_aggregator.fetcher:run',
            ],
    },
    include_package_data=True,
    package_data={
            '': ['../scdev.key'],
    },
)
