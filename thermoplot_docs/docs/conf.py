"""Sphinx configuration for the Thermoplot documentation."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

project = "Thermoplot"
author = "Matthias Van Mechelen"
copyright = "2026, Matthias Van Mechelen"
release = "0.1.0"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
]
myst_enable_extensions = ["colon_fence", "deflist", "dollarmath"]
myst_heading_anchors = 3

# The documentation builds without REFPROP, CoolProp or a display.
autodoc_mock_imports = ["CoolProp", "matplotlib"]
autodoc_member_order = "bysource"
autodoc_typehints = "description"
napoleon_google_docstring = False
napoleon_numpy_docstring = True

exclude_patterns = ["_build", "_scripts", "examples/*.ini"]

html_theme = "furo"
html_title = "Thermoplot"
html_static_path = ["_static"]
html_theme_options = {
    "source_repository": "https://github.com/mths-mhln/thermoplot/",
    "source_branch": "master",
    "source_directory": "docs/",
}


def _normalize_docstring_sections(app, what, name, obj, options, lines):
    """Map the section names used in the docstrings onto those napoleon knows,
    and separate section headers from the preceding text by a blank line."""
    renamed = {"Result": "Returns"}
    if what in ("function", "method"):
        renamed["Attributes"] = "Parameters"
    out = []
    skip_underline = False
    for i, line in enumerate(lines):
        if skip_underline:
            skip_underline = False
            continue
        title = line.strip()
        underline = lines[i + 1].strip() if i + 1 < len(lines) else ""
        if title and underline and set(underline) == {"-"} and set(title) != {"-"}:
            if out and out[-1].strip():
                out.append("")
            if title == "Methods":
                # napoleon turns a Methods section into method entries, which
                # duplicate the methods that autodoc documents.
                out.extend([line.replace(title, ".. rubric:: Methods"), ""])
                skip_underline = True
                continue
            line = line.replace(title, renamed.get(title, title))
        out.append(line)
    lines[:] = out


def setup(app):
    app.connect("autodoc-process-docstring", _normalize_docstring_sections, priority=400)
