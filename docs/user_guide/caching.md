# Caching

Drawing a diagram takes a few seconds, since every isoline needs hundreds of property evaluations. {func}`thermoplot_cached <thermoplot.thermoplot_cached>` stores each diagram on disk the first time and loads it from there afterwards. It takes the same arguments as {func}`thermoplot <thermoplot.thermoplot>`.

```python
from thermoplot import thermoplot_cached

fig = thermoplot_cached("config/CO2.ini")   # first call: computes, stores, prints "cache does not exist"
fig = thermoplot_cached("config/CO2.ini")   # later calls: loads the stored figure
```

In a test with the CO2 example, the first call took about 3.5 s and later calls 0.07 s; each cached diagram takes about 0.7 MB on disk.

## Where the cache lives

The figures are stored as pickle files in the folder `pyshockflow_thermoplot_cache` inside the temporary directory of the operating system:

```python
import tempfile
from pathlib import Path

print(Path(tempfile.gettempdir()) / "pyshockflow_thermoplot_cache")
```

On Windows, this is usually `C:\Users\<user>\AppData\Local\Temp\pyshockflow_thermoplot_cache`.

## When a cached diagram is reused

Each cache file is identified by a hash of

- the path of the configuration file, as passed to the function;
- the contents of the configuration file;
- the override settings.

Editing the configuration file, or passing other overrides, therefore produces a new diagram. The cache does **not** notice changes to the code of Thermoplot, to CoolProp or REFPROP, or to Matplotlib settings. Clear it after updating any of these:

```python
import shutil, tempfile
from pathlib import Path

shutil.rmtree(Path(tempfile.gettempdir()) / "pyshockflow_thermoplot_cache", ignore_errors=True)
```

Every call returns a fresh copy of the stored figure, so changes that you make to a returned figure do not affect later calls.
