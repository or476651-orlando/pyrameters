import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

project = 'pyrameters'
copyright = '2026, Student Team'
author = 'Students'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

html_theme = 'sphinx_rtd_theme'
latex_elements = {
    'papersize': 'letterpaper',
    'pointsize': '10pt',
}
