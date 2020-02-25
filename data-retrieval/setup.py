from setuptools import setup, Extension

setup(
    setup_requires=[
        # Setuptools 18.0 properly handles Cython extensions.
        'setuptools>=18.0',
        'cython',
    ],
    ext_modules=[
        Extension('package.cython_code1', sources=['package/cython_code1.pyx']),
        Extension('package.cython_code2', sources=['package/cython_code2.pyx']),
    ],
    include_dirs=[numpy.get_include()],
)