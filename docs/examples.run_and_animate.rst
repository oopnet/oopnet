-------------
Run & Animate
-------------

In this example we want to create a matplotlib animation of the model where we plot the flow and pressure results from an
extended period simulation.

For this, we first have to import the packages we require:

- `os` for specifying the path to the EPANET input file
- `matplotlib.pyplot` for creating an animation of a certain size
- `matplotlib.animation.PillowWriter` for writing the animation to a file
- and of course `oopnet` itself

In this example we read a part of the `L-Town` network (Area C) with slight modifications. This model
already comes with included patterns and can be used for extended period simulations.

.. literalinclude:: /../examples/run_and_animate.py
	:language: python
	:lines: 1-9

Then, we can simulate the model with its ``.run()`` method and save the simulation results to the variable ``rpt``.

.. literalinclude:: /../examples/run_and_animate.py
	:language: python
	:lines: 11

If we want to take a closer look at the simulation results, we can access the report's different properties. Since we
want to use the flow and pressure data in the animation, we assign them to variables. We also limit the data to a single
day and take a look at a few data points.

.. literalinclude:: /../examples/run_and_animate.py
	:language: python
	:lines: 13-16

.. :meth:`oopnet.report.report_getter_functions`

Now, we create an animation using the Network's ``.animate()`` method. First, we create matplotlib `Figure` and `Axes`
objects and pass a desired figure size:

.. literalinclude:: /../examples/run_and_animate.py
	:language: python
	:lines: 18

We then pass the ``ax`` object to the ``animate`` method along with the simulation data. We call the flow data's
``.abs()`` method, to use the absolute flow values in the animation. The labels for the node and link color bars have
to be passed as well.
You can also specify how long the interval between the reporting time steps should be. The model uses a reporting time
step of 5 minutes, so we choose an interval of 50 ms. The ``robust`` argument limits the color bar to values between
the 2nd and the 98th percentile of the passed data's value range.

.. literalinclude:: /../examples/run_and_animate.py
	:language: python
	:lines: 19

.. image:: figures/examples/simple_animation.gif

Finally, we can save the animation. Using the ``dpi`` and ``fps`` attributes helps you control the animation quality
and file size:

.. literalinclude:: /../examples/run_and_animate.py
	:language: python
	:lines: 20


+++++++
Summary
+++++++

.. literalinclude:: /../examples/run_and_animate.py
	:language: python
