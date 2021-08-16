"""

Documentation: https://jak.readthedocs.io

Copyright 2021 Dispel, LLC

Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""

from setuptools import find_packages, setup
import re
import ast

# 100% stolen from flask to avoid catch 22 issue with importing version
# (can't rely on something that we haven't installed yet)
_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('jak/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


setup(
    name='jak',
    version=version,
    url='https://github.com/dispel/jak',
    license='Apache-2.0',
    author='Dispel, LLC',
    author_email='jak@dispel.io',
    description='jak makes encrypting files really easy',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'click>=6.6',
        'pycryptodome>=3.10.1',
        'six>=1.10.0'
    ],
    entry_points={
        'console_scripts': [
            'jak = jak.app:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        # 'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
