import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-ag-survey',
    version='2.0',
    packages=find_packages(),
    include_package_data=True,
    license='Copyright (C) Atlantic Geomatics, UK',  # example license
    description='ag-survey is an app to do CRUD operations for surveys',
    long_description=README,
    # url='http://www.example.com/',
    author='Peter S',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: Copyright (C) Atlantic Geomatics, UK', # example license
        'Operating System :: OS Independent',
        # 'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
