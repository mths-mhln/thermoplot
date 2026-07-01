import os
import sys
from src.coolprop_interface_thermoplot import CoolPropAbstractState
cwd = os.getcwd()
sys.path.append(f'{cwd}/src/')


import matplotlib.pyplot as plt
import numpy as np
from functools import partial
from src.thermoplot import thermoplot_cached
from src.isolines import construct_saturation_dome
from configthermoplot import ConfigThermoplot



def computeSoundSpeed_p_rho(self, p, rho):
    """Public method - handles self.fluid and vectorization"""
    # Ensure inputs are numpy arrays
    p = np.asarray(p, dtype=float)
    rho = np.asarray(rho, dtype=float)
    p, rho = np.broadcast_arrays(p, rho)
    
    # Vectorize the core function, passing self.fluid
    vectorized_func = np.vectorize(
        partial(_computeSoundSpeed_p_rho_single, fluid="CO2"),
        otypes=[float]
    )
    
    return vectorized_func(p, rho)

@staticmethod
def _computeSoundSpeed_p_rho_single(p, rho, fluid):
    """Core scalar function - no self, pure computation"""
    # check if the state is single phase or two phase
    T = AS.PropsSI("T", "P", p, "D", rho)
    T_crit = AS.PropsSI("Tcrit")
    if T < 0.99 * T_crit: 
        # 0.99 because an evaluation had T = 304.1281982111877, T_crit = 304.1282 (CO2) 
        # and S_sat_V was not defined, which is acceptable from CoolProp
        S_sat_V = AS.PropsSI("S", "T", T, "Q", 1)
        S_sat_L = AS.PropsSI("S", "T", T, "Q", 0)
        non_saturable = False
    else:
        non_saturable = True
    S = AS.PropsSI("S", "P", p, "D", rho)

    def _computeSoundSpeed_p_rho_single_phase(p, rho, fluid):
        a = AS.PropsSI("A", "P", p, "D", rho, fluid)
        return a
    
    def _computeSoundSpeed_p_rho_two_phase(p, rho, fluid):
        # two-phase (HEM model from Cioffi et al.)
        x_V = AS.PropsSI("Q", "P", p, "D", rho, fluid)
        x_L = 1 - x_V
        soundSpeed_L = AS.PropsSI("A", "P", p, "Q", 0, fluid)
        soundSpeed_V = AS.PropsSI("A", "P", p, "Q", 1, fluid)
        rho_L = AS.PropsSI("D", "P", p, "Q", 0, fluid)
        rho_V = AS.PropsSI("D", "P", p, "Q", 1, fluid)
        c_p_L = AS.PropsSI("Cpmass", "P", p, "Q", 0, fluid)
        c_p_V = AS.PropsSI("Cpmass", "P", p, "Q", 1, fluid)
        alpha_V = x_V * (rho/rho_V)
        alpha_L = x_L * (rho/rho_L)
        
        # Finite difference for ds/dp at constant Q
        ds_dp_cQ_L = (AS.PropsSI("S", "P", p + 1e3, "Q", 0, fluid) -
                        AS.PropsSI("S", "P", p - 1e3, "Q", 0, fluid)) / (2 * 1e3)
        ds_dp_cQ_V = (AS.PropsSI("S", "P", p + 1e3, "Q", 1, fluid) -
                        AS.PropsSI("S", "P", p - 1e3, "Q", 1, fluid)) / (2 * 1e3)

        # Sound speed according to Eq. 29 (Cioffi et al.)
        a = (rho * (
                alpha_L / (rho_L * soundSpeed_L**2) +
                alpha_V / (rho_V * soundSpeed_V**2) +
                T * ((alpha_L * rho_L / c_p_L) * ds_dp_cQ_L**2 +
                        (alpha_V * rho_V / c_p_V) * ds_dp_cQ_V**2)
                ))**(-0.5)
        return a
    if non_saturable:
        # only option is single phase
        a = _computeSoundSpeed_p_rho_single_phase(p, rho, fluid)
        return a
    else:
        # can be two-phase or single phase:
        if S <= S_sat_L or S >= S_sat_V:
            # try single phase first. At boundary can yield some errors.
            try: 
                a = _computeSoundSpeed_p_rho_single_phase(p, rho, fluid)
            except:
                a = _computeSoundSpeed_p_rho_two_phase(p, rho, fluid)
            return a
        else:
            a = _computeSoundSpeed_p_rho_two_phase(p, rho, fluid)
            return a 


input_file_path = "config/CO2.ini"
fig = thermoplot_cached(input_file_path)
axes = fig.get_axes()
AS = CoolPropAbstractState("REFPROP", "CO2")
config = ConfigThermoplot(config_file=input_file_path)
config.get_thermoplot_settings()
dome_coords = construct_saturation_dome(config, AS)
axes[0].plot(dome_coords[:, 0], dome_coords[:, 1], color='red', lw=1.0, zorder=3) # plot saturation dome
plt.show()








