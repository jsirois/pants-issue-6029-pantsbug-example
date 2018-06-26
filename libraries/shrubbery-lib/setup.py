import os
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

sources = [os.path.join(os.path.dirname(__file__), 'shrubbery.pyx')]
ext_modules = cythonize([Extension("shrubberylib", sources=sources, libraries=[], language='c++')])
setup(name='Shrubbery Lib', ext_modules=ext_modules)
