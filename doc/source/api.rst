===
API
===

-------------------
Read, Write and Run
-------------------

.. autofunction:: oopnet.api.Read
.. autofunction:: oopnet.api.Write
.. autofunction:: oopnet.api.Run

------------------
Plotting functions
------------------

.. autofunction:: oopnet.api.Plot
.. autofunction:: oopnet.api.Show
.. autofunction:: oopnet.api.BPlot

----------------
Report functions
----------------

^^^^^^^^^^^^
Node reports
^^^^^^^^^^^^

.. autofunction:: oopnet.api.Elevation
.. autofunction:: oopnet.api.Demand
.. autofunction:: oopnet.api.Head
.. autofunction:: oopnet.api.Pressure
.. autofunction:: oopnet.api.Quality
.. autofunction:: oopnet.api.Nodeinfo


^^^^^^^^^^^^
Link reports
^^^^^^^^^^^^

.. autofunction:: oopnet.api.Flow
.. autofunction:: oopnet.api.Velocity
.. autofunction:: oopnet.api.Headloss
.. autofunction:: oopnet.api.Reaction
.. autofunction:: oopnet.api.FFactor
.. autofunction:: oopnet.api.Length
.. autofunction:: oopnet.api.Diameter
.. autofunction:: oopnet.api.Position
.. autofunction:: oopnet.api.Setting
.. autofunction:: oopnet.api.Linkinfo

------------------------
Element getter functions
------------------------

^^^^^^^^^^^^^^^^^^^^^^^^^^^
Get single elements by name
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: oopnet.utils.getters.get_by_id.get_junction
.. autofunction:: oopnet.utils.getters.get_by_id.get_tank
.. autofunction:: oopnet.utils.getters.get_by_id.get_reservoir
.. autofunction:: oopnet.utils.getters.get_by_id.get_node

.. autofunction:: oopnet.utils.getters.get_by_id.get_pipe
.. autofunction:: oopnet.utils.getters.get_by_id.get_pump
.. autofunction:: oopnet.utils.getters.get_by_id.get_valve
.. autofunction:: oopnet.utils.getters.get_by_id.get_link

.. autofunction:: oopnet.utils.getters.get_by_id.get_curve
.. autofunction:: oopnet.utils.getters.get_by_id.get_pattern
.. autofunction:: oopnet.utils.getters.get_by_id.get_rule

^^^^^^^^^^^^^^^^^^^^^^
Retrieve element lists
^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: oopnet.utils.getters.element_lists.get_junction_ids
.. autofunction:: oopnet.utils.getters.element_lists.get_tank_ids
.. autofunction:: oopnet.utils.getters.element_lists.get_reservoir_ids
.. autofunction:: oopnet.utils.getters.element_lists.get_node_ids
.. autofunction:: oopnet.utils.getters.element_lists.get_pipe_ids
.. autofunction:: oopnet.utils.getters.element_lists.get_pump_ids
.. autofunction:: oopnet.utils.getters.element_lists.get_valve_ids
.. autofunction:: oopnet.utils.getters.element_lists.get_link_ids

.. autofunction:: oopnet.utils.getters.element_lists.get_nodes
.. autofunction:: oopnet.utils.getters.element_lists.get_links

^^^^^^^^^^^^^^^
Special getters
^^^^^^^^^^^^^^^

.. autofunction:: oopnet.utils.getters.special_getters.getsourcelist

-----
Utils
-----

.. autofunction:: oopnet.api.Copy
.. autofunction:: oopnet.api.tic
.. autofunction:: oopnet.api.toc
.. autofunction:: oopnet.api.make_measurement


^^^^^^^^^^^^^^^^
Adding functions
^^^^^^^^^^^^^^^^
For the parameters of the following functions the documentation of the following Network Components applies as well: :ref:`Node <node>`, :ref:`Tank <tank>`, :ref:`Reservoir <reservoir>`, :ref:`Pipe <pipe>`, :ref:`Pump <pump>` and :ref:`Valve <valve>`.

.. autofunction:: oopnet.utils.adders.add_element.add_junction
.. autofunction:: oopnet.utils.adders.add_element.add_tank
.. autofunction:: oopnet.utils.adders.add_element.add_reservoir
.. autofunction:: oopnet.utils.adders.add_element.add_pipe
.. autofunction:: oopnet.utils.adders.add_element.add_pump
.. autofunction:: oopnet.utils.adders.add_element.add_valve

^^^^^^^^^^^^^^^^^^
Removing functions
^^^^^^^^^^^^^^^^^^

.. autofunction:: oopnet.utils.removers.remove_element.remove_junction
.. autofunction:: oopnet.utils.removers.remove_element.remove_tank
.. autofunction:: oopnet.utils.removers.remove_element.remove_reservoir
.. autofunction:: oopnet.utils.removers.remove_element.remove_pipe
.. autofunction:: oopnet.utils.removers.remove_element.remove_pump
.. autofunction:: oopnet.utils.removers.remove_element.remove_valve

-----
Graph
-----

.. autoclass:: oopnet.graph.Graph
.. autoclass:: oopnet.graph.DiGraph
.. autoclass:: oopnet.graph.MultiGraph

----------------------------
Shortcuts for other packages
----------------------------

* sns - `Seaborn <http://stanford.edu/~mwaskom/software/seaborn/>`__ package for statistical data visualization. Actually this is used because it makes matplotlib plots more beautiful.

* os - `os <https://docs.python.org/2/library/os.html>`_: Miscellaneous operating system interfaces from Python's standard library

* nx - `NetworkX <https://networkx.github.io>`_: High-productivity software for complex networks, used for graph theoretic stuff in OOPNET

* np - `NumPy <http://www.numpy.org>`_: NumPy is the fundamental package for scientific computing with Python

* pd - `Pandas <http://pandas.pydata.org>`_: library providing high-performance, easy-to-ise data structures and data analysis tools for Python

* plt - `matplotlib.pyplot <http://matplotlib.org/api/pyplot_api.html>`_: Provides a MATLAB-like plotting framework.

* datetime, timedelta - `datetime.datetime and datetime.timedelta <https://docs.python.org/2/library/datetime.html>`_: objects of Python's standard library package datetime for basic date and time types