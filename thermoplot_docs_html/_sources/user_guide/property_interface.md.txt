# Property interface

Thermoplot evaluates all fluid properties through {class}`CoolPropAbstractState <coolprop_interface_thermoplot.CoolPropAbstractState>`, a wrapper around the low-level `AbstractState` interface of CoolProp. It combines the familiar syntax of CoolProp's `PropsSI` function with the speed of the low-level interface, and accepts arrays. You can also use it on its own.

```python
import sys
sys.path.insert(0, "src")
import numpy as np
from coolprop_interface_thermoplot import CoolPropAbstractState

AS = CoolPropAbstractState("REFPROP", "CO2")

T = np.linspace(230.0, 300.0, 8)
s_liquid = AS.PropsSI("S", "T", T, "Q", 0)              # array of saturated-liquid entropies
h, rho = AS.PropsSI(("H", "D"), "P", 9e6, "T", 308.0)   # two properties from one state update
p_crit = AS.PropsSI("Pcrit")                             # fluid constant, no inputs
```

## Creating the object

`CoolPropAbstractState(library, fluid_name)` takes

- `library`: the CoolProp backend, `"REFPROP"` or `"HEOS"` (CoolProp's own implementation of the reference equations of state); `"CoolProp"` is accepted as an alias of `"HEOS"`;
- `fluid_name`: the fluid name in the CoolProp convention.

Thermoplot itself always uses `"REFPROP"`.

## Calling `PropsSI`

```python
AS.PropsSI(prop, x_str, x, y_str, y)
```

| Argument | Meaning |
| --- | --- |
| `prop` | output property, or a tuple of output properties |
| `x_str`, `y_str` | names of the two input properties, in either order |
| `x`, `y` | input values, as numbers or arrays of the same shape |

The result has the shape of the inputs. Points for which CoolProp finds no solution return `NaN` instead of raising an error, which lets you evaluate a whole grid at once. A tuple of output properties returns a tuple of results, computed from a single state update per point.

### Input properties

| Name | Property | Unit |
| --- | --- | --- |
| `P` | pressure | Pa |
| `T` | temperature | K |
| `D` or `Dmass` | density | kg/m³ |
| `H` or `Hmass` | specific enthalpy | J/kg |
| `S` or `Smass` | specific entropy | J/(kg K) |
| `U` or `Umass` | specific internal energy | J/kg |
| `Q` | vapour quality | – |

The supported input pairs, accepted in either order, are:

| | P | T | D | H | S | U | Q |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **P** | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **T** | ✓ | | ✓ | ✓ | ✓ | ✓ | ✓ |
| **D** | ✓ | ✓ | | ✓ | ✓ | ✓ | ✓ |
| **H** | ✓ | ✓ | ✓ | | ✓ | | |
| **S** | ✓ | ✓ | ✓ | ✓ | | ✓ | ✓ |
| **U** | ✓ | ✓ | ✓ | | ✓ | | |
| **Q** | ✓ | ✓ | ✓ | | ✓ | | |

Other pairs raise a `ValueError` that lists the supported combinations. Whether a pair can be solved also depends on the backend: HEOS, for instance, does not support enthalpy with temperature.

### Output properties

| Name | Property |
| --- | --- |
| `P`, `T`, `Q` | pressure, temperature, vapour quality (clipped to the range 0 to 1) |
| `D`, `H`, `S`, `U` | density and the specific enthalpy, entropy and internal energy |
| `A` | speed of sound |
| `G` | specific Gibbs energy |
| `Cpmass`, `Cvmass` | isobaric and isochoric specific heat capacity |
| `V` | dynamic viscosity |
| `Phase` | CoolProp phase index |
| `d(P)/d(D)\|T`, `d(P)/d(D)\|U`, `d(P)/d(U)\|D` | partial derivatives of the pressure |

The fluid constants `Tcrit`, `Pcrit`, `Dcrit`, `Ttriple`, `Tmax` and `M` (molar mass) take no input properties. Any other name is passed on to the `AbstractState` method of the same name.

## Behaviour near the critical point

Flash calculations at or near the critical point often fail. When an update fails and an input equals its critical value within a relative tolerance of $10^{-5}$, the wrapper retries with that input pinned to the critical value, or sets the state to the critical point if both inputs are critical. If the retry fails as well, it returns `NaN`.
