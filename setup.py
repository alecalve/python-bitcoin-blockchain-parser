from setuptools import setup, find_packages
from blockchain_parser import __version__


setup(
    name='blockchain-parser',
    version=__version__,
    packages=find_packages(),
    url='http://p2sh.info/parser',
    author='Antoine Le Calvez',
    author_email='antoine@p2sh.info',
    description='Bitcoin blockchain parser',
    test_suite='blockchain_parser.tests'
)
