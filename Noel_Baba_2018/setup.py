from distutils.core import setup, Extension

module = Extension('santa', sources = ['data.c','pysanta.c'])

setup (name = 'santa',
        version = '1.0',
        description = 'Gezgin Santa Problemi',
        ext_modules = [module])
