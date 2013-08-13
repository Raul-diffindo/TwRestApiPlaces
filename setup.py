from distutils.core import setup
import os


def get_packages(package):
    """
    Return root package & all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


setup(
    name='twrestapiplaces.py',
    version='0.1',
    packages=get_packages('TwRestApiPlaces'),
    package_data=get_package_data('TwRestApiPlaces'),
    description='Django App for use Twitter Rest API. Search Trends/Places & Tweets',
    author='Raul Gonzalez',
    author_email='raul.gonzalez@diffindo.es',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description='https://github.com/Raul-diffindo/TwRestApiPlaces',
    install_requires=['python-oauth2', 'python-dateutil'],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP'
    ]
)