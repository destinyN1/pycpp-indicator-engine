from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import setuptools
import pybind11

class get_pybind_include:
    def __str__(self):
        return pybind11.get_include()

ext_modules = [
    Extension(
        'indicator_engine',
        ['bindings.cpp', 'indicator_engine.cpp'],
        include_dirs=[
            get_pybind_include(),
        ],
        language='c++',
        extra_compile_args=['-std=c++11'],
    ),
]

setup(
    name='indicator_engine',
    version='1.0.0',
    author='Your Name',
    description='C++ Indicator Engine for Python',
    ext_modules=ext_modules,
    install_requires=['pybind11>=2.6.0'],
    cmdclass={'build_ext': build_ext},
    zip_safe=False,
)
