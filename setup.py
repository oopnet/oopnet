from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

# todo: check entries; move parts to setup.cfg?
setup(
    name='oopnet',
    version='0.0.1',
    packages=find_packages(),
    # url='https://github.com/oopnet/oopnet',
    # long_description=README,
    # long_description_content_type='text/markdown',
    license='MIT',
    # author='David B. Steffelbauer',
    # author_email='david.steffelbauer@tugraz.at',
    description='Object-oriented EPANET in Python',
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'Topic :: Scientific/Engineering',
                 'Programming Language :: Python :: 3.9'],
    package_data={'': ['*.exe']},
    install_requires=['numpy', 'pandas', 'xarray'],
    include_package_data=True,
    python_requires='>3.9'
)
