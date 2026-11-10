"""Regenerate the example figures of the documentation.

Run from the repository root:

    python docs/_scripts/generate_figures.py

The figures are written to docs/_static/gallery/. Thermoplot uses REFPROP. On a
machine without REFPROP, the script switches to the HEOS backend of CoolProp,
which implements the same reference equations of state.
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

import matplotlib

matplotlib.use("Agg")
import CoolProp.CoolProp as CP
from CoolProp import AbstractState

import thermoplot as tp
from coolprop_interface_thermoplot import CoolPropAbstractState

OUT = ROOT / "docs" / "_static" / "gallery"
EXAMPLES = ROOT / "docs" / "examples"
CONFIG = ROOT / "config"


class HEOSAbstractState(CoolPropAbstractState):
    """Thermoplot's property wrapper with the HEOS backend instead of REFPROP."""

    def __init__(self, library, fluid_name):
        super().__init__("HEOS", fluid_name)

    def _extract(self, AS, x_str_AS, x, y_str_AS, y, prop_AS, input_spec, verbose=False):
        # HEOS keeps a phase imposed after a failed flash at the critical point,
        # which turns every later (p, T) call into a liquid state.
        AS.unspecify_phase()
        # HEOS cannot flash at exactly the critical pressure or temperature, which
        # the critical isobar (T-s) and critical isotherm (p-h) require.
        T_crit, _, p_crit = self.critical_point_vals
        critical = {"P": p_crit, "T": T_crit}
        if x_str_AS in critical and x == critical[x_str_AS]:
            x *= 1 + 1e-9
        if y_str_AS in critical and y == critical[y_str_AS]:
            y *= 1 + 1e-9
        return super()._extract(AS, x_str_AS, x, y_str_AS, y, prop_AS, input_spec, verbose)


def select_backend() -> str:
    try:
        AbstractState("REFPROP", "CO2")
        return "REFPROP"
    except Exception:
        tp.CoolPropAbstractState = HEOSAbstractState
        return "HEOS"


def save(fig, name: str) -> None:
    fig.savefig(OUT / name, dpi=110)
    matplotlib.pyplot.close(fig)


def overlay_expansions(fig) -> None:
    """Isentropic and isenthalpic expansion of CO2 from 9 MPa and 308 K to 4 MPa."""
    import numpy as np

    ax = fig.get_axes()[0]
    p_in, T_in, p_out = 9e6, 308.0, 4e6
    s_in = CP.PropsSI("S", "P", p_in, "T", T_in, "CO2")
    h_in = CP.PropsSI("H", "P", p_in, "T", T_in, "CO2")
    p = np.geomspace(p_in, p_out, 60)
    T_isentropic = CP.PropsSI("T", "P", p, "S", np.full_like(p, s_in), "CO2")
    s_isenthalpic = CP.PropsSI("S", "P", p, "H", np.full_like(p, h_in), "CO2")
    T_isenthalpic = CP.PropsSI("T", "P", p, "H", np.full_like(p, h_in), "CO2")
    ax.plot(np.full_like(p, s_in), T_isentropic, color="crimson", lw=2.0, zorder=10, label="isentropic expansion")
    ax.plot(s_isenthalpic, T_isenthalpic, color="seagreen", lw=2.0, ls="--", zorder=10, label="isenthalpic expansion")
    ax.plot([s_in], [T_in], "o", color="black", zorder=11)
    ax.annotate("inlet: 9 MPa, 308 K", (s_in, T_in), xytext=(12, 6), textcoords="offset points", zorder=11)
    ax.legend(loc="upper left")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    backend = select_backend()
    print(f"property backend: {backend}")
    jobs = [
        ("co2_ts.png", lambda: tp.thermoplot(str(CONFIG / "CO2.ini"))),
        ("r1234ze_ts.png", lambda: tp.thermoplot(str(CONFIG / "R1234ze(E).ini"))),
        ("co2_ph.png", lambda: tp.thermoplot(str(EXAMPLES / "CO2_PH.ini"))),
        ("co2_ts_zoom.png", lambda: tp.thermoplot(str(CONFIG / "CO2.ini"),
                                                  {"S_range": [900, 2000], "T_range": [260, 320]})),
        ("co2_ts_no_isolines.png", lambda: tp.thermoplot(str(CONFIG / "CO2.ini"), {"show_isolines": False})),
    ]
    for name, make in jobs:
        start = time.perf_counter()
        save(make(), name)
        print(f"{name:<24} {time.perf_counter() - start:5.1f} s")

    start = time.perf_counter()
    fig = tp.thermoplot(str(CONFIG / "CO2.ini"))
    overlay_expansions(fig)
    save(fig, "co2_ts_overlay.png")
    print(f"{'co2_ts_overlay.png':<24} {time.perf_counter() - start:5.1f} s")


if __name__ == "__main__":
    main()
