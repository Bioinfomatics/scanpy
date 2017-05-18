import sys
from setuptools import setup, find_packages
from distutils.extension import Extension
import numpy
import versioneer

# Pip calls setup.py egg_info to get static dependency information,
# then installs them, and finally it calls setup.py develop/bdist.
# We create a dummy build_ext so egg_info can be called before pip installs Cython
try:
    from Cython.Distutils import build_ext
except ImportError as e:
    from distutils.cmd import Command
    class build_ext(Command):
        extensions = []
        def initialize_options(self): pass
        def finalize_options(self): pass
        def get_source_files(self): return []
        def run(self):
            if 'egg_info' not in sys.argv:
                raise e

with open('requirements.txt') as requirements:
    requires = [l.strip() for l in requirements]

more_requires = []
if sys.version_info[0] == 2:
    more_requires = [
        'configparser',  # named ConfigParser in py2
        'enum34',        # enum module introduced in python 3.4
    ]

setup(
    name='scanpy',
    version=versioneer.get_version(),
    description='Single-Cell Analysis in Python.',
    url='http://github.com/theislab/scanpy',
    author='F. Alexander Wolf, P. Angerer',
    author_email='alex.wolf@helmholtz-muenchen.de',
    license='GPL-3.0',
    entry_points={
        'console_scripts': [
            'scanpy = scanpy.__main__:main',
        ],
    },
    install_requires=requires + more_requires,
    packages=find_packages(exclude=['scripts', 'scripts.*']),
    include_dirs=[numpy.get_include()],
    cmdclass=versioneer.get_cmdclass({'build_ext': build_ext}),
    ext_modules=[
        Extension('scanpy.cython.utils_cy', [
            'scanpy/cython/utils_cy.pyx',
        ]),
    ],
    zip_safe=False,
)
