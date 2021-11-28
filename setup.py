from setuptools import setup, find_packages

# todo: check entries
setup(
    name='oopnet',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/steffelbauer/oopnet',
    license='',
    author='David B. Steffelbauer',
    author_email='david.steffelbauer@tugraz.at',
    description='Object-oriented EPANET in Python',
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'Topic :: Water Distribution System Analysis :: Open Source EPANET',
                 'Programming Language :: Python :: 3.9'],
    package_data={'': ['*.exe']},
    include_package_data=True,
    install_requires=[],
    python_requires='>3.9'
)
