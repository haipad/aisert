import os
import sys
sys.path.insert(0, os.path.abspath('../'))

project = 'Aisert'
copyright = '2024, haipad'
author = 'haipad'
release = '0.2.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.doctest',
]

# Autosummary settings
autosummary_generate = False

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# Add custom object names
add_function_parentheses = False
add_module_names = False

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pydantic': ('https://docs.pydantic.dev/latest/', None),
}

# HTML theme
html_theme = 'python_docs_theme'
html_theme_options = {
    'collapsiblesidebar': True,
    'externalrefs': True,
}

# Fallback to alabaster if python_docs_theme not available
try:
    import python_docs_theme
except ImportError:
    html_theme = 'alabaster'
    html_theme_options = {
        'github_user': 'haipad',
        'github_repo': 'aisert',
        'description': 'Assert-style validation library for AI outputs',
        'fixed_sidebar': True,
    }
