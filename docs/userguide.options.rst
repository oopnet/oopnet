Options
=======

In this tutorial we will take a look at the different modelling settings that users can modify.

Network objects have several attributes related to settings:

- :attr:`~oopnet.elements.network.Network.options` contains general model settings (e.g., units, headloss formula)
- :attr:`~oopnet.elements.network.Network.times` stores all time related settings (e.g., reporting time step, simulation duration)
- :attr:`~oopnet.elements.network.Network.report` configures general report settings (e.g., whether the simulation report should contain all the nodes)
- :attr:`~oopnet.elements.network.Network.reportparameter` is used to enable or disable the reporting on individual report parameters
- :attr:`~oopnet.elements.network.Network.reportprecision` allows for configuring the precision of the individual report parameters

.. note::
    By default, OOPNET uses SI units and will convert all units in a model to SI units.

We start by importing all required packages and reading a model. We will again use the Poulakis model for demonstration.

.. literalinclude:: /../examples/userguide_settings.py
    :language: python
    :lines: 1-6

We can check what kind of demand model (demand driven or pressure driven) is used in the model:

.. literalinclude:: /../examples/userguide_settings.py
    :language: python
    :lines: 8

::

    DDA

The model we loaded is configured for steady state analysis. We can check this by looking at the :attr:`~oopnet.elements.network.Network.times.duration` setting:

.. literalinclude:: /../examples/userguide_settings.py
    :language: python
    :lines: 9

::

    0:00:00

All times settings have :class:`datetime.timedelta` as type. We will use this later in this guide, to set up an extended
period simulation.

You can also enable or disable the reporting of certain parameters (pressure, flow, length, velocity, headloss etc). Here,
we disable the reporting of the velocity and enable length reporting:

.. literalinclude:: /../examples/userguide_settings.py
    :language: python
    :lines: 11-12

To change the reporting precision of a parameter, you can do something like this:

.. literalinclude:: /../examples/userguide_settings.py
    :language: python
    :lines: 14

Summary
-------

.. literalinclude:: /../examples/userguide_settings.py
	:language: python
