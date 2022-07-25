.. OOPNET documentation master file, created by
   sphinx-quickstart on Tue Jul 26 10:07:02 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

============
Introduction
============

OOPNET (Object-oriented EPANET in Python) is an easy-to-use programming interface of EPANET to
students, researchers and scientists who are not blessed with sophisticated programming skills.
It enables people to easily prototype Python code for different water distribution related tasks.
Right now it is in an alpha stage, meaning that it is nothing more than a wrapper around EPANET's command line interface
that is able to manipulate EPANET .inp files, run a EPANET simulation through the command line interface and parse
the information contained in the .rpt and .bin files.

Although it is a little bit more, as you will see reading this documentation, since OOPNET

* is object-oriented
* has multi-dimensional xray support for simulation reports
* is easy to run in parallel
* makes beautiful, paper ready plots

The vision of OOPNET is to build an open-source community around it, connect programmers and wanna-be programmers in
the water distribution related community and build a stand-alone hydraulic solver resulting in a totally in Python
written water distribution system software making it nice and shiny from the same mould.

.. warning::
    Be warned, that OOPNET is still changing a lot. Until it's marked as 1.0.0, you should assume that it is unstable
    and act accordingly. We are trying to avoid breaking changes but they can and will occur!

-------------
Citing OOPNET
-------------

If you publish something that uses OOPNET, we greatly appreciate a citation of the following reference:

- Steffelbauer, D., Fuchs-Hanusch, D., 2015. OOPNET: an object-oriented EPANET in Python. Procedia Eng. 119, 710e718. https://doi.org/10.1016/j.proeng.2015.08.924.


--------
Contents
--------

.. toctree::
    :maxdepth: 2

    about
    gettingstarted
    userguide
    oopnet
    development

.. Packages <packages/modules>

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
