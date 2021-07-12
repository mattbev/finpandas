# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

sys.path.insert(0, os.path.abspath('../'))

import sphinx.ext.apidoc as apidoc
def setup(app):
    # app.add_javascript('copybutton.js')
    apidoc.main(
        ['-f', #Overwrite existing files
        '-T', #Create table of contents
        '-e', #Give modules their own pages
        #'-E', #user docstring headers
        '-M', #Modules first
        '-o', #Output the files to:
        './_autogen/', #Output Directory
        './../finpandas', #Main Module directory
        ]
    )


# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False


# -- Project information -----------------------------------------------------

project = 'finpandas'
copyright = '2021, Matthew Beveridge'
author = 'Matthew Beveridge'


# the short version
version = 'v0.1'
# The full version, including alpha/beta/rc tags
release = '0.1.0alpha'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.autodoc", "sphinx.ext.coverage", "sphinx.ext.napoleon", "sphinx.ext.todo"]


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# main page
master_doc = 'index'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
# import sphinx_theme
# html_theme_path = [sphinx_theme.get_html_theme_path()]


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# favicon
# html_favicon = "black_minimal.ico"