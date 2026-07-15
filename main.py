import os
import sys
import pandas as pd
from src.coolprop_interface_thermoplot import CoolPropAbstractState
cwd = os.getcwd()
sys.path.append(f'{cwd}/src/')


import matplotlib.pyplot as plt
import numpy as np
from functools import partial
from src.thermoplot import thermoplot_cached
from src.isolines import construct_saturation_dome
from configthermoplot import ConfigThermoplot





def computeSoundSpeed_p_rho(p: float | np.ndarray, rho: float | np.ndarray, AS: CoolPropAbstractState) -> float | np.ndarray:
    # Ensure inputs are numpy arrays
    p = np.asarray(p, dtype=float)
    rho = np.asarray(rho, dtype=float)
    p, rho = np.broadcast_arrays(p, rho)
    
    # Vectorize the core function, passing self.fluid
    vectorized_func = np.vectorize(
        partial(_computeSingleSoundSpeed_p_rho, AS=AS),
        otypes=[float]
    )
    return vectorized_func(p, rho)

@staticmethod
def _computeSingleSoundSpeed_p_rho(p: float, rho: float, AS: CoolPropAbstractState) -> float:
    """single thdy point evaluation"""
    # check if the state is two phase
    # readers can find interpretation of the phase number in the CoolProp documentation:
    # https://coolprop.org/_static/doxygen/html/namespace_cool_prop.html#aa1ce7c368d1058004293708038241850a648039a97f7392876038eaf56cf91e95
    # under section "phases"
    phase = AS.PropsSI("Phase", "P", p, "D", rho)
    
    # if phase == 6, fluid is in two-phase region. 
    two_phase = False
    if phase == 6:
        two_phase = True

    def _computeSingleSoundSpeed_p_rho_single_phase(p: float, rho: float) -> float:
        a = AS.PropsSI("A", "P", p, "D", rho)      
        return a
    
    def _computeSingleSoundSpeed_p_rho_two_phase(p: float, rho: float) -> float:
        # two-phase (HEM model from Cioffi et al.)
        T = AS.PropsSI("T", "P", p, "D", rho)
        x_V = AS.PropsSI("Q", "P", p, "D", rho)
        x_L = 1 - x_V
        soundSpeed_L = AS.PropsSI("A", "P", p, "Q", 0)
        soundSpeed_V = AS.PropsSI("A", "P", p, "Q", 1)
        rho_L = AS.PropsSI("D", "P", p, "Q", 0)
        rho_V = AS.PropsSI("D", "P", p, "Q", 1)
        c_p_L = AS.PropsSI("Cpmass", "P", p, "Q", 0)
        c_p_V = AS.PropsSI("Cpmass", "P", p, "Q", 1)
        alpha_V = x_V * (rho/rho_V)
        alpha_L = x_L * (rho/rho_L)
        
        # Finite difference for ds/dp at constant Q
        ds_dp_cQ_L = (AS.PropsSI("S", "P", p + 1e3, "Q", 0) -
                        AS.PropsSI("S", "P", p - 1e3, "Q", 0)) / (2 * 1e3)
        ds_dp_cQ_V = (AS.PropsSI("S", "P", p + 1e3, "Q", 1) -
                        AS.PropsSI("S", "P", p - 1e3, "Q", 1)) / (2 * 1e3)

        # Sound speed according to Eq. 29 (Cioffi et al.)
        a = (rho * (
                alpha_L / (rho_L * soundSpeed_L**2) +
                alpha_V / (rho_V * soundSpeed_V**2) +
                T * ((alpha_L * rho_L / c_p_L) * ds_dp_cQ_L**2 +
                        (alpha_V * rho_V / c_p_V) * ds_dp_cQ_V**2)
                ))**(-0.5)
        return a
    if not two_phase:
        # from tests performed in pyshockflow of this function, when computesoundspeed
        # is called in any region other than two-phase near the two-phase dome, 
        # the value is stable. Values inside the two-phase dome (phase == 6) near the 
        # dome can return -9999980 or nan. 
        a = _computeSingleSoundSpeed_p_rho_single_phase(p, rho)
        # common errors:
        if abs(a) > 99999:
            print(f"Warning: Computed sound speed {a} is unusually high for p={p}, rho={rho}.\n"
                "This issue is common when the thdy pair is considered two-phase by CoolProp\n"
                "but is nevertheless evaluated using PropsSI, which from experience only\n"
                "returns sensible values for non-two-phase regions.")
        if np.isnan(a):
            print(f"Warning: Computed sound speed is NaN for p={p}, rho={rho}.\n"
                "This issue is common when the thdy pair is close to the critical point.\n"
                "The user may try relaxing the tolerance of the CoolPropAbstractState_v2\n"
                "_critical_value method. However if the relaxation required is too large\n"
                "it is recommended to launch a separate investigation.")
        return a
    else:
        # but if the value is computed using the cioffi equation, the returned value
        # has no risk of being -9999980 or nan either, so we can be ensured about stability.
        a = _computeSingleSoundSpeed_p_rho_two_phase(p, rho)
        return a


