# Overriding settings

Both entry points take an optional second argument, `thermoplot_overwrite_settings`: a dictionary whose entries replace the settings read from the configuration file. This lets you draw variants of a diagram from one file.

```python
from thermoplot import thermoplot

fig = thermoplot("config/CO2.ini", {"S_range": [900, 2000], "T_range": [260, 320]})
```

The values must have the type that the file would produce after conversion ({doc}`configuration`): lists of numbers for ranges, `bool` for switches, `int` for `n_pts` and `str` for names.

## Examples

Zoom in on the critical region:

```python
fig = thermoplot("config/CO2.ini", {"S_range": [900, 2000], "T_range": [260, 320]})
```

```{figure} ../_static/gallery/co2_ts_zoom.png
:alt: T-s diagram of CO2 zoomed in on the region between 260 and 320 K.
:width: 100%

The CO2 diagram with the ranges overridden. The isenthalps adapt to the new window.
```

Draw only the saturation dome:

```python
fig = thermoplot("config/CO2.ini", {"show_isolines": False})
```

```{figure} ../_static/gallery/co2_ts_no_isolines.png
:alt: T-s diagram of CO2 that shows only the saturation dome and the critical point.
:width: 80%

The CO2 diagram without isolines.
```

Draw a series of diagrams, for instance for a report:

```python
for T_max in (310, 330, 350):
    fig = thermoplot("config/CO2.ini", {"T_range": [220, T_max]})
    fig.savefig(f"co2_ts_up_to_{T_max}K.png", dpi=200)
```

## Rules

- **Do not override `diagram_type`.** Part of the code reads the diagram type from the file and part from the overrides, so a mixed diagram results. Use a separate configuration file for each diagram type.
- **When you override `fluid_name`, override the ranges as well,** since good ranges depend on the fluid.
- **Keys are not checked.** A misspelled key, for example `"show_isoline"`, is added to the settings without any message and has no effect.
- **LaTeX settings persist.** `latex_formatting = True` changes Matplotlib's global settings for the rest of the Python session; a later diagram with `latex_formatting = False` still uses LaTeX. Call `matplotlib.rcdefaults()` to restore the defaults.
- **Cached diagrams:** with {func}`thermoplot_cached <thermoplot.thermoplot_cached>`, every combination of file and overrides is cached separately ({doc}`caching`).
