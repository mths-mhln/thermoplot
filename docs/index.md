# Thermoplot

Thermoplot draws the background of a thermodynamic diagram, a temperature–entropy (T–s) or a pressure–enthalpy (p–h) diagram, for any fluid available in REFPROP. It returns the diagram as a standard Matplotlib figure, so you can plot your own processes on top of it: a heat pump cycle, a nozzle expansion, or measured states.

```{figure} _static/gallery/co2_ts.png
:alt: Temperature-entropy diagram of CO2 with the saturation dome, the critical point, and labelled isolines of vapour quality, pressure and enthalpy.
:width: 100%

T–s diagram of CO2, drawn from the configuration file `config/CO2.ini` that ships with the repository.
```

## Features

- **Two diagram types:** T–s, and p–h with a logarithmic pressure axis.
- **Complete background:** saturation dome, critical point, critical isoline, and isolines of vapour quality, pressure and enthalpy (T–s) or temperature and entropy (p–h).
- **Readable labels:** every isoline carries a label that follows its local slope; the middle line of each family also shows the symbol and unit.
- **Any REFPROP fluid,** named with the CoolProp convention, for example `CO2`, `R1234ze(E)` or `Water`.
- **One configuration file** per diagram, whose settings you can override from Python without editing the file.
- **LaTeX typesetting** of all text, for figures that match a LaTeX document.
- **Disk cache:** a diagram that was drawn before is returned in a fraction of a second.
- **Vectorized property interface:** a `PropsSI`-style wrapper around the CoolProp low-level interface, also usable on its own.

## Quick example

```python
import sys
sys.path.insert(0, "src")           # thermoplot lives in the src folder of the repository

import matplotlib.pyplot as plt
from thermoplot import thermoplot

fig = thermoplot("config/CO2.ini")  # returns a matplotlib.figure.Figure
plt.show()
```

Continue with {doc}`installation` and the {doc}`quickstart`, or browse the {doc}`examples/index`.

```{toctree}
:maxdepth: 2
:caption: Getting started
:hidden:

installation
quickstart
```

```{toctree}
:maxdepth: 2
:caption: User guide
:hidden:

user_guide/configuration
user_guide/diagrams
user_guide/overriding_settings
user_guide/customizing_figures
user_guide/caching
user_guide/property_interface
user_guide/integration
```

```{toctree}
:maxdepth: 2
:caption: Examples
:hidden:

examples/index
```

```{toctree}
:maxdepth: 2
:caption: Reference
:hidden:

api
troubleshooting
limitations
building_docs
```