input_file_path = "config/R1234ze(E).ini"
fig = thermoplot_cached(input_file_path)
# axes = fig.get_axes()
# AS = CoolPropAbstractState("REFPROP", "R1234ze(E)")
# config = ConfigThermoplot(config_file=input_file_path)
# config.get_thermoplot_settings()
# dome_coords = construct_saturation_dome(config, AS)
# axes[0].plot(dome_coords[:, 0], dome_coords[:, 1], color='red', lw=1.0, zorder=3) # plot saturation dome
plt.show()

input_file_path = "config/CO2.ini"
fig = thermoplot_cached(input_file_path)
axes = fig.get_axes()
AS = CoolPropAbstractState("REFPROP", "CO2")
config = ConfigThermoplot(config_file=input_file_path)
config.get_thermoplot_settings()
dome_coords = construct_saturation_dome(config, AS)
axes[0].plot(dome_coords[:, 0], dome_coords[:, 1], color='red', lw=1.0, zorder=3) # plot saturation dome
plt.show()







def computeSoundSpeed_de_lorenzo_p_rho(p: float | np.ndarray, rho: float | np.ndarray, AS: CoolPropAbstractState) -> float | np.ndarray:
        # Ensure inputs are numpy arrays
        p = np.asarray(p, dtype=float)
        rho = np.asarray(rho, dtype=float)
        p, rho = np.broadcast_arrays(p, rho)
        
        # Vectorize the core function, passing self.fluid
        vectorized_func = np.vectorize(
            partial(_computeSingleSoundSpeed_de_lorenzo_p_rho, AS=AS),
            otypes=[float]
        )
        return vectorized_func(p, rho)

@staticmethod
def _computeSingleSoundSpeed_de_lorenzo_p_rho(p: float, rho: float, AS: CoolPropAbstractState) -> float:
    """single thdy point evaluation"""
    # check if the state is two phase
    # readers can find interpretation of the phase number in the CoolProp documentation:
    # https://coolprop.org/_static/doxygen/html/namespace_cool_prop.html#aa1ce7c368d1058004293708038241850a648039a97f7392876038eaf56cf91e95
    # under section "phases"
    phase = AS.PropsSI("Phase", "P", p, "D", rho)
    
    # if phase == 6, fluid is in two-phase region. 
    two_phase = False
    if phase == 6:
        two_phase = True

    def _computeSingleSoundSpeed_de_lorenzo_p_rho_single_phase(p: float, rho: float) -> float:
        a = AS.PropsSI("A", "P", p, "D", rho)      
        return a
    
    def _computeSingleSoundSpeed_de_lorenzo_p_rho_two_phase(p: float, rho: float) -> float:
        # two-phase (HEM model from De Lorenzo et al.)
        # compute thdy quantities
        x_eq = AS.PropsSI("Q", "P", p, "D", rho)
        rho_L = AS.PropsSI("D", "P", p, "Q", 0)
        rho_V = AS.PropsSI("D", "P", p, "Q", 1)
        s_L = AS.PropsSI("S", "P", p, "Q", 0)
        s_V = AS.PropsSI("S", "P", p, "Q", 1)

        # compute specific volumes
        nu_L = 1 / rho_L
        nu_V = 1 / rho_V
        nu_m =   x_eq * nu_V + (1 - x_eq) * nu_L  

        # central difference for d(nu)/d(p) at saturation dome boundary
        dnu_dp_cQ_L = (AS.PropsSI("D", "P", p + 1e3, "Q", 0)**(-1) -
                        AS.PropsSI("D", "P", p - 1e3, "Q", 0)**(-1)) / (2 * 1e3)
        dnu_dp_cQ_V = (AS.PropsSI("D", "P", p + 1e3, "Q", 1)**(-1) -
                        AS.PropsSI("D", "P", p - 1e3, "Q", 1)**(-1)) / (2 * 1e3)

        # central difference ds_dp_cQ at the Q under current evaluation. 
        ds_dp_cQ = (AS.PropsSI("S", "P", p + 1e3, "Q", x_eq) -
                    AS.PropsSI("S", "P", p - 1e3, "Q", x_eq)) / (2 * 1e3)    

        # Sound speed according to Eq 27 (De Lorenzo et al.)
        a = np.sqrt( -nu_m**2 *(
            dnu_dp_cQ_L - ds_dp_cQ * (nu_V - nu_L)/(s_V - s_L) + 
            x_eq * (dnu_dp_cQ_V - dnu_dp_cQ_L)
        )**(-1)
        )
        return a
    
    if not two_phase:
        # from tests performed in pyshockflow of this function, when computesoundspeed
        # is called in any region other than two-phase near the two-phase dome, 
        # the value is stable. Values inside the two-phase dome (phase == 6) near the 
        # dome can return -9999980 or nan. 
        a = _computeSingleSoundSpeed_de_lorenzo_p_rho_single_phase(p, rho)
        # common errors:
        if abs(a) > 99999:
            print(f"Warning: Computed sound speed {a} is unusually high for p={p}, rho={rho}.\n"
                "This issue is common when the thdy pair is considered two-phase by CoolProp\n"
                "but is nevertheless evaluated using PropsSI, which from experience only\n"
                "returns sensible values for non-two-phase regions.")
        if np.isnan(a):
            print(f"Warning: Computed sound speed is NaN for p={p}, rho={rho}.\n"
                "This issue is common when the thdy pair is close to the critical point.\n"
                "The user may try relaxing the tolerance of the CoolPropAbstractState_v2\n"
                "_critical_value method. However if the relaxation required is too large\n"
                "it is recommended to launch a separate investigation.")
        return a
    else:
        # but if the value is computed using the de Lorenzo equation, the returned value
        # has no risk of being -9999980 or nan either, so we can be ensured about stability.
        a = _computeSingleSoundSpeed_de_lorenzo_p_rho_two_phase(p, rho)
        return a


