# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
import os


sys.path.append('/opt/homebrew/Caskroom/miniforge/base/envs/sphinx/lib/python3.11/site-packages')
project = 'metaFun'
copyright = '2024, HyeonGwon Lee'
author = 'HyeonGwon Lee'
release = '0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']
html_logo = "_static/ref_picture.png"
html_title = "My site title"
#html_sidebars = {
#    "**": ["sbt-sidebar-nav.html"]
#}
html_theme_options = {
    "use_sidenotes": True,
     "home_page_in_toc": True ,
    "pygments_light_style": "default",
    "pygments_dark_style": "monokai"
}
html_css_files = [
    'custom.css',
]
def   setup(app):
    app.add_css_file('css/custom.css')
    
#html4_writer = truefrom sphinx_markdown_parser.parser import MarkdownParser

from sphinx_markdown_parser.parser import MarkdownParser

from recommonmark.parser import CommonMarkParser



extensions = [
    'myst_nb',
    'sphinx_book_theme',
    'nbsphinx',
    'sphinx_thebe',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosectionlabel',
    ]

myst_enable_extensions = [
    "dollarmath",
    "amsmath",
    "deflist",
    "html_admonition",
    "html_image",
    "colon_fence",
    "linkify",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
    "colon_fence"   
]

pygments_style = 'sphinx' 
#source_suffix = {
#    '.rst': 'restructuredtext',
#    '.md': 'markdown',
#    '.ipynb': 'myst-nb'
#}

#html_sidebars = {
#    '**': ['globaltoc.html', 'relations.html', 'sourcelink.html', 'searchbox.html'],
#}
