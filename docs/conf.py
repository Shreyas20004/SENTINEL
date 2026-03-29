# Configuration file for the Sphinx documentation builder
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Add parent directory to path for autodoc
sys.path.insert(0, os.path.abspath('../../backend'))

# Project information
project = 'SENTINEL'
copyright = '2026, SENTINEL Contributors'
author = 'SENTINEL Team'
release = '1.0.0'
version = '1.0.0'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'sphinx_copybutton',
    'myst_parser',
    'sphinx_design',
    'sphinxcontrib.mermaid',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Language
language = 'en'
locale_dirs = ['locale/']

# HTML output configuration
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'style_nav_header_background': '#1f1f1f',
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False,
    'github_url': 'https://github.com/your-org/sentinel',
    'vcs_pageview_mode': 'view',
}

html_static_path = ['_static']
html_logo = '_static/sentinel-logo.png'
html_favicon = '_static/favicon.ico'

# Autodoc configuration
autodoc_typehints = 'description'
autodoc_member_order = 'bysource'
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'undoc-members': True,
    'show-inheritance': True,
}

# Napoleon extension configuration (Google/NumPy docstring style)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'fastapi': ('https://fastapi.tiangolo.com/', None),
    'sqlalchemy': ('https://docs.sqlalchemy.org/14/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
}

# MyST Parser configuration
myst_enable_extensions = [
    'colon_fence',
    'dollarmath',
    'linkify',
    'tasklist',
    'strikethrough',
]

# Copybutton configuration
copybutton_exclude = '.linenos, .gp, .go'

# Mermaid configuration
mermaid_version = 'latest'
mermaid_init_js = """
mermaid.initialize({
    'startOnLoad': true,
    'theme': 'dark',
    'dark': true,
    'securityLevel': 'loose',
});
"""

# LaTeX/PDF configuration
latex_elements = {
    'papersize': 'letterpaper',
    'pointsize': '12pt',
    'fncychap': '\\usepackage[Bjornstrup]{fncychap}',
    'figure_align': 'htbp',
}

latex_documents = [
    ('index', 'sentinel.tex', 'SENTINEL Documentation', author, 'manual'),
]

# Man page configuration
man_pages = [
    ('index', 'sentinel', 'SENTINEL Documentation', [author], 1)
]

# Texinfo configuration
texinfo_documents = [
    ('index', 'sentinel', 'SENTINEL Documentation', author, 'SENTINEL',
     'Real-Time Public Safety AI System', 'Miscellaneous'),
]
