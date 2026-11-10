# Using Thermoplot in another project

Thermoplot is a set of modules rather than an installable package: the modules in `src` import each other by their plain names, for example `from configthermoplot import ConfigThermoplot`. Three ways to use it from another project follow from this.

## Put `src` on the Python path

The simplest option, used by `main.py`, is to add the `src` folder of a clone to the Python path before the import:

```python
import sys
sys.path.insert(0, r"C:\path\to\thermoplot\src")

from thermoplot import thermoplot, thermoplot_cached
```

The modules then become top-level modules named `thermoplot`, `configthermoplot`, `isolines`, `labelling`, `utils` and `coolprop_interface_thermoplot`. A module with the same name elsewhere on the path, `utils` in particular, can shadow one of them; insert the folder at the front of the path, as above, to give Thermoplot priority.

## Copy the modules into your project

PyShockFlow carries a copy of Thermoplot in `src/thermoplot` and calls it from its post-processing, which draws the expansion path of a nozzle simulation on a T–s diagram:

```python
from pyshockflow.post_processing import generate_expansion_thermoplot

fig = generate_expansion_thermoplot(
    resultsFolders=["Results/lettieri/output_L1_friction"],
    iterationIndexes=[-1],
    simulationLegendLabels=["L1, friction"],
    thermoplotConfigFilePath="inputs/thermoplot/CO2.ini",
)
```

A copy is independent of later changes in this repository, so update it when Thermoplot changes.

## Merge the settings into your own configuration

If your project already reads an INI configuration file, you can keep a single file: add the `[THERMOPLOT SETTINGS]` section with its settings to your file, and pass that file to Thermoplot. {class}`ConfigThermoplot <configthermoplot.ConfigThermoplot>` reads only its own section and ignores all others. Alternatively, copy the parsing logic of `ConfigThermoplot` into your own configuration parser.
