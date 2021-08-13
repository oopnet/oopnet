==========
Installing
==========

Before installing OOPNET, you need to have `setuptools <http://pythonhosted.org/setuptools/>`_ installed.

Installing with pip
-------------------

.. note::
    the ``gitlab.com`` repository is available for members of the private repository. But guests can be
    invited as well. Just write me a Mail (david.steffelbauer@tugraz.at)

Try to install it with

::

    pip install --upgrade git+https://gitlab.com/steffel/oopnet.git

On Windows OOPNET includes in the delivery an EPANET executable (``epanet2d.exe``). If you are using OOPNET on Linux or
Unix Systems (Mac OSX) make sure that EPANET is working in the command line as ``epanet2`` e.g:

::

    epanet2 path-to-inputfile/inputfile.inp path-to-reportfile/reportfile.rpt


Installing from source
----------------------

.. warning::

    GitHub repository is not generated yet. The following lines are just a placeholder for the time when the GitHub
    project is finished

You can install from source by downloading a source archive file (tar.gz or zip) or by checking out the source files
from the Git source code repository.

OOPNET is till now a pure Python package, therefor there is no need for a compiler.

Source archive files
^^^^^^^^^^^^^^^^^^^^

    1. Download the source from ...
    2. Unpack and change the directory to the source directory (it should have the files README.md and setup.py)
    3. Run ``python setup.py install`` to build and install


Requirements
------------

Python
^^^^^^

To use OOPNET you need Python 2.7 .

The easiest way to get Python and most optional packages is to install the "`Anaconda <https://www.continuum
.io/why-anaconda>`_" Python distribution from Continuum Analytics.

Alternatively, you can also install the Enthought python distibution "`Canopy <https://www.enthought
.com/products/canopy/>`_".

.. note::

    Make sure to install Python 2.7 and not Pyhton 3 since OOPNET is currently only working under Python 2.7. It is
    planned in the near future to port the code to Python 3.


traits
^^^^^^

explicitly typed attributes for Python
(https://pypi.python.org/pypi/traits)

Traits is used for the object-oriented programming in OOPNET.

Install ``traits`` simply with ``pip``

::

    pip install traits

or Anaconda

::

    conda install traits

xray
^^^^

N-D labeled arrays and datasets in Python (http://xray.readthedocs.org/en/stable/)

.. note::
    xray requires ``numpy 1.7`` or later and ``pandas 0.15.0`` or later!

matplotlib
^^^^^^^^^^

Python plotting package (http://matplotlib.org)

networkx
^^^^^^^^

Python package for creating and manipulating graphs and networks (https://networkx.github.io)

Bokeh
^^^^^

Statistical and novel interactive HTML plots for Python (http://bokeh.pydata.org/en/latest/)

-----------------
Optional Packages
-----------------

Deap
^^^^

Distributed Evolutionary Algorithms in Python (http://deap.readthedocs.org/en/master/)

Scoop
^^^^^

Scalable COncurrent Operations in Python (http://scoop.readthedocs.org/en/0.7/)

.. warning::
    Experiments on our institute have shown that ``scoop`` is not the best or most stablest packeage for
    multiprocessing. Use Python's ``multiprocessing`` instead.
