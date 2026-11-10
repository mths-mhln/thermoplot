# Known limitations

This page lists the limitations of version 0.1.0 that affect users.

## Settings

- `show_critical_point`, `show_critical_isoline` and `show_spinodal` must be present in the configuration file, but have no effect: the critical point and the critical isoline are always drawn, and spinodal curves are not implemented.
- The numbers of isolines (10, 12 and 18 per family), the label positions and the colours are fixed in the code.
- `diagram_type` cannot be overridden through `thermoplot_overwrite_settings`.
- Override keys are not checked. The message that `thermoplot` prints for an unrecognized setting is never shown, since unknown keys are simply added to the settings.
- `latex_formatting = True` changes Matplotlib's global settings for the rest of the session.

## Diagrams

- The isentrope labels of the p–h diagram print the entropy in J/(kg K), but the named label states kJ/kg/K.
- Label angles are computed once, for the size and axis limits at the moment of drawing.
- Thermoplot always creates a new figure of 10 by 7 inches; it cannot draw into an existing `Axes`.

## Properties

- The property backend is fixed to REFPROP. CoolProp's open-source HEOS backend would make Thermoplot usable without a REFPROP licence, but needs two adjustments: HEOS keeps a phase imposed after a failed calculation at the critical point, which turns later pressure–temperature calls into liquid states, and it cannot solve states at exactly the critical pressure or temperature. `docs/_scripts/generate_figures.py` shows both adjustments. HEOS also does not support enthalpy and temperature as inputs, which the critical isotherm of the p–h diagram needs.

## Caching and packaging

- The cache does not notice changes to the code, to the property libraries or to Matplotlib settings ({doc}`user_guide/caching`).
- Thermoplot is not an installable package. Its modules use plain names, so they must be importable from the `src` folder, and a generic name such as `utils` can clash with other modules ({doc}`user_guide/integration`).
