.. oopnet documentation master file, created by
   sphinx-quickstart on Fri Oct 23 09:55:09 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

======
OOPNET
======

Object-oriented EPANET in Python

By David B. Steffelbauer

Latest tagged version: v0.0.1

.. warning::
    Be warned, that OOPNET is still changing a lot. Until it's marked as 1.0, you should assume that it is unstable
    and act accordingly.

----------
Objectives
----------

The purpose of OOPNET is to provide an easy-to-use programming interface of EPANET to students, researchers and
scientists who are not blessed with sophisticated programming skills.
It should enable people to easily prototype Python code for different water distribution related tasks.
Now it is in an alpha stage, meanaing that it is nothing more as a wrapper around EPANET's command line interface
that is able to manipulate EPANET .inp files, run a EPANET simulation through the command line interface and parse
the information contained in the .rpt file.

Although it is a little bit more, as you will see reading this documentation, since OOPNET

* is object-oriented
* has multi-dimensional xray support for simulation reports
* is easy to run in parallel
* makes beautiful, paper ready plots


The vision of oopnet is to build an open-source community around it, connect programmers and wanna-be programmers in
the water distribution related community and build a stand-alone hydraulic solver resulting in a totally in Python
written water distribution system software making it nice and shiny from the same mould.

---------
Contents:
---------


.. toctree::
    :maxdepth: 2

    intro
    download
    installation
    tutorial
    examples
    api
    elements

.. Packages <packages/modules>

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
