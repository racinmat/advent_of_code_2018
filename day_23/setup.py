from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("things.pyx")
)
# build it by python setup.py build_ext --inplace