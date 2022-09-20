# OOPNET
[![PyPI](https://img.shields.io/pypi/v/oopnet.svg)](https://pypi.python.org/pypi/oopnet)
[![OOPNET build](https://github.com/oopnet/oopnet/actions/workflows/build.yml/badge.svg)](https://github.com/oopnet/oopnet/actions/workflows/build.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/oopnet/oopnet/blob/main/LICENSE.md)
[![Documentation Status](https://readthedocs.org/projects/oopnet/badge/?version=latest)](https://oopnet.readthedocs.io/en/latest/?badge=latest)

OOPNET (object-oriented EPANET) is a Python package for modelling and simulating hydraulic water distribution system models based on the modelling software EPANET.

Main functionalities:

-	Reading EPANET input files (.inp)
-	Modifying model components, settings, controls and rules 
-	Simulating models using EPANET with results as pandas data objects
-	Plotting models using matplotlib

A detailed documentation is available under https://oopnet.readthedocs.io.

---
**Warning!**

Be warned, that OOPNET is still changing a lot. Until it's marked as 1.0.0, you should assume that it is unstable and act accordingly. We are trying to avoid breaking changes but they can and will occur!

---

## Installation

OOPNET uses features only available in the newer Python version, which is why Python >= 3.9 is needed along with
several Python package dependencies.

OOPNET is available on PyPI and can be easily installed together with its dependencies using `pip`:

```bash
pip install oopnet
```

Alternatively, you can install OOPNET from its repository:


```bash
pip install git+https://github.com/oopnet/oopnet.git
```

### Dependencies
OOPNET requires the following Python packages:
- networkx
- numpy
- pandas
- xarray
- matplotlib
- bokeh

On Linux and macOS, EPANET has to be installed as well and has to be added to the `path` environment variable. Windows users don't have to have EPANET installed.

## Basic Usage

To use OOPNET, you first have to import it in your script:

```python
import oopnet as on
```

In OOPNET, everything is about the `Network`. If you want to start with a new, empty Network, type the following:

```python
network = on.Network()
```

If you want to read an existing EPANET model, you can `read` it as an input-file:

```python
filename = "network.inp"
network = on.Network.read(filename)
```

To simulate the model, you can use the Network\`s `run` method:

```python
report = network.run()
```

If you want to create a basic Network plot, you can use its `plot` method:

```python
network.plot()
```

## License

OOPNET is available under a [MIT License](https://github.com/oopnet/oopnet/blob/main/LICENSE.md).

## Contributing
If you want to contribute, please check out our [Code of Conduct](https://github.com/oopnet/oopnet/blob/main/CODE_OF_CONDUCT.md) and our [Contribution Guide](https://github.com/oopnet/oopnet/blob/main/CONTRIBUTING.md). Looking forward to your pull request or issue!

## Citing
If you publish work based on OOPNET, we appreciate a citation of the following reference:
 
 - Steffelbauer, D., Fuchs-Hanusch, D., 2015. OOPNET: an object-oriented EPANET in Python. Procedia Eng. 119, 710e718. https://doi.org/10.1016/j.proeng.2015.08.924.
