import os
import re
import setuptools
import sys

py_version = sys.version_info[:2]

_file_content = open(os.path.join(os.path.dirname(__file__), 'dnsaio', 'version.py')).read()

rex = re.compile(r"""version__ = '(.*)'.*__packagename__ = '(.*)'""", re.MULTILINE | re.DOTALL)
VERSION, PACKAGE_NAME = rex.search(_file_content).groups()
description = 'dns implementation using dnspython and asyncio'

requirements = [
    'dnspython3'
]
if (3,2) < py_version < (3, 4):
    requirements.append('asyncio')

setuptools.setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author="Polyconseil dev' team",
    author_email='opensource+dnsaio@polyconseil.fr',
    url='https://github.com/polyconseil/dnsaio',
    description=description,
    long_description=open('README.rst').read(),
    download_url='https://pypi.python.org/pypi/dnsaio',
    packages=[
        'dnsaio',
    ],
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
    ],
    platforms='all',
    license='BSD'
)