# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
sys.path.append('/opt/homebrew/Caskroom/miniforge/base/envs/sphinx/lib/python3.12/site-packages')
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
    "pygment_light_style": "default",
    "pygment_dark_style": "monokai"
}
html_css_files = [
    'custom.css',
]
def   setup(app):
    app.add_css_file('css/custom.css')

#html4_writer = true



extensions = ["myst_parser",
                  'sphinx.ext.autodoc',
                  'sphinx.ext.napoleon',
                  'sphinx.ext.doctest',
                  'sphinx.ext.viewcode',
                  'sphinx.ext.autosectionlabel']

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
    "tasklist"    
]

pygments_style = 'sphinx' 
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
myst_enable_extensions = ["colon_fence"]

#html_sidebars = {
#    '**': ['globaltoc.html', 'relations.html', 'sourcelink.html', 'searchbox.html'],
#}
