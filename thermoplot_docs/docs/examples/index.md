# Examples

Each example below lists the code and the figure it produces. Run the examples from the root of the repository, after adding `src` to the Python path:

```python
import sys
sys.path.insert(0, "src")
from thermoplot import thermoplot
```

```{note}
The figures on this page were generated with `docs/_scripts/generate_figures.py`. REFPROP was not available on the machine that built them, so the script used the HEOS backend of CoolProp, which implements the same reference equations of state. HEOS cannot evaluate states from enthalpy and temperature, so the dotted critical isotherm is missing from the p–h example; with REFPROP it is drawn.
```

## T–s diagram of CO2

The configuration file shipped in `config/CO2.ini`.

```python
fig = thermoplot("config/CO2.ini")
```

```{image} ../_static/gallery/co2_ts.png
:alt: T-s diagram of CO2.
:width: 100%
```

## T–s diagram of R1234ze(E)

A refrigerant for high-temperature heat pumps, from `config/R1234ze(E).ini`.

```python
fig = thermoplot("config/R1234ze(E).ini")
```

```{image} ../_static/gallery/r1234ze_ts.png
:alt: T-s diagram of R1234ze(E).
:width: 100%
```

## p–h diagram of CO2

The configuration file `docs/examples/CO2_PH.ini` of this documentation sets `diagram_type = PH` with a pressure range of 0.6 to 20 MPa and an enthalpy range of 80 to 520 kJ/kg.

```python
fig = thermoplot("docs/examples/CO2_PH.ini")
```

```{image} ../_static/gallery/co2_ph.png
:alt: p-h diagram of CO2 with a logarithmic pressure axis.
:width: 100%
```

## Zooming in

Override the ranges to zoom in, here on the region around the critical point ({doc}`../user_guide/overriding_settings`).

```python
fig = thermoplot("config/CO2.ini", {"S_range": [900, 2000], "T_range": [260, 320]})
```

```{image} ../_static/gallery/co2_ts_zoom.png
:alt: T-s diagram of CO2 zoomed in on the critical region.
:width: 100%
```

## Saturation dome only

```python
fig = thermoplot("config/CO2.ini", {"show_isolines": False})
```

```{image} ../_static/gallery/co2_ts_no_isolines.png
:alt: T-s diagram of CO2 with only the saturation dome, the critical point and the critical isobar.
:width: 80%
```

## Expansion processes

An isentropic and an isenthalpic expansion of CO2 from 9 MPa and 308 K to 4 MPa, as in a turbine and a throttling valve. The {doc}`../quickstart` explains the code.

```python
import numpy as np
import CoolProp.CoolProp as CP

fig = thermoplot("config/CO2.ini")
ax = fig.get_axes()[0]

p_in, T_in, p_out = 9e6, 308.0, 4e6
s_in = CP.PropsSI("S", "P", p_in, "T", T_in, "CO2")
h_in = CP.PropsSI("H", "P", p_in, "T", T_in, "CO2")
p = np.geomspace(p_in, p_out, 60)
T_isentropic = CP.PropsSI("T", "P", p, "S", np.full_like(p, s_in), "CO2")
s_isenthalpic = CP.PropsSI("S", "P", p, "H", np.full_like(p, h_in), "CO2")
T_isenthalpic = CP.PropsSI("T", "P", p, "H", np.full_like(p, h_in), "CO2")

ax.plot(np.full_like(p, s_in), T_isentropic, color="crimson", lw=2, zorder=10, label="isentropic expansion")
ax.plot(s_isenthalpic, T_isenthalpic, color="seagreen", lw=2, ls="--", zorder=10, label="isenthalpic expansion")
ax.plot([s_in], [T_in], "o", color="black", zorder=11)
ax.annotate("inlet: 9 MPa, 308 K", (s_in, T_in), xytext=(12, 6), textcoords="offset points")
ax.legend(loc="upper left")
```

```{image} ../_static/gallery/co2_ts_overlay.png
:alt: T-s diagram of CO2 with an isentropic and an isenthalpic expansion.
:width: 100%
```
