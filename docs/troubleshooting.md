# Troubleshooting

## "Could not load REFPROP"

CoolProp cannot find the REFPROP library. Install REFPROP, or point CoolProp to its folder with `CoolProp.CoolProp.set_config_string(CoolProp.CoolProp.ALTERNATIVE_REFPROP_PATH, folder)` before calling Thermoplot ({doc}`installation`).

## `ModuleNotFoundError: No module named 'configthermoplot'`

The `src` folder is not on the Python path. Add it with `sys.path.insert(0, "path/to/thermoplot/src")` before the import ({doc}`user_guide/integration`).

## `ValueError: Missing 'THERMOPLOT SETTINGS' section in config file`

The path does not point to an existing file, or the file lacks the section header. Check the path relative to the current working directory, and the spelling `[THERMOPLOT SETTINGS]`. With {func}`thermoplot_cached <thermoplot.thermoplot_cached>`, a missing file raises `FileNotFoundError` instead.

## `ValueError: Missing necessary thermoplot settings in config file: [...]`

The listed settings are missing. All settings are required, including `show_spinodal`, `show_critical_point` and `show_critical_isoline`, and keys are case-sensitive ({doc}`user_guide/configuration`).

## `KeyError` with a range name, for example `'S_range'`

`diagram_type` is neither `TS` nor `PH`, so the validation did not know which ranges to require. Write `TS` or `PH` in upper case.

## The diagram is empty, or isolines are missing

- The ranges are given in the wrong units: entropy in J/(kg K), enthalpy in J/kg and pressure in Pa, not in kJ or MPa.
- The ranges lie partly outside the validity of the equation of state, for example below the triple point.
- `show_isolines = False`.

Warnings such as `RuntimeWarning: invalid value encountered` come from points for which REFPROP finds no solution. These points are left out and the warnings can be ignored.

## Changes have no effect with `thermoplot_cached`

The cache does not notice changes to the code of Thermoplot or to the property libraries. Clear it ({doc}`user_guide/caching`). Changes to the configuration file itself are always picked up.

## LaTeX errors, or very slow figures

`latex_formatting = True` requires a working LaTeX installation with the packages `lmodern`, `siunitx` and `bm`, and makes interaction slower. Set it to `False` while you work on a figure.

## LaTeX is still used after setting `latex_formatting = False`

The LaTeX settings of an earlier diagram persist in the same Python session. Call `matplotlib.rcdefaults()`, or restart Python.

## A setting passed in the override dictionary has no effect

Override keys are not checked: a misspelled key is accepted silently. Compare the key with the list in {doc}`user_guide/configuration`. Overriding `diagram_type` is not supported ({doc}`user_guide/overriding_settings`).

## Labels no longer follow their lines

The label angles were computed for the figure size and axis limits when the diagram was drawn. Override the ranges instead of zooming, or redraw the diagram after resizing.

## "cache does not exist" is printed

This is not an error: {func}`thermoplot_cached <thermoplot.thermoplot_cached>` reports that it computes the diagram because no stored copy exists yet.
