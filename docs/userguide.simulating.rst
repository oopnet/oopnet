Network Simulation
==================

OOPNET's network objects come with a simulation method :meth:`~oopnet.elements.network.Network.run` that returns a
:class:`~oopnet.report.report.SimulationReport` object. This report object contains all simulation results as well as
any errors raised by EPANET during the simulation. We will do both a steady state and a extended period simulation
and take a look at handling simulations errors.

Steady State Analysis
---------------------

For demonstrating a steady state analysis, we will once more use the Poulakis model:

.. literalinclude:: /../examples/userguide_simulating.py
    :language: python
    :lines: 1, 3-6

Let's run a simulation and look at the node and link results which are stored as :class:`xarray.DataArray` objects:

.. literalinclude:: /../examples/userguide_simulating.py
    :language: python
    :lines: 8-9

::

    <xarray.DataArray (id: 31, vars: 4)>
    array([[    0.   ,    50.   ,    48.08 ,    48.076],
           [    0.   ,    50.   ,    36.26 ,    36.263],
           ...
           [    0.   ,    50.   ,     7.95 ,     7.952],
           [   52.   , -1500.   ,    52.   ,    -0.   ]])
    Coordinates:
      * id       (id) object 'J-02' 'J-03' 'J-04' 'J-05' ... 'J-30' 'J-31' 'J-01'
      * vars     (vars) object 'Elevation' 'Demand' 'Head' 'Pressure'

.. literalinclude:: /../examples/userguide_simulating.py
    :language: python
    :lines: 10

::

    <xarray.DataArray (id: 50, vars: 8)>
    array([[1.00000e+02, 6.00000e+02, 1.50000e+03, 5.31000e+00, 3.92400e+01,
            0.00000e+00, 0.00000e+00, 2.00000e-02],
           [1.00000e+03, 6.00000e+02, 8.18758e+02, 2.90000e+00, 1.18100e+01,
            0.00000e+00, 0.00000e+00, 2.00000e-02],
           ...

           [1.00000e+03, 3.00000e+02, 5.12740e+01, 7.30000e-01, 1.84000e+00,
            0.00000e+00, 0.00000e+00, 2.00000e-02],
           [1.00000e+03, 3.00000e+02, 2.68080e+01, 3.80000e-01, 5.30000e-01,
            0.00000e+00, 0.00000e+00, 2.00000e-02]])
    Coordinates:
      * id       (id) object 'P-01' 'P-02' 'P-03' 'P-04' ... 'P-48' 'P-49' 'P-50'
      * vars     (vars) object 'Length' 'Diameter' 'Flow' ... 'Reaction' 'F-Factor'

There is another way of accessing the results, that is based on the data analysis and manipulation library
:mod:`pandas`. You can get the simulation results as :class:`pandas.Series` objects (for steady state analysis) or
:class:`pandas.DataFrame` (for extended period simulations) by accessing the different attributes of the simulation report.

For instance, we can get the pressure data from the simulation report like this:

.. literalinclude:: /../examples/userguide_simulating.py
    :language: python
    :lines: 12-13

::

    id
    J-01    -0.000
    J-02    48.076
    ...
    J-30     8.481
    J-31     7.952
    Name: Pressure (m), dtype: float64

The nice thing about pandas is, that it already comes with a lot of useful features. Here, we get some basic statistical
data from the pressure results:

.. literalinclude:: /../examples/userguide_simulating.py
    :language: python
    :lines: 14

::

    count    31.000000
    mean     20.189516
    std      10.322198
    min      -0.000000
    25%      12.222000
    50%      17.344000
    75%      26.360500
    max      48.076000
    Name: Pressure (m), dtype: float64

Extended Period Simulations
---------------------------

We will use another model for this example. Let's read the "Micropolis" model and check the simulation duration and the
reporting time step:

.. literalinclude:: /../examples/userguide_simulating.py
    :language: python
    :lines: 16-19

::

    10 days, 0:00:00
    1:00:00

Right now, the simulation duration is 10 days and we get a result in the report for every hour. Let's change the
simulation duration to one day and the reporting time step to 10 minutes. For this, we use :class:`datetime.timedelta`:

.. literalinclude:: /../examples/userguide_simulating.py
    :language: python
    :lines: 2, 21-22

Next, we will display the node and link results:

.. literalinclude:: /../examples/userguide_simulating.py
    :language: python
    :lines: 24-25

::

    <xarray.DataArray (time: 145, id: 1577, vars: 4)>
    array([[[ 3.1577e+02,  0.0000e+00,  3.5171e+02,  3.5940e+01],
            [ 3.1577e+02,  2.1000e-01,  3.5171e+02,  3.5940e+01],
            [ 3.1638e+02,  0.0000e+00,  3.5152e+02,  3.5140e+01],
            ...
            [ 2.8346e+02, -3.0510e+01,  2.8346e+02,  0.0000e+00],
            [ 3.1394e+02,  0.0000e+00,  3.1394e+02,  0.0000e+00],
            [ 3.1699e+02, -5.4430e+01,  3.4643e+02,  2.9440e+01]]])
    Coordinates:
      * id       (id) object 'IN0' 'TN1' 'IN2' ... 'Aquifer' 'SurfaceResrvr' 'Tank'
      * vars     (vars) object 'Elevation' 'Demand' 'Head' 'Pressure'
      * time     (time) datetime64[ns] 2016-01-01 ... 2016-01-01T09:50:00


