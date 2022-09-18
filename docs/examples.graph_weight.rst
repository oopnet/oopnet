-----------------------
Different Graph Weights
-----------------------

In this example, we will discuss how to specify different weights for edges, when creating a Graph from an OOPNET network.

First, we import :mod:`os`, :mod:`networkx` and :mod:`oopnet`.

.. literalinclude:: /../examples/graph_weight.py
	:language: python
	:lines: 1-7

We will use the "Anytown" model in this example, so we read it:

.. literalinclude:: /../examples/graph_weight.py
	:language: python
	:lines: 9-10

When we create a :class:`networkx.Graph` (or :class:`networkx.DiGraph`, :class:`networkx.MultiGraph` or :class:`networkx.MultiDiGraph`) object using the corresponding factories in :mod:`oopnet.graph`, the pipe lengths are used as
weights in the graph. We will use Dijkstra's shortest path to compare the different graphs.

.. literalinclude:: /../examples/graph_weight.py
	:language: python
	:lines: 10-12

::

    Average Shortest Path: 3494.6983087192225

You can specify a different weight, by passing a ``weight`` argument. You can specify any Link attribute you want (e.g. ``roughness``). If a link doesn't have the attribute, a default value is used ``0.00001``).

.. literalinclude:: /../examples/graph_weight.py
	:language: python
	:lines: 14-16

::

    Average Shortest Path: 6363.355196667406

You can specify a different default value, if you want to:

.. literalinclude:: /../examples/graph_weight.py
	:language: python
	:lines: 18-20

::

    Average Shortest Path: 6363.355182198411

+++++++
Summary
+++++++

.. literalinclude:: /../examples/graph_weight.py
	:language: python
