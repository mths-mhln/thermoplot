# Building this documentation

The documentation is written in Markdown ([MyST](https://myst-parser.readthedocs.io/)) and built with [Sphinx](https://www.sphinx-doc.org/) and the [Furo](https://pradyunsg.me/furo/) theme. Its sources live in the `docs` folder:

```text
docs/
├── conf.py                 Sphinx configuration
├── requirements.txt        packages needed to build the documentation
├── index.md                landing page
├── installation.md, quickstart.md, troubleshooting.md, limitations.md, api.md
├── user_guide/             one page per topic
├── examples/               gallery page and example configuration files
├── _static/gallery/        figures of the gallery
└── _scripts/generate_figures.py   script that regenerates those figures
```

## Build locally

From the root of the repository:

```bash
pip install -r docs/requirements.txt
sphinx-build -b html docs docs/_build/html
```

Then open `docs/_build/html/index.html`. On Windows, `docs\make.bat html` does the same; on Linux and macOS, `make -C docs html`. The build does not need REFPROP, CoolProp or Matplotlib: the API reference is generated from the docstrings with these packages replaced by placeholders.

## Regenerate the figures

The gallery figures are stored in the repository. After a change that affects the diagrams, regenerate them in the environment of Thermoplot:

```bash
python docs/_scripts/generate_figures.py
```

## Publish

Two options are prepared:

- **GitHub Pages.** The workflow `.github/workflows/docs.yml` builds the documentation on every push to `master` and publishes it. Enable it once under *Settings*, *Pages*, *Build and deployment*, *Source: GitHub Actions*. The documentation then appears at `https://mths-mhln.github.io/thermoplot/`.
- **Read the Docs.** `.readthedocs.yaml` configures the build; import the repository on [readthedocs.org](https://readthedocs.org/).

## Docstrings

The API reference is generated from the docstrings with the NumPy style of `sphinx.ext.napoleon`. Sections titled `Parameters` (or `Arguments`), `Returns` and `Raises`, each underlined with dashes and preceded by a blank line, render best. `conf.py` maps the titles `Attributes` (in functions) and `Result`, which some docstrings use, onto `Parameters` and `Returns`.
