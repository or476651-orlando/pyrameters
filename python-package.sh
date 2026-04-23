#!/bin/bash

# 1. Check for Project Name
if [ -z "$1" ]; then
    echo "❌ Error: Please provide a project name."
    echo "Usage: bash setup_project.sh my_project"
    exit 1
fi

PROJECT_NAME=$1
SRC_DIR="src/$PROJECT_NAME"

echo "🚀 Building $PROJECT_NAME architecture..."

# 2. Create Directory Structure
mkdir -p "$SRC_DIR"
mkdir -p tests
mkdir -p docs/_static
mkdir -p docs/_templates
mkdir -p .github/workflows

# 3. Create Sample Solver Code
cat <<EOF > "$SRC_DIR/solvers.py"
def solve_example(input_data):
    """
    A placeholder solver following the backtracking pattern.

    Args:
        input_data (list): The problem constraints.

    Returns:
        list: The solution found.
    """
    if not input_data:
        return []
    return input_data
EOF

touch "$SRC_DIR/__init__.py"

# 4. Create Sample Test
cat <<EOF > tests/test_solvers.py
from $PROJECT_NAME.solvers import solve_example

def test_solve_example_empty():
    """Test that the solver handles empty input correctly."""
    assert solve_example([]) == []

def test_solve_example_data():
    """Test the solver with sample data."""
    data = [1, 2, 3]
    assert solve_example(data) == data
EOF

# 5. Create pyproject.toml
cat <<EOF > pyproject.toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "$PROJECT_NAME"
version = "0.1.0"
description = "Backtracking optimization solvers."
requires-python = ">=3.8"
dependencies = []

[project.optional-dependencies]
test = ["pytest"]
docs = ["sphinx", "sphinx-rtd-theme"]
EOF

# 6. Setup Sphinx (conf.py and index.rst)
cat <<EOF > docs/conf.py
import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

project = '$PROJECT_NAME'
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
EOF

cat <<EOF > docs/index.rst
$PROJECT_NAME Documentation
==========================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Solvers API
-----------
.. automodule:: $PROJECT_NAME.solvers
   :members:
   :undoc-members:
EOF

# 7. Create Makefile with PDF Target
cat <<'EOF' > docs/Makefile
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile pdf

pdf:
	@$(SPHINXBUILD) -M latexpdf "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
EOF

# 8. Create GitHub Actions (HTML Only)
cat <<EOF > .github/workflows/docs.yml
name: Deploy Documentation
on:
  push:
    branches: [ main ]

permissions:
  contents: write

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install .[docs]

      - name: Build HTML
        run: cd docs && make html

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: \${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs/_build/html
EOF

# 9. Final touches (README, gitignore, install)
echo "# $PROJECT_NAME" > README.md
cat <<EOF > .gitignore
__pycache__/
*.py[cod]
.pytest_cache/
docs/_build/
dist/
build/
*.egg-info/
EOF

echo "📦 Installing package in editable mode..."
pip install -e ".[test,docs]"

echo "-------------------------------------------------------"
echo "✅ Project $PROJECT_NAME successfully created!"
echo "-------------------------------------------------------"
echo "STUDENT INSTRUCTIONS:"
echo "1. Run 'pytest' to check your solvers."
echo "2. Run 'cd docs && make pdf' to create local PDF docs (requires LaTeX)."
echo "3. Commit and push to GitHub 'main' branch."
echo "4. ACTIVATE GITHUB PAGES:"
echo "   a. Go to your repo on GitHub.com -> Settings -> Pages."
echo "   b. Under 'Build and deployment' > 'Branch', select 'gh-pages'."
echo "   c. Click 'Save'. Your site will be live in a few minutes!"
echo "-------------------------------------------------------"