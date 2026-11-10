# Quickstart

This page draws a T–s diagram of CO2, plots two expansion processes on top of it and saves the result.

## 1. Write a configuration file

All settings of a diagram live in one INI file with the section `[THERMOPLOT SETTINGS]`. The repository ships `config/CO2.ini`:

```{literalinclude} ../config/CO2.ini
:language: ini
```

{doc}`user_guide/configuration` explains every setting.

## 2. Draw the diagram

```python
import sys
sys.path.insert(0, "src")

import matplotlib.pyplot as plt
from thermoplot import thermoplot

fig = thermoplot("config/CO2.ini")
ax = fig.get_axes()[0]
```

`thermoplot` returns a `matplotlib.figure.Figure` with a single `Axes`. Use {func}`thermoplot_cached <thermoplot.thermoplot_cached>` instead if the same diagram is drawn repeatedly, for example in a post-processing script ({doc}`user_guide/caching`).

## 3. Plot your own processes

The axes use SI units: entropy in J/(kg K) on the horizontal axis and temperature in K on the vertical axis. The example computes an isentropic and an isenthalpic expansion of CO2 from 9 MPa and 308 K to 4 MPa with CoolProp, and plots them:

```python
import numpy as np
import CoolProp.CoolProp as CP

p_in, T_in, p_out = 9e6, 308.0, 4e6
s_in = CP.PropsSI("S", "P", p_in, "T", T_in, "CO2")
h_in = CP.PropsSI("H", "P", p_in, "T", T_in, "CO2")
p = np.geomspace(p_in, p_out, 60)

T_isentropic = CP.PropsSI("T", "P", p, "S", np.full_like(p, s_in), "CO2")
s_isenthalpic = CP.PropsSI("S", "P", p, "H", np.full_like(p, h_in), "CO2")
T_isenthalpic = CP.PropsSI("T", "P", p, "H", np.full_like(p, h_in), "CO2")

ax.plot(np.full_like(p, s_in), T_isentropic, color="crimson", lw=2, zorder=10, label="isentropic expansion")
ax.plot(s_isenthalpic, T_isenthalpic, color="seagreen", lw=2, ls="--", zorder=10, label="isenthalpic expansion")
ax.legend(loc="upper left")
```

```{figure} _static/gallery/co2_ts_overlay.png
:alt: T-s diagram of CO2 with an isentropic expansion drawn as a vertical red line and an isenthalpic expansion drawn as a dashed green curve.
:width: 100%

Isentropic and isenthalpic expansion of CO2 from 9 MPa and 308 K to 4 MPa. A `zorder` of 10 or more keeps your curves above the diagram background.
```

## 4. Save the figure

```python
fig.savefig("co2_ts.pdf")            # vector format for reports
fig.savefig("co2_ts.png", dpi=200)   # raster format
plt.show()
```

## Next steps

- {doc}`user_guide/diagrams` describes what is drawn and how.
- {doc}`user_guide/overriding_settings` shows how to vary settings without editing the file.
- {doc}`examples/index` collects complete examples, including a p–h diagram.
