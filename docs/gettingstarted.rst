===============
Getting started
===============

------------
Installation
------------

OOPNET used features only available in the newer Python version, which is why Python >= 3.9 is needed along with
several Python package dependencies.

.. note::
   If your are using Linux, EPANET has to be available in you command line interface.

   To test, if EPANET is available, open a terminal and run:

   .. code-block:: bash

      epanet

OOPNET is available on PyPI and can be easily installed together with its dependencies using `pip`:


.. code-block:: bash

   pip install oopnet

Alternatively, you can install OOPNET from its repository:

.. code-block:: bash

   pip install git+https://github.com/oopnet/oopnet.git

-----------
Basic Usage
-----------

To use OOPNET, you first have to import it in your script:

.. code-block:: python

   import oopnet as on

In OOPNET, everything is about the `Network`. If you want to start with a new, empty Network, type the following:

.. code-block:: python

   network = on.Network()


If you want to read an existing EPANET model, you can `read` it as an input-file:

.. code-block:: python

   filename = "network.inp"
   network = on.Network.read(filename)

To simulate the model, you can use the Network`s `run` method:

.. code-block:: python

   report = network.run()

If you want to create a basic Network plot, you can use its `plot` method:

.. code-block::

   network.plot()