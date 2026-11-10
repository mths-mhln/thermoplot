# Installation

## Requirements

| Requirement | Version | Notes |
| --- | --- | --- |
| Python | 3.12 or newer | |
| REFPROP | 10 | Licensed software from NIST. Thermoplot evaluates all properties with REFPROP. |
| CoolProp | 7.2.0 | Interface to REFPROP. |
| Matplotlib | 3.10.9 | |
| NumPy | 2.2.1 | |
| SciPy | 1.17.1 | |
| pandas | 2.3.3 or newer | |
| LaTeX | any recent distribution | Only for `latex_formatting = True`; see [Matplotlib's usetex guide](https://matplotlib.org/stable/users/explain/text/usetex.html). The preamble loads `lmodern`, `siunitx` and `bm`. |

The Python dependencies and their versions are pinned in `pyproject.toml` and `uv.lock`.

## Get the code

```bash
git clone https://github.com/mths-mhln/thermoplot.git
cd thermoplot
```

The repository has the following layout:

```text
thermoplot/
├── config/                  example configuration files (CO2, R1234ze(E))
├── src/
│   ├── thermoplot.py        thermoplot() and thermoplot_cached(): the entry points
│   ├── configthermoplot.py  reading and checking the configuration file
│   ├── isolines.py          saturation dome, critical isoline and isolines
│   ├── labelling.py         label placement along the isolines
│   ├── coolprop_interface_thermoplot.py   vectorized property interface
│   └── utils.py             LaTeX formatting and critical point
├── main.py                  minimal example
├── pyproject.toml
└── uv.lock
```

## Create the environment

With [uv](https://docs.astral.sh/uv/), which reads the pinned versions from `uv.lock`:

```bash
uv sync
uv run main.py
```

With pip:

```bash
python -m venv .venv
.venv\Scripts\activate           # on Linux or macOS: source .venv/bin/activate
pip install coolprop==7.2.0 matplotlib==3.10.9 numpy==2.2.1 scipy==1.17.1 pandas
python main.py
```

## Make REFPROP available to CoolProp

CoolProp loads the REFPROP library (`REFPRP64.dll` on 64-bit Windows) at the first property call, and looks for it in the current folder and on the system `PATH`. If it cannot find it there, point CoolProp to the REFPROP folder before calling Thermoplot:

```python
import CoolProp.CoolProp as CP
CP.set_config_string(CP.ALTERNATIVE_REFPROP_PATH, r"C:\Program Files (x86)\REFPROP")
```

To check the setup, create a REFPROP state; this raises an error that starts with "Could not load REFPROP" if the library is not found:

```python
from CoolProp import AbstractState
AbstractState("REFPROP", "CO2")
```

## Check the installation

`main.py` draws the T–s diagram of CO2 from `config/CO2.ini` and opens it in a window. The first run prints `cache does not exist`, because the diagram is computed and stored in the cache ({doc}`user_guide/caching`); later runs return it from the cache.

```{note}
Thermoplot is not an installable package: the modules in `src` import each other by their plain module names, for example `from configthermoplot import ConfigThermoplot`. The `src` folder must therefore be on the Python path, as `main.py` arranges with `sys.path.append`. {doc}`user_guide/integration` describes how to use Thermoplot from another project.
```
