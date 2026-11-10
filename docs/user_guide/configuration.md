# Configuration file

A diagram is fully described by one configuration file in the INI format. This page lists every setting, its type, its allowed values and its unit.

## File format

```ini
[THERMOPLOT SETTINGS]

; comment lines start with ; or #
diagram_type = TS
fluid_name = CO2
S_range = [500, 2250]
```

- All settings belong to the single section `[THERMOPLOT SETTINGS]`.
- Keys are case-sensitive: write `S_range`, not `s_range`.
- Comments must stand on their own line. A comment after a value becomes part of the value.
- Values are converted as follows:

| Written in the file | Becomes in Python | Example |
| --- | --- | --- |
| text in square brackets, separated by commas | list, each item converted with these rules | `[500, 2250]` becomes `[500, 2250]` |
| `True` or `False`, in any case | `bool` | `true` becomes `True` |
| a number without fractional part | `int` | `400`, `1e5` |
| any other number | `float` | `0.5`, `2.5e6` |
| anything else | `str` | `CO2`, `TS` |

## Settings

Every setting below must be present; the file is rejected otherwise. The comments in the example files mention defaults, but Thermoplot does not fill in missing settings.

| Setting | Type | Allowed values | Unit | Description |
| --- | --- | --- | --- | --- |
| `diagram_type` | str | `TS`, `PH` | | Diagram type: temperature against entropy, or pressure (logarithmic) against enthalpy. Upper case. |
| `fluid_name` | str | a fluid name in the CoolProp convention that REFPROP knows, e.g. `CO2`, `R1234ze(E)`, `Water` | | Working fluid. |
| `show_isolines` | bool | `True`, `False` | | Draw the isolines of quality and the two isoline families of the diagram. With `False`, only the saturation dome, the critical point and the critical isoline remain. |
| `show_critical_point` | bool | `True`, `False` | | Required, but not used in version 0.1.0: the critical point is always drawn. |
| `show_critical_isoline` | bool | `True`, `False` | | Required, but not used in version 0.1.0: the critical isoline is always drawn. |
| `show_spinodal` | bool | `True`, `False` | | Required, but not used in version 0.1.0: spinodal curves are not yet implemented. |
| `n_pts` | int | 2 or more; 400 in the examples | | Number of points per isoline. The saturation dome uses twice as many. More points give smoother lines and take longer. |
| `latex_formatting` | bool | `True`, `False` | | Typeset all text with LaTeX. Requires a LaTeX installation and makes interactive windows slower. |

Depending on `diagram_type`, two range settings are also required. Each is a list of a lower and an upper bound.

| Setting | Required for | Unit | Description |
| --- | --- | --- | --- |
| `S_range` | `TS` | J/(kg K) | Limits of the horizontal (entropy) axis. |
| `T_range` | `TS` | K | Limits of the vertical (temperature) axis. |
| `H_range` | `PH` | J/kg | Limits of the horizontal (enthalpy) axis. The tick labels show kJ/kg. |
| `P_range` | `PH` | Pa | Limits of the vertical (pressure) axis, on a logarithmic scale. |

The ranges set the axis limits, and also decide which isolines are drawn: the isenthalps of a T–s diagram and the isentropes of a p–h diagram are spread over the enthalpy or entropy range found inside the window ({doc}`diagrams`).

## Validation

When the file is read, Thermoplot checks that

1. the section `[THERMOPLOT SETTINGS]` exists, otherwise it raises `ValueError: Missing 'THERMOPLOT SETTINGS' section in config file`;
2. `diagram_type` is present, otherwise `ValueError: Missing necessary thermoplot setting: diagram_type`;
3. all settings required for the diagram type are present, otherwise `ValueError: Missing necessary thermoplot settings in config file: [...]`, listing the missing keys.

Types and values are not checked. A `diagram_type` other than `TS` or `PH` passes the checks but fails later, and ranges outside the validity of the fluid (for example below its triple point) simply leave parts of the diagram empty. Settings that Thermoplot does not know are read without error and ignored.

## Choosing the ranges

Good ranges enclose the saturation dome and the states of the processes you want to plot. CoolProp gives the reference values:

```python
import CoolProp.CoolProp as CP

fluid = "CO2"
T_triple = CP.PropsSI("Ttriple", fluid)
T_crit, p_crit = CP.PropsSI("Tcrit", fluid), CP.PropsSI("Pcrit", fluid)
s_liquid = CP.PropsSI("S", "T", 1.02 * T_triple, "Q", 0, fluid)   # left edge of the dome
s_vapour = CP.PropsSI("S", "T", 1.02 * T_triple, "Q", 1, fluid)   # right edge of the dome
print(f"T_range = [{1.02 * T_triple:.0f}, {1.15 * T_crit:.0f}]")
print(f"S_range = [{0.9 * s_liquid:.0f}, {1.05 * s_vapour:.0f}]")
```

Keep the lower temperature above the triple-point temperature: the saturation dome ends there, and the equations of state do not describe solid states.

## Example files

The repository contains two T–s configurations, and this documentation adds a p–h configuration:

```{literalinclude} ../../config/R1234ze(E).ini
:language: ini
:caption: config/R1234ze(E).ini
```

```{literalinclude} ../examples/CO2_PH.ini
:language: ini
:caption: docs/examples/CO2_PH.ini
```