.. literalinclude:: /../examples/userguide_simulating.py
    :language: python
    :lines: 26

::

    <xarray.DataArray (time: 145, id: 1619, vars: 8)>
    array([[[4.635e+01, 1.016e+02, 2.100e-01, ..., 0.000e+00, 0.000e+00,
             3.000e-02],
            [2.879e+01, 1.016e+02, 3.000e-01, ..., 0.000e+00, 0.000e+00,
             5.000e-02],
            [2.285e+01, 1.016e+02, 3.000e-02, ..., 0.000e+00, 0.000e+00,
             2.000e-01],
            ...
            [0.000e+00, 1.200e+01, 1.300e-01, ..., 0.000e+00, 0.000e+00,
             0.000e+00],
            [0.000e+00, 1.200e+01, 3.600e-01, ..., 0.000e+00, 0.000e+00,
             0.000e+00],
            [0.000e+00, 1.200e+01, 1.440e+00, ..., 0.000e+00, 0.000e+00,
             0.000e+00]]])
    Coordinates:
      * id       (id) object 'SC0' 'SC1' 'SC2' 'SC3' ... 'V201' 'V202' 'V1028'
      * vars     (vars) object 'Length' 'Diameter' 'Flow' ... 'Reaction' 'F-Factor'
      * time     (time) datetime64[ns] 2016-01-01 ... 2016-01-01T09:50:00

As you can see, the DataArrays now have a new dimension ``time``.

If we access the pressure property of the simulation result, we now get a :class:`pandas.DataFrame`:

.. literalinclude:: /../examples/userguide_simulating.py
    :language: python
    :lines: 28-29

::

        id                      IN0     TN1     IN2  ...  Aquifer  SurfaceResrvr   Tank
    time                                         ...
    2016-01-01 00:00:00   35.94   35.94   35.14  ...      0.0            0.0  35.05
    2016-01-01 00:10:00   35.91   35.91   35.11  ...      0.0            0.0  35.03
    2016-01-01 00:20:00   35.88   35.88   35.09  ...      0.0            0.0  35.00
    2016-01-01 00:30:00   35.86   35.86   35.06  ...      0.0            0.0  34.97
    2016-01-01 00:40:00   35.83   35.83   35.03  ...      0.0            0.0  34.95
    ...                     ...     ...     ...  ...      ...            ...    ...
    2016-01-01 23:20:00 -290.15 -290.15 -290.90  ...      0.0            0.0  27.43
    2016-01-01 23:30:00 -290.15 -290.15 -290.90  ...      0.0            0.0  27.43
    2016-01-01 23:40:00 -290.15 -290.15 -290.90  ...      0.0            0.0  27.43
    2016-01-01 23:50:00 -290.15 -290.15 -290.90  ...      0.0            0.0  27.43
    2016-01-02 00:00:00 -205.97 -205.97 -206.71  ...      0.0            0.0  27.43

    [145 rows x 1577 columns]

Handling errors
---------------

Now we will take a look at handling simulation errors. We will again use the Poulakis model for this.
To cause an error, we will add a Junction without connecting it to the rest of the model. This will lead to an error during the
simulation.

.. literalinclude:: /../examples/error_handling.py
	:language: python
	:lines: 9

If we were to run the simulation now, an :class:`~oopnet.simulator.simulation_errors.EPANETSimulationError` would be raised by OOPNET.
These exceptions act as containers for all the errors raised by EPANET. To catch those exceptions, we can use a try-except clause:

.. literalinclude:: /../examples/error_handling.py
	:language: python
	:lines: 11-14

We first try to simulate the model and wait for the exception. When it is caught, we can print it, which results in this::

	[UnconnectedNodeError('Error 233 - Error  Error 200: one or more errors in input file'), InputDataError('Error 200 - one or more errors in input file')]

Since an :class:`~oopnet.simulator.simulation_errors.EPANETSimulationError` is a container, we can check for specific
errors using :meth:`~oopnet.simulator.simulation_errors.EPANETSimulationError.check:_contained_errors`. You can check either be providing
a single Exception class

.. literalinclude:: /../examples/error_handling.py
	:language: python
	:lines: 16-19

or using a list of Exception classes:

.. literalinclude:: /../examples/error_handling.py
	:language: python
	:lines: 20-21

If EPANET provides a more detailed error description (e.g., if a value in the model is invalid, EPANET tells us which part
is faulty), OOPNET also outputs these details.

Let's test this by rereading the model and setting a Pipe's diameter to a negative value:

.. literalinclude:: /../examples/error_handling.py
	:language: python
	:lines: 23-33

Here, outputting ``e`` results in this::

	[IllegalLinkPropertyError('Error 211 - illegal link property value -100.0 in [PIPES] section: P-01 J-01 J-02 -100.0 600.0 0.26 0.0'), InputDataError('Error 200 - one or more errors in input file')]

Further Examples
----------------

.. toctree::
   :maxdepth: 1

   examples.extended_period_simulation.rst
   examples.mc_make_some_noise.rst
   examples.mc_stereo.rst


Summary
-------

Simulation Example
~~~~~~~~~~~~~~~~~~

.. literalinclude:: /../examples/userguide_simulating.py
	:language: python

Error Handling Example
~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: /../examples/error_handling.py
	:language: python