-------------------
Error Handling
-------------------

This examples discusses handling errors raised by EPANET when simulating a model.

First, let's import the necessary packages and read the Poulakis model.

.. literalinclude:: /../examples/error_handling.py
	:language: python
	:lines: 1-7

Next, we will add a Junction without connecting it to the rest of the model. This will lead to an error during the
simulation.

.. literalinclude:: /../examples/error_handling.py
	:language: python
	:lines: 9

If we were to run the simulation now, an `EPANETSimulationError` would be raised by OOPNET. These exceptions act as
containers for all the errors raised by EPANET. To catch those exceptions, we can use a try-except clause:

.. literalinclude:: /../examples/error_handling.py
	:language: python
	:lines: 11-14

We first try to simulate the model and wait for the exception. When it is caught, we can print it, which results in this::

	[UnconnectedNodeError('Error 233 - Error  Error 200: one or more errors in input file'), InputDataError('Error 200 - one or more errors in input file')]

Since an `EPANETSimulationError` is also a container, we can check for specific errors. You can check either be providing
a single Exception class

.. literalinclude:: /../examples/error_handling.py
	:language: python
	:lines: 16-19

or using a list of Exception classes:

.. literalinclude:: /../examples/error_handling.py
	:language: python
	:lines: 20-21

If EPANET provides a more detailed error description (e.g., for invalid inputs in the model, EPANET tells us which part
is faulty), OOPNET also outputs these details.

Let's test this by rereading the model and setting a Pipe's diameter to a negative value:

.. literalinclude:: /../examples/error_handling.py
	:language: python
	:lines: 23-33

Here, outputting `e` results in this::

	[IllegalLinkPropertyError('Error 211 - illegal link property value -100.0 in [PIPES] section: P-01 J-01 J-02 -100.0 600.0 0.26 0.0'), InputDataError('Error 200 - one or more errors in input file')]


+++++++
Summary
+++++++

.. literalinclude:: /../examples/error_handling.py
	:language: python


