# Working with the figure

`thermoplot` returns an ordinary `matplotlib.figure.Figure`. Everything Matplotlib offers therefore applies: adding curves and annotations, changing the size, restyling the background and saving in any format.

```python
from thermoplot import thermoplot

fig = thermoplot("config/CO2.ini")
ax = fig.get_axes()[0]
```

## Add processes

Plot states and processes in the units of the axes ({doc}`diagrams`): entropy in J/(kg K) and temperature in K for a T–s diagram, enthalpy in J/kg and pressure in Pa for a p–h diagram. Use a `zorder` of 10 or more to draw above the background.

```python
import numpy as np
import CoolProp.CoolProp as CP

# states of a cycle, as arrays of entropy and temperature
s = np.array([1100.0, 1350.0, 1900.0, 1750.0, 1100.0])
T = np.array([280.0, 300.0, 330.0, 280.0, 280.0])
ax.plot(s, T, "o-", color="crimson", lw=2, zorder=10, label="cycle")
ax.legend()
```

The {doc}`../quickstart` computes an isentropic and an isenthalpic expansion with CoolProp and plots them in the same way. On a p–h diagram, the pressure axis is logarithmic, and the enthalpy must be given in J/kg:

```python
fig = thermoplot("docs/examples/CO2_PH.ini")
ax = fig.get_axes()[0]
h = CP.PropsSI("H", "P", 6e6, "T", 300.0, "CO2")      # J/kg
ax.plot([h], [6e6], "o", color="crimson", zorder=10)
```

## Restyle the background

The background consists of `Line2D` objects in `ax.lines` and labels in `ax.texts`, which you can change after the fact:

```python
for label in ax.texts:            # hide all isoline labels
    label.set_visible(False)

for line in ax.lines:             # thinner background lines
    line.set_linewidth(0.4)

ax.set_title("CO$_2$")
fig.set_size_inches(8, 5.5)       # the default size is 10 by 7 inches
```

The label angles are computed for the size and axis limits at the moment the diagram is drawn. After you resize the figure or change the axis limits, for example by zooming in an interactive window, the labels may no longer follow their lines exactly. To change the window permanently, override the ranges instead ({doc}`overriding_settings`).

## Save

```python
fig.savefig("diagram.pdf")              # vector format for reports
fig.savefig("diagram.png", dpi=300)     # raster format
```

## Typeset with LaTeX

With `latex_formatting = True`, Matplotlib renders all text with LaTeX, using a serif font and the packages `lmodern`, `siunitx` and `bm`. Your own labels can then use the same LaTeX commands, for example `\SI{9}{\mega\pascal}`. Rendering with LaTeX is noticeably slower, in particular when you pan or zoom in an interactive window, so keep it off while you work on a figure and switch it on for the final version.

```{note}
Thermoplot always creates a new figure. It cannot draw into an existing `Axes`, for example a subplot of a larger figure.
```