AS = CoolPropAbstractState("REFPROP", "water")

df = pd.read_csv("HEM_sos_benchmark_of_dem_fig_1b.csv")
data = dict.fromkeys(df.columns)
for i, col in enumerate(df.columns):
    data[col] = df.iloc[1:, i].values

alpha_V = data["alpha_V"]
# the next parameters are known from how the test case was constructed.
p = np.ones_like(alpha_V) * 0.1e6  # 0.1 MPa
rho_v = AS.PropsSI("D", "P", p, "Q", np.ones_like(alpha_V))

# solve equation iteratively for rho
def func(Q, alpha_v, rho_v, p):
    if np.any(Q < 0) or np.any(Q > 1):
        return np.inf  # Return a large number to indicate an invalid solution
    else:
        return (AS.PropsSI("D", "P", p, "Q", Q)/rho_v)*Q - alpha_v
from scipy.optimize import newton
Q_new = newton(func, x0=np.full_like(alpha_V, 1e-6),
        args=(alpha_V, rho_v, p))

rho_new = AS.PropsSI("D", "P", p, "Q", Q_new)

# compute the sound speed using the FluidReal method
soundSpeed_HEM = computeSoundSpeed_p_rho(p, rho_new, AS)


plt.plot(alpha_V, soundSpeed_HEM, label="HEM Sound Speed (m/s)", color='blue', lw=1.0, zorder=3)
plt.plot(alpha_V, data["HEM_sound_speed"], label="De Lorenzo Sound Speed (m/s)", color='orange', lw=1.0, zorder=3)
plt.ylim(0,120)

plt.show()

def rel_abs_error(a1, a2):
    rel_error = np.abs(a1 - a2) / np.abs(a2)
    abs_error = np.abs(a1 - a2)
    return rel_error, abs_error

print("Max relative error:", np.max(rel_abs_error(soundSpeed_HEM, data["HEM_sound_speed"])[0]), " max absolute error:", np.max(rel_abs_error(soundSpeed_HEM, data["HEM_sound_speed"])[1]))

# convert to log space
soundSpeed_HEM_log = np.log10(soundSpeed_HEM)
soundSpeed_DeLorenzo_log = np.log10(data["HEM_sound_speed"])

print("Max relative error (log space):", np.max(rel_abs_error(soundSpeed_HEM_log, soundSpeed_DeLorenzo_log)[0]), "max absolute error (log space):", np.max(rel_abs_error(soundSpeed_HEM_log, soundSpeed_DeLorenzo_log)[1]))

# plot
plt.plot(alpha_V, soundSpeed_HEM_log, label="HEM Sound Speed (log10)", color='blue', lw=1.0, zorder=3)
plt.plot(alpha_V, soundSpeed_DeLorenzo_log, label="De Lorenzo Sound Speed (log10)", color='orange', lw=1.0, zorder=3)

plt.show()

