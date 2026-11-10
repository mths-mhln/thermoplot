# What is drawn

Thermoplot draws the same set of elements in both diagram types. This page lists them, with the rules that decide which isolines appear and how they are labelled.

```{figure} ../_static/gallery/co2_ts.png
:alt: T-s diagram of CO2.
:width: 100%

T–s diagram of CO2 (`config/CO2.ini`).
```

```{figure} ../_static/gallery/co2_ph.png
:alt: p-h diagram of CO2 with a logarithmic pressure axis.
:width: 100%

p–h diagram of CO2 (`docs/examples/CO2_PH.ini`).
```

## Elements of the diagram

| Element | T–s diagram | p–h diagram | Style |
| --- | --- | --- | --- |
| Saturation dome | saturated liquid ($x = 0$) and vapour ($x = 1$) lines, joined at the critical point | same | black, solid |
| Critical point | marker at $(s_c, T_c)$ | marker at $(h_c, p_c)$ | yellow circle with black edge |
| Critical isoline | critical isobar, $p = p_c$ | critical isotherm, $T = T_c$ | black, dotted |
| Quality isolines | 10 lines, $x = 0, 1/9, \ldots, 1$ | same | dark blue |
| Second isoline family | 12 isobars, spaced geometrically from 1.1 times the triple-point pressure (at least 1 kPa) to 3 $p_c$ | 12 isentropes, spaced evenly over the entropy range found in the window | light blue |
| Third isoline family | 18 isenthalps, spaced evenly over the enthalpy range found in the window, widened by 5 % on both sides | 18 isotherms, spaced evenly from 1.05 times the triple-point temperature to 1.5 $T_c$ | orange |

The isolines are drawn only if `show_isolines = True`. Inside the saturation dome, isobars (T–s) and isotherms (p–h) are drawn as horizontal lines between the saturated liquid and vapour states. The numbers of isolines are fixed in the code.

## Labels

Each isoline carries one label, placed at a fixed fraction of its length and rotated to follow the local slope of the line, so that it reads along the line on screen. A semi-transparent white box keeps the label readable. The middle line of each family shows the symbol and the unit; the other lines show the value only.

| Isolines | Position along the line | Named label (middle line) | Other labels |
| --- | --- | --- | --- |
| Quality | 15 % | `x = 0.56` | `0.33` |
| Isobars (T–s) | 83 % | `p = 4212 kPa` | pressure in kPa |
| Isenthalps (T–s) | 10 % | `h = 305 kJ/kg` | enthalpy in kJ/kg |
| Isotherms (p–h) | 90 % | `T = 322 K` | temperature in K |
| Isentropes (p–h) | 83 % | `s = 1709 kJ/kg/K` | entropy in J/(kg K) |

```{note}
The isentrope labels print the entropy in J/(kg K), but the named label states the unit kJ/kg/K ({doc}`../limitations`).
```

## Axes and figure

| | T–s diagram | p–h diagram |
| --- | --- | --- |
| Horizontal axis | specific entropy $s$ in J/(kg K) | specific enthalpy $h$: data in J/kg, tick labels in kJ/kg |
| Vertical axis | temperature $T$ in K, linear | pressure $p$ in Pa, logarithmic |
| Axis limits | `S_range`, `T_range` | `H_range`, `P_range` |

The figure measures 10 by 7 inches and contains one `Axes`. The elements are stacked in this order, from bottom to top:

| `zorder` | Elements |
| --- | --- |
| 2 | isolines and critical isoline |
| 3 | saturation dome |
| 6 | labels |
| 9 | critical point |

Curves that you add with a `zorder` of 10 or more therefore lie on top of the whole background.

```{important}
When you plot on a p–h diagram, give the enthalpy in J/kg: the tick labels show kJ/kg, but the data coordinates are in J/kg.
```

## How the isolines are computed

All properties come from REFPROP, through the vectorized interface described in {doc}`property_interface`. In short:

- **Saturation dome and quality isolines:** the saturated states are evaluated at points of the vertical-axis variable, up to the critical point (temperature for T–s, pressure for p–h).
- **Isobars (T–s) and isotherms (p–h):** evaluated at points of temperature or pressure. Below the critical value, the liquid branch, the horizontal two-phase bridge and the vapour branch are computed separately and joined.
- **Isenthalps (T–s) and isentropes (p–h):** Thermoplot first samples the enthalpy or entropy on a 6 by 6 grid inside the window to find the visible range, then evaluates each line along a set of pressures.
- **Critical isoline:** evaluated at points of the horizontal-axis variable, so that it can pass the flat top of the dome.

States for which REFPROP returns no solution become `NaN` and are left out, as are points outside the window. This is why an isoline can stop at the edge of the fluid's range of validity.
