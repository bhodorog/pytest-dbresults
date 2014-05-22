import os
from setuptools import setup, find_packages


README = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md')


DEPENDENCIES = [
    'pytest',
    'sqlalchemy',
]


setup(
    name='pytest-dbresults',
    version='0.1',
    description='Plugin for pytest. Store into a DB the results of tests'
    'executed by pytest organized by sessions',
    long_description=open(README, 'r').read(),
    author='Bogdan Hodorog',
    author_email='bogdan.hodorog@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=DEPENDENCIES,
    setup_requires=[],
    classifiers=[],
    entry_points={
        'pytest11': [
            'dbresults = dbresults.plugin'
        ]
    },
)
