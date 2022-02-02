----------------------------------------------
OOPNET in the middle - Centrality calculations
----------------------------------------------

.. note::

    Another graph theoretic example of what you can do together with OOPNET and NetworkX

In this example different centrality calculations are shown. To calculate the matrices, NetworkX is used.

First, the necessary packages are imported, a filename is declared and an OOPNET ``Network`` is created from the EPANET input file.

.. literalinclude:: /../../examples/centrality.py
	:lines: 1-9

Then a ``MultiGraph`` is created based on the Network.

.. literalinclude:: /../../examples/centrality.py
	:lines: 11

Next, a Matplotlib figure is instantiated. This object will hold a subplot for all of the four centralities we will calculate:

.. literalinclude:: /../../examples/centrality.py
	:lines: 13

Now, the metrics are calculated. We pass the previously created ``MultiGraph`` to different NetworkX functions to calculate the metrics. Since we want to plot the centrality values per node, we need a pandas Series to pass it to the OOPNET ``Plot`` function. We change the series' names so that it is correctly shown in the Plot. Then, we create Matplotlib axes objects and plot the network with these axes objects to correctly place them in the plot.

.. literalinclude:: /../../examples/centrality.py
	:lines: 21-37

To create a single plot for a centrality, just omit the axes object creation and don't pass one to the plotting function.

.. literalinclude:: /../../examples/centrality.py
	:lines: 39-42

Finally, show the plots:

.. literalinclude:: /../../examples/centrality.py
	:lines: 44

+++++++
Summary
+++++++

.. literalinclude:: /../../examples/centrality.py

.. image:: fig/centrality1.png

.. image:: fig/centrality2.png