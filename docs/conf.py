# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join('..', '..', 'oopnet')))
from oopnet import __version__

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'OOPNET'
copyright = '2022, David B. Steffelbauer'
author = 'David B. Steffelbauer'
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'sphinx_mdinclude',
    'bokeh.sphinxext.bokeh_plot'

]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
source_suffix = ['.rst', '.md']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'sphinx_rtd_theme'
html_theme = 'sphinx_material'
html_static_path = ['_static', 'figures']
html_sidebars = {
    "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]
}

html_theme_options = {
    'repo_url': 'https://github.com/oopnet/oopnet/',
    'html_minify': True,
    'css_minify': True,
    'logo_icon': '&#xe91c',
    'color_primary': 'blue',
    'color_accent': 'light-blue',
    'nav_title': 'OOPNET',
    'globaltoc_depth': 2,
    'globaltoc_collapse': False
}
