# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import enum
import os
import sys

sys.path.insert(0, os.path.abspath('..'))

import xjsonrpc  # noqa


# -- Project information -----------------------------------------------------

project = xjsonrpc.__title__
author = xjsonrpc.__author__
copyright = '2019, {}'.format(author)

# The full version, including alpha/beta/rc tags
release = xjsonrpc.__version__
version = xjsonrpc.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
]

html_theme_options = {
    'github_user': 'bernhardkaindl',
    'github_repo': 'xjsonrpc',
    'github_banner': True,
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_css_files = ['css/custom.css']

# The master toctree document.
master_doc = 'index'

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'aiohttp': ('https://aiohttp.readthedocs.io/en/stable/', None),
    'requests': ('https://requests.kennethreitz.org/en/master/', None),
}

autodoc_mock_imports = ['attrs']
autodoc_typehints = 'description'
autodoc_member_order = 'bysource'


def maybe_skip_member(app, what, name, obj, skip, options):
    if isinstance(obj, enum.Enum):
        return False

    return None


def setup(app):
    app.connect('autodoc-skip-member', maybe_skip_member)
