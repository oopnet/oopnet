-------------------
Adders and Removers
-------------------

This example shows you how to add network components like junctions, pipes or pumps to a network and remove them again.

.. note::

	There are adding and removing functions for every network component type (pipes, junctions, valves, tanks, ...). In this example only some of these functions are shown, the remaining functions however all work in the same way.

For the addition and removal of network components only OOPNET has to be imported. The other packages are only imported to show other possibilities how you could work with these functions.

.. literalinclude:: /../../examples/adders_and_removers.py
	:lines: 1-3

For this example the Poulakis network is used, this network is therefore imported.

.. literalinclude:: /../../examples/adders_and_removers.py
	:lines: 5-7

.. image:: fig/adders_and_removers_1.png

To add a new pipe, first a new junction has to be added to the network. Here a new junction is added in the top right corner of the network. The new junction is given an ID, coordinates and a demand. Other values like elevation could also be set but in this example the default values are being used for the other parameters.

.. literalinclude:: /../../examples/adders_and_removers.py
	:lines: 9

Now a new pipe is added to connect the new junction to the network. Again some default values for the parameters are used, some parameters are set manually.

.. literalinclude:: /../../examples/adders_and_removers.py
	:lines: 11

.. image:: fig/adders_and_removers_2.png

Next all pipes connected to the junction ``J-24`` and then the junction itself are removed from the network.

.. literalinclude:: /../../examples/adders_and_removers.py
	:lines: 13-22
	
After that a single pipe is added in the area where the other pipes were just removed.

.. literalinclude:: /../../examples/adders_and_removers.py
	:lines: 24

.. image:: fig/adders_and_removers_3.png
	
Finally, a new reservoir is added to the network and a pump is used to connect it to a nearby junction.

.. literalinclude:: /../../examples/adders_and_removers.py
	:lines: 26-28

.. image:: fig/adders_and_removers_4.png

+++++++
Summary
+++++++

.. literalinclude:: /../../examples/adders_and_removers.py


